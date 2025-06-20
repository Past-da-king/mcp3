# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse # Or FileResponse
from pathlib import Path
import uvicorn
import os
import sys
import json
import traceback # Added
from mcp.client.streamable_http import streamablehttp_client # Added
from mcp import ClientSession # Added
from mcp.shared.exceptions import McpError # Added

# Add backend directory to sys.path to import mcp_client_logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mcp_client_logic import (
    process_user_message_stream,
    initialize_chat_history,
    cleanup_chat_history,
    clear_specific_chat_history,
    MCP_SERVER_URL, # Added
    send_websocket_message # Added
)

# --- BEGIN DEBUG CODE ---
try:
    # Attempt to import the module itself to inspect it
    import mcp_client_logic
    print("DEBUG: Successfully imported 'mcp_client_logic' module itself.")
    print(f"DEBUG: Contents of mcp_client_logic module (via dir()): {dir(mcp_client_logic)}")

    if hasattr(mcp_client_logic, 'clear_specific_chat_history'):
        print("DEBUG: 'clear_specific_chat_history' IS found in mcp_client_logic using hasattr().")
    else:
        print("DEBUG: 'clear_specific_chat_history' IS NOT found in mcp_client_logic using hasattr().")

    # Explicitly test the problematic import again within a try-except
    from mcp_client_logic import clear_specific_chat_history as csch_test_import
    print(f"DEBUG: Successfully imported 'clear_specific_chat_history' directly via from-import: {type(csch_test_import)}")

except ImportError as e_debug:
    print(f"DEBUG: ImportError during debug block: {e_debug}")
except Exception as e_general_debug:
    print(f"DEBUG: General error during debug block: {e_general_debug}")
# --- END DEBUG CODE ---

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"  # General static files (HTML, CSS, JS)
INDEX_HTML_FILE = STATIC_DIR / "index.html"

# Define and create directory for plot images
# This path should correspond to where calculater_mcp.py saves plots.
# ProjectRoot/static/plots
PLOT_SAVE_DIR_RELATIVE_TO_PROJECT_ROOT = "static/plots"
PLOT_STATIC_DIR_ABSOLUTE = BASE_DIR.parent / PLOT_SAVE_DIR_RELATIVE_TO_PROJECT_ROOT
os.makedirs(PLOT_STATIC_DIR_ABSOLUTE, exist_ok=True)

# Mount static files (HTML, CSS, JS for frontend)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static_root")

# Mount plot images directory
# This makes files from ProjectRoot/static/plots available at /static/plots/filename.png
app.mount("/static/plots", StaticFiles(directory=PLOT_STATIC_DIR_ABSOLUTE), name="static_plots")


@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    # Serve the main HTML page
    # For simplicity, reading it here. For complex apps, use FileResponse or templating.
    try:
        return HTMLResponse(content=INDEX_HTML_FILE.read_text())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Chat UI - index.html not found</h1><p>Make sure static/index.html exists.</p>", status_code=404)

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_id = id(websocket)
    initialize_chat_history(ws_id)
    print(f"WebSocket connection accepted from {websocket.client.host}:{websocket.client.port}, ID: {ws_id}")

    mcp_session_active = False # Flag to track if session was successfully started
    try:
        # Attempt to connect to MCP server ONCE per WebSocket session
        await send_websocket_message(websocket, "status", f"Attempting to connect to MCP server at {MCP_SERVER_URL}...")
        async with streamablehttp_client(MCP_SERVER_URL) as (read, write, _http_session):
            await send_websocket_message(websocket, "status", "Connected to MCP server's HTTP transport.")
            async with ClientSession(read, write) as mcp_session:
                await mcp_session.initialize()
                await send_websocket_message(websocket, "status", "MCP session initialized and ready.")
                mcp_session_active = True
                print(f"MCP session established for WebSocket ID: {ws_id}")

                # The main message processing loop, now nested inside MCP session contexts
                while True:
                    user_message_json = await websocket.receive_text()
                    user_message_data = json.loads(user_message_json)

                    if user_message_data.get("action") == "clear_server_history":
                        clear_specific_chat_history(ws_id)
                        print(f"Server-side history cleared for WebSocket ID: {ws_id} due to client request.")
                        await send_websocket_message(websocket, "status", "Server-side chat history cleared.")
                        continue # Wait for next message

                    user_prompt = user_message_data.get("message")
                    if user_prompt:
                        print(f"Processing prompt '{user_prompt}' for WebSocket ID: {ws_id} with active MCP session.")
                        await process_user_message_stream(user_prompt, websocket, mcp_session) # Pass the session
                    elif "action" not in user_message_data: # Avoid error on our own actions
                        await send_websocket_message(websocket, "error", "Empty message received (no prompt or action).")

    except McpError as mcp_e: # Catch MCP connection/initialization errors
        print(f"MCP Connection/Initialization Error for WebSocket ID {ws_id}: {mcp_e}")
        traceback.print_exc()
        await send_websocket_message(websocket, "error", f"Could not establish session with MCP server: {str(mcp_e)}")
    except WebSocketDisconnect:
        print(f"WebSocket connection closed for ID: {ws_id}")
    except Exception as e: # Catch any other unexpected errors during MCP setup or general handling
        print(f"Error in WebSocket handler for ID {ws_id}: {e}")
        traceback.print_exc()
        try:
            await send_websocket_message(websocket, "error", f"Server error: {str(e)}")
        except Exception:
            pass
        if not isinstance(e, WebSocketDisconnect): # Ensure close if not already a disconnect
            await websocket.close(code=1011)
    finally:
        cleanup_chat_history(ws_id)
        if not mcp_session_active:
            print(f"MCP session was not activated for WebSocket ID {ws_id}. Chat may have been non-functional for MCP tasks.")
            # Optionally inform client and close if connection was accepted but MCP failed.
            # This part might need refinement based on desired client experience if MCP fails post-connection.
            # if websocket.client_state == WebSocketState.CONNECTED:
            #    await send_websocket_message(websocket, "error", "Failed to maintain MCP session. Please refresh.")
            #    await websocket.close(code=1011)
        print(f"WebSocket resources cleaned up for ID: {ws_id}")