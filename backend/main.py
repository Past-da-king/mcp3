# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse # Or FileResponse
from pathlib import Path
import uvicorn
import os
import sys
import json

# Add backend directory to sys.path to import mcp_client_logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mcp_client_logic import process_user_message_stream # We'll create this next

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"
INDEX_HTML_FILE = STATIC_DIR / "index.html"

# Mount static files (HTML, CSS, JS for frontend)
# Ensure this path is correct relative to where you run uvicorn
# If running uvicorn from chat_ui_project/, then 'static' is correct
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
    print("WebSocket connection accepted.")
    try:
        while True:
            user_message_json = await websocket.receive_text()
            user_message_data = json.loads(user_message_json)
            user_prompt = user_message_data.get("message")

            if user_prompt:
                print(f"Received prompt via WebSocket: {user_prompt}")
                # This function will handle connecting to MCP, Gemini, and streaming back
                await process_user_message_stream(user_prompt, websocket)
            else:
                await websocket.send_json({"type": "error", "content": "Empty message received."})

    except WebSocketDisconnect:
        print("WebSocket connection closed.")
    except Exception as e:
        print(f"Error in WebSocket handler: {e}")
        await websocket.send_json({"type": "error", "content": f"Server error: {str(e)}"})
        await websocket.close(code=1011) # Internal server error