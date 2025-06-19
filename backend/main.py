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
from mcp_client_logic import (
    process_user_message_stream,
    initialize_chat_history,
    cleanup_chat_history
)

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
        print(f"WebSocket connection closed for ID: {ws_id}")
    except Exception as e:
        print(f"Error in WebSocket handler for ID {ws_id}: {e}")
        # It's good practice to try and inform the client if possible,
        # but the connection might already be compromised.
        try:
            await websocket.send_json({"type": "error", "content": f"Server error: {str(e)}"})
        except Exception: # Catch error if send fails (e.g. broken pipe)
            pass
        # Ensure close is called if not a disconnect exception
        if not isinstance(e, WebSocketDisconnect):
            await websocket.close(code=1011) # Internal server error
    finally:
        cleanup_chat_history(ws_id)
        print(f"WebSocket resources cleaned up for ID: {ws_id}")