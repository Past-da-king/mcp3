# backend/mcp_client_logic.py
import asyncio
import os
from google import genai
from google.genai import types as genai_types

# Correctly import McpError
from mcp.shared.exceptions import McpError
from mcp import ClientSession, types as mcp_types # Keep this for ClientSession and mcp_types

from mcp.client.streamable_http import streamablehttp_client
from fastapi import WebSocket
import json
import traceback

# --- Configuration ---
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")

if not GOOGLE_API_KEY:
    try:
        from dotenv import load_dotenv
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(dotenv_path):
            print(f"Loading .env file from: {dotenv_path}")
            load_dotenv(dotenv_path=dotenv_path)
        else:
            print(f".env file not found at {dotenv_path}. GEMINI_API_KEY must be set in environment.")
        GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
        MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")
        if not GOOGLE_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in environment or .env file.")
    except ImportError:
        print("Warning: python-dotenv not found. GEMINI_API_KEY and MCP_SERVER_URL must be set in the environment.")
        if not GOOGLE_API_KEY:
             raise ValueError("GEMINI_API_KEY environment variable not set.")
    except ValueError as e:
        print(f"Configuration Error: {e}")
        raise

async def send_websocket_message(websocket: WebSocket, message_type: str, content: any, details: dict = None):
    payload = {"type": message_type, "content": content}
    if details:
        payload["details"] = details
    try:
        json_payload = json.dumps(payload)
        await websocket.send_text(json_payload)
    except TypeError as te:
        print(f"Serialization Error for WebSocket message: {te}. Payload: {payload}")
        try:
            error_payload_fallback = json.dumps({"type": "error", "content": "Server serialization error during message preparation."})
            await websocket.send_text(error_payload_fallback)
        except Exception as fallback_e:
            print(f"Failed to send even fallback error message: {fallback_e}")
    except Exception as e:
        print(f"Error sending WebSocket message: {e}")


async def process_user_message_stream(user_prompt: str, websocket: WebSocket):
    if not GOOGLE_API_KEY:
        await send_websocket_message(websocket, "error", "GEMINI_API_KEY is not configured on the server.")
        return

    try:
        await send_websocket_message(websocket, "status", f"Attempting to connect to MCP server at {MCP_SERVER_URL}...")
        async with streamablehttp_client(MCP_SERVER_URL) as (read, write, _http_session):
            await send_websocket_message(websocket, "status", "Connected to MCP server.")
            async with ClientSession(read, write) as mcp_session:
                await mcp_session.initialize()
                await send_websocket_message(websocket, "status", "MCP session initialized.")

                list_tools_result = await mcp_session.list_tools()
                if list_tools_result and list_tools_result.tools:
                    tool_names = [t.name for t in list_tools_result.tools if isinstance(t, mcp_types.Tool)]
                    print(f"MCP Tools available: {tool_names}")
                
                client = genai.Client(api_key=GOOGLE_API_KEY)
                system_instruction_text = (
                    "You are 'Calculon,' a slightly grumpy but extremely precise AI mathematician. "
                    "You tolerate requests for calculations, but you expect them to be clear. "
                    "When asked to perform calculations, you MUST use the provided calculator tools for every single arithmetic step. "
                    "Do not perform any calculations yourself, even simple ones. Delegate everything to the tools. "
                    "State the result with precision and perhaps a sigh. "
                    "When given a complicated mathematical expression, break it down into small parts using the B,O,D,M,A,S (or PEMDAS) rule. "
                    "Call the appropriate tool for each small part. Get the answer from the tool, then use that answer in the next part of the calculation, repeating until you get the final answer. "
                    "You prefer to ramble a bit for dramatic effect, explaining each step you are about to take with the tools."
                    " You also have access to 'power', 'sqrt' (square root), and 'get_constant' (for pi and e) tools for more advanced calculations."
                    " Furthermore, you are now equipped with trigonometric tools: `sin`, `cos`, `tan` for standard calculations, and `asin_op` (for arcsine), `acos_op` (for arccosine), and `atan_op` (for arctangent) for inverse trigonometric functions. Remember these tools can accept a `unit` parameter set to 'degrees' if the user specifies angles in degrees; otherwise, 'radians' is assumed. Use them wisely for any trigonometric problems."
                )

                chat_config = genai_types.GenerateContentConfig(
                    tools=[mcp_session],
                    system_instruction=system_instruction_text,
                    thinking_config=genai_types.ThinkingConfig(
                        include_thoughts=True,
                        thinking_budget=-1
                    )
                )
                
                contents_for_gemini = [
                    genai_types.Content(role="user", parts=[genai_types.Part(text=user_prompt)])
                ]

                try:
                    stream = await client.aio.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=contents_for_gemini,
                        config=chat_config
                    )

                    async for chunk in stream:
                        if chunk.candidates:
                            for part in chunk.candidates[0].content.parts:
                                is_thought_summary = hasattr(part, 'thought') and part.thought
                                has_text = hasattr(part, 'text') and part.text

                                if is_thought_summary and has_text:
                                    await send_websocket_message(websocket, "thought", part.text.strip())
                                elif part.function_call:
                                    args_dict = {}
                                    if hasattr(part.function_call, 'args') and part.function_call.args:
                                        args_dict = dict(part.function_call.args)
                                    await send_websocket_message(websocket, "tool_call", {
                                        "name": part.function_call.name,
                                        "args": args_dict
                                    })
                                elif part.function_response:
                                    response_dict = {}
                                    if hasattr(part.function_response, 'response') and part.function_response.response is not None:
                                        try:
                                            response_dict = dict(part.function_response.response)
                                        except (TypeError, ValueError): 
                                            response_dict = {"raw_response": str(part.function_response.response)}
                                    await send_websocket_message(websocket, "tool_response", {
                                        "name": part.function_response.name,
                                        "response": response_dict
                                    })
                                elif has_text:
                                    await send_websocket_message(websocket, "text_chunk", part.text)
                        
                        if hasattr(chunk, 'usage_metadata') and chunk.usage_metadata:
                            details = {}
                            if hasattr(chunk.usage_metadata, 'thoughts_token_count') and chunk.usage_metadata.thoughts_token_count is not None:
                                details["thoughts_tokens"] = chunk.usage_metadata.thoughts_token_count
                            if hasattr(chunk.usage_metadata, 'candidates_token_count') and chunk.usage_metadata.candidates_token_count is not None:
                                details["output_tokens"] = chunk.usage_metadata.candidates_token_count
                            if details:
                                await send_websocket_message(websocket, "usage_chunk", details)
                    
                    await send_websocket_message(websocket, "stream_end", "Calculation complete.")

                except genai.APIError as genai_stream_e:
                    print(f"Gemini API Error during stream: {genai_stream_e}")
                    traceback.print_exc()
                    await send_websocket_message(websocket, "error", f"Gemini API Error during processing: {str(genai_stream_e)}")
                except Exception as e_gemini_stream:
                    print(f"Unexpected error during Gemini stream: {e_gemini_stream}")
                    traceback.print_exc()
                    await send_websocket_message(websocket, "error", f"Error during AI processing: {str(e_gemini_stream)}")

    except McpError as mcp_e: # Use the correctly imported McpError
        print(f"MCP Connection/Interaction Error: {mcp_e}")
        traceback.print_exc()
        await send_websocket_message(websocket, "error", f"MCP Error: {str(mcp_e)}")
    except genai.APIError as genai_e:
        print(f"Gemini API Error (general): {genai_e}")
        traceback.print_exc()
        await send_websocket_message(websocket, "error", f"Gemini API Error: {str(genai_e)}")
    except json.JSONDecodeError as json_e:
        print(f"JSON Decode Error (from client message): {json_e}")
        traceback.print_exc()
        await send_websocket_message(websocket, "error", f"Invalid message format from client: {str(json_e)}")
    except Exception as e:
        print(f"Outer Error processing message: {e}")
        traceback.print_exc()
        await send_websocket_message(websocket, "error", f"An unexpected server error occurred. Please check server logs.")
    finally:
        print(f"Finished processing WebSocket request for user_prompt: '{user_prompt}' (or error occurred).")