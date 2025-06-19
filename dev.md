# Codebase Snapshot

Source Directory: `mcp3`

## README.md

```markdown
# Calculon: AI Math Chatbot with MCP Tool Integration

Calculon is a web-based AI chatbot that specializes in mathematical calculations. It leverages Google's Gemini AI and a custom MCP (Modular Calculation Protocol) server to perform arithmetic operations using defined tools, ensuring all calculations are delegated to the backend for accuracy and transparency.

## Features

- **Conversational Math Chatbot:** Interact with "Calculon," an AI mathematician with a personality, via a web chat interface.
- **MCP Tool Integration:** All arithmetic (add, subtract, multiply, divide) is performed using backend tools, not by the AI directly.
- **Streaming Responses:** Real-time, chunked responses and tool call explanations are streamed to the frontend.
- **WebSocket Communication:** Fast, interactive chat experience using WebSockets.
- **Frontend:** Simple HTML/CSS/JS interface (no frameworks required).
- **Backend:** FastAPI server connects the frontend, Gemini AI, and MCP server.

## Project Structure

```
.env
README.md
ss.py                  # Codebase snapshot tool
backend/
    main.py            # FastAPI backend server
    mcp_client_logic.py# Handles Gemini/MCP logic and WebSocket streaming
mcp/
    calculater_mcp.py  # MCP server with calculator tools
static/
    index.html         # Chat UI
    css/
        style.css
    js/
        app.js
```

## How It Works

1. **User** enters a math question in the chat UI.
2. **Frontend** sends the message via WebSocket to the backend.
3. **Backend** (FastAPI) receives the message and passes it to Gemini AI, providing access to MCP calculator tools.
4. **Gemini AI** breaks down the problem, calls MCP tools for each arithmetic step, and streams thoughts, tool calls, and results back to the frontend.
5. **Frontend** displays AI responses, tool usage, and internal thoughts in real time.

## Setup & Running

### Prerequisites

- Python 3.10+
- Node.js (optional, for frontend development)
- [Google Gemini API key](https://ai.google.dev/)
- MCP Python package (and dependencies)

### 1. Install Python Dependencies

```sh
pip install fastapi uvicorn python-dotenv google-generativeai mcp
```

### 2. Configure Environment

Create a `.env` file in the project root:

```
GEMINI_API_KEY="your-gemini-api-key"
MCP_SERVER_URL=http://127.0.0.1:8000/mcp
```


## Running the Project

Open two terminals and run the following commands:

**1. Start the backend server (on port 8001):**
```sh
uvicorn main:app --reload --port 8001
```

**2. Start the MCP calculator server:**
```sh
mcp run calculater_mcp.py --transport streamable-http
```

Then, open [http://localhost:8001/](http://localhost:8001/) in your browser to use the chat interface.

## Usage

- Type a math question (e.g., "What is (5 + 3) * 2?") and send.
- Calculon will explain each step, call the appropriate tool, and show the result.

## Codebase Snapshot Tool

Use `ss.py` to create a Markdown snapshot of the codebase or reconstruct the codebase from a snapshot.

- **Snapshot:**  
  `python ss.py fm ./ -o snapshot.md`
- **Recreate:**  
  `python ss.py mf snapshot.md -o ./recreated_project`

## License

MIT License

---

**Note:** This project is for educational/demo purposes. Do not expose your API keys in production environments.
```

## dev.md

```markdown

```

## requirements.txt

```
fastapi
uvicorn
python-dotenv
google-genai
mcp

```

## ss.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standalone Codebase Snapshot Tool (Concise Commands)

This script provides two main functions, runnable from the command line:
1.  fm <folder>: Creates a single Markdown file snapshot from a source code folder.
2.  mf <markdown_file>: Recreates a folder structure from a Markdown snapshot file.

Usage:
  # Create snapshot FROM 'my_project_folder' TO 'snapshot.md' (Folder -> Markdown)
  python this_script.py fm ./my_project_folder -o snapshot.md

  # Create snapshot with additional ignore patterns
  python this_script.py fm ./proj -o out.md --ignore "*.log" --ignore "temp/"

  # Recreate folder structure FROM 'snapshot.md' TO 'recreated_project' (Markdown -> Folder)
  python this_script.py mf snapshot.md -o ./recreated_project
"""

import os
import mimetypes
import fnmatch
import platform
import argparse
import sys

# --- Configuration ---
ENCODING = 'utf-8'

# --- Default Ignore Patterns ---
DEFAULT_IGNORE_PATTERNS = [
    '.git', '.gitignore', '.gitattributes', '.svn', '.hg', 'node_modules',
    'bower_components', 'venv', '.venv', 'env', '.env', '.env.*', '*.pyc',
    '__pycache__', 'build', 'dist', 'target', '*.o', '*.so', '*.dll', '*.exe',
    '*.class', '*.jar', '*.war', '*.log', '*.tmp', '*.swp', '*.swo', '.DS_Store',
    'Thumbs.db', '.vscode', '.idea', '*.sublime-project', '*.sublime-workspace',
    '*.zip', '*.tar', '*.gz', '*.rar', 'credentials.*', 'config.local.*',
    'settings.local.py',".next", "package-lock.json"
]

# --- Core Helper Functions (No Changes Here) ---

def is_ignored(relative_path, ignore_patterns):
    normalized_path = relative_path.replace("\\", "/")
    basename = os.path.basename(normalized_path)
    is_case_sensitive_fs = platform.system() != "Windows"
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(basename, pattern) or \
           (not is_case_sensitive_fs and fnmatch.fnmatch(basename.lower(), pattern.lower())):
            return True
        if fnmatch.fnmatch(normalized_path, pattern) or \
           (not is_case_sensitive_fs and fnmatch.fnmatch(normalized_path.lower(), pattern.lower())):
            return True
    return False

def guess_language(filepath):
    mimetypes.init()
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type:
        lang_map_mime = {
            "text/x-python": "python", "application/x-python-code": "python",
            "text/javascript": "javascript", "application/javascript": "javascript",
            "text/html": "html", "text/css": "css", "application/json": "json",
            "application/xml": "xml", "text/xml": "xml",
            "text/x-java-source": "java", "text/x-java": "java",
            "text/x-csrc": "c", "text/x-c": "c", "text/x-c++src": "cpp", "text/x-c++": "cpp",
            "application/x-sh": "bash", "text/x-shellscript": "bash",
            "text/markdown": "markdown", "text/x-yaml": "yaml", "application/x-yaml": "yaml",
            "text/plain": ""
        }
        if mime_type in lang_map_mime: return lang_map_mime[mime_type]
        if mime_type.startswith("text/"): return ""
    _, ext = os.path.splitext(filepath.lower())
    lang_map_ext = {
        ".py": "python", ".pyw": "python", ".js": "javascript", ".mjs": "javascript", ".cjs": "javascript",
        ".html": "html", ".htm": "html", ".css": "css", ".java": "java", ".cpp": "cpp", ".cxx": "cpp",
        ".cc": "cpp", ".hpp": "cpp", ".hxx": "cpp", ".c": "c", ".h": "c", ".cs": "csharp", ".php": "php",
        ".rb": "ruby", ".go": "go", ".rs": "rust", ".ts": "typescript", ".tsx": "typescript",
        ".json": "json", ".xml": "xml", ".yaml": "yaml", ".yml": "yaml", ".sh": "bash", ".bash": "bash",
        ".sql": "sql", ".md": "markdown", ".markdown": "markdown", ".txt": ""
    }
    return lang_map_ext.get(ext, "")

def write_code_to_file(output_dir, relative_filepath, code_lines, encoding=ENCODING):
    safe_relative_path = os.path.normpath(relative_filepath).replace("\\", "/")
    if safe_relative_path.startswith("..") or os.path.isabs(safe_relative_path):
        print(f"[WRITE] [WARN] Skipping potentially unsafe path: {relative_filepath}")
        return False
    abs_output_dir = os.path.abspath(output_dir)
    full_path = os.path.join(abs_output_dir, safe_relative_path)
    abs_full_path = os.path.abspath(full_path)
    if not abs_full_path.startswith(abs_output_dir + os.path.sep) and abs_full_path != abs_output_dir:
        print(f"[WRITE] [ERROR] Security Error: Attempted write outside target directory: {relative_filepath} -> {abs_full_path}")
        return False
    dir_name = os.path.dirname(full_path)
    try:
        if dir_name: os.makedirs(dir_name, exist_ok=True)
        if os.path.isdir(full_path):
             print(f"[WRITE] [ERROR] Cannot write file. Path exists and is a directory: {full_path}")
             return False
        with open(full_path, "w", encoding=encoding) as outfile:
            outfile.writelines(code_lines)
        return True
    except OSError as e:
        print(f"[WRITE] [ERROR] OS Error writing file {full_path}: {e}")
        return False
    except Exception as e:
        print(f"[WRITE] [ERROR] General Error writing file {full_path}: {e}")
        return False

# --- Main Logic Functions (No Changes Here) ---

def create_codebase_snapshot(root_dir, output_file, encoding=ENCODING, base_ignore_patterns=DEFAULT_IGNORE_PATTERNS, user_ignore_patterns=[]):
    processed_files_count = 0
    ignored_items_count = 0
    errors = []
    all_ignore_patterns = list(set(base_ignore_patterns + user_ignore_patterns))
    abs_root = os.path.abspath(root_dir)
    if not os.path.isdir(abs_root):
        print(f"[ERROR] Source directory not found or not a directory: {abs_root}", file=sys.stderr)
        return False, 0, 0, ["Source directory not found."]

    print("-" * 60)
    print(f"Starting snapshot creation (Folder -> Markdown):")
    print(f"  Source: {abs_root}")
    print(f"  Output: {output_file}")
    print(f"  Ignoring: {all_ignore_patterns}")
    print("-" * 60)
    try:
        with open(output_file, "w", encoding=encoding) as md_file:
            md_file.write("# Codebase Snapshot\n\n")
            md_file.write(f"Source Directory: `{os.path.basename(abs_root)}`\n\n")
            for dirpath, dirnames, filenames in os.walk(abs_root, topdown=True):
                dirs_to_remove = set()
                for d in dirnames:
                    rel_dir_path = os.path.relpath(os.path.join(dirpath, d), abs_root)
                    if is_ignored(rel_dir_path, all_ignore_patterns): dirs_to_remove.add(d)
                if dirs_to_remove:
                    ignored_items_count += len(dirs_to_remove)
                    dirnames[:] = [d for d in dirnames if d not in dirs_to_remove]
                filenames.sort()
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    relative_filepath = os.path.relpath(filepath, abs_root).replace("\\", "/")
                    if is_ignored(relative_filepath, all_ignore_patterns):
                        ignored_items_count += 1; continue
                    processed_files_count += 1
                    print(f"[PROCESS] Adding: {relative_filepath}")
                    md_file.write(f"## {relative_filepath}\n\n")
                    try:
                        try:
                             with open(filepath, "r", encoding=encoding) as f_content: content = f_content.read()
                             language = guess_language(filepath)
                             md_file.write(f"```{language}\n{content}\n```\n\n")
                        except UnicodeDecodeError:
                             md_file.write("```\n**Note:** File appears to be binary or uses an incompatible encoding.\nContent not displayed.\n```\n\n")
                             print(f"[WARN] Binary or non-{encoding} file skipped content: {relative_filepath}")
                        except Exception as read_err:
                             errors.append(f"Error reading file '{relative_filepath}': {read_err}")
                             md_file.write(f"```\n**Error reading file:** {read_err}\n```\n\n")
                             print(f"[ERROR] Could not read file: {relative_filepath} - {read_err}")
                    except Exception as e:
                        errors.append(f"Error processing file '{relative_filepath}': {e}")
                        md_file.write(f"```\n**Error processing file:** {e}\n```\n\n")
                        print(f"[ERROR] Processing failed for: {relative_filepath} - {e}")
    except IOError as e:
        print(f"[ERROR] Failed to write snapshot file '{output_file}': {e}", file=sys.stderr)
        return False, processed_files_count, ignored_items_count, [f"IOError writing snapshot: {e}"]
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during snapshot generation: {e}", file=sys.stderr)
        return False, processed_files_count, ignored_items_count, [f"Unexpected error: {e}"]
    print("-" * 60)
    print(f"Snapshot creation finished.")
    print(f"  Processed: {processed_files_count} files")
    print(f"  Ignored:   {ignored_items_count} items")
    if errors: print(f"  Errors:    {len(errors)}"); [print(f"    - {err}") for err in errors]
    print("-" * 60)
    return True, processed_files_count, ignored_items_count, errors

def extract_codebase(md_file, output_dir, encoding=ENCODING):
    created_files_count = 0; errors = []; file_write_attempts = 0
    abs_output_dir = os.path.abspath(output_dir)
    if not os.path.isfile(md_file):
        print(f"[ERROR] Snapshot file not found: {md_file}", file=sys.stderr)
        return False, 0, ["Snapshot file not found."]
    print("-" * 60); print(f"Starting codebase extraction (Markdown -> Folder):"); print(f"  Snapshot: {md_file}"); print(f"  Output Directory: {abs_output_dir}"); print("-" * 60)
    try:
        os.makedirs(abs_output_dir, exist_ok=True); print(f"[INFO] Ensured output directory exists: {abs_output_dir}")
    except OSError as e: print(f"[ERROR] Failed to create output directory '{abs_output_dir}': {e}", file=sys.stderr); return False, 0, [f"Failed to create output directory: {e}"]
    try:
        with open(md_file, "r", encoding=encoding) as f: lines = f.readlines()
    except Exception as e: print(f"[ERROR] Failed to read snapshot file '{md_file}': {e}", file=sys.stderr); return False, 0, [f"Failed to read snapshot file: {e}"]
    relative_filepath = None; in_code_block = False; code_lines = []; skip_block_content = False
    for line_num, line in enumerate(lines, 1):
        line_stripped = line.strip()
        if line_stripped.startswith("## "):
            if relative_filepath and code_lines and not skip_block_content:
                file_write_attempts += 1
                if write_code_to_file(abs_output_dir, relative_filepath, code_lines, encoding): created_files_count += 1
                else: errors.append(f"Failed write: {relative_filepath} (ended near line {line_num})")
            code_lines = []; relative_filepath = None; in_code_block = False; skip_block_content = False
            new_relative_filepath = line[3:].strip().strip('/').strip('\\')
            if not new_relative_filepath: errors.append(f"Warning: Found '##' header without a filepath on line {line_num}. Skipping.")
            else: relative_filepath = new_relative_filepath
        elif line_stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                if relative_filepath and code_lines and not skip_block_content:
                     file_write_attempts += 1
                     if write_code_to_file(abs_output_dir, relative_filepath, code_lines, encoding): created_files_count += 1
                     else: errors.append(f"Failed write: {relative_filepath} (block ended line {line_num})")
                elif skip_block_content: pass
                elif relative_filepath and not code_lines:
                    file_write_attempts += 1; print(f"[WARN] Empty code block for {relative_filepath} on line {line_num}. Creating empty file.")
                    if write_code_to_file(abs_output_dir, relative_filepath, [], encoding): created_files_count += 1
                    else: errors.append(f"Failed write (empty): {relative_filepath}")
                elif not relative_filepath and code_lines: errors.append(f"Warning: Code block found ending on line {line_num} without a preceding '## filepath' header. Content ignored.")
                code_lines = []; skip_block_content = False
            else: in_code_block = True; code_lines = []; skip_block_content = False
        elif in_code_block:
            if line_stripped.startswith("**Note:") or line_stripped.startswith("**Error reading file:") or line_stripped.startswith("**Binary File:"):
                 skip_block_content = True; print(f"[INFO] Skipping content block for {relative_filepath} due to marker: {line_stripped[:30]}...")
            if not skip_block_content: code_lines.append(line)
    if relative_filepath and code_lines and not skip_block_content:
        file_write_attempts += 1
        if write_code_to_file(abs_output_dir, relative_filepath, code_lines, encoding): created_files_count += 1
        else: errors.append(f"Failed write (end of file): {relative_filepath}")
    elif relative_filepath and skip_block_content: pass
    print("-" * 60); print(f"Codebase extraction finished."); print(f"  Attempted writes: {file_write_attempts}"); print(f"  Successfully created: {created_files_count} files")
    if errors: print(f"  Errors/Warnings: {len(errors)}"); [print(f"    - {err}") for err in errors]
    print("-" * 60)
    return True, created_files_count, errors


# --- Command Line Interface (Modified for Positional Args) ---
def main():
    parser = argparse.ArgumentParser(
        description="Standalone Codebase Snapshot Tool. Use 'fm <folder>' or 'mf <markdown_file>'.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python %(prog)s fm ./my_project -o project_snapshot.md
  python %(prog)s mf project_snapshot.md -o ./recreated_project"""
    )

    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands: fm, mf')

    # --- Sub-parser for fm (Folder to Markdown) ---
    parser_fm = subparsers.add_parser('fm', help='Create Markdown from Folder.')
    # Positional argument for input directory
    parser_fm.add_argument('input_directory', help='Path to the source code directory.')
    # Optional argument for output file
    parser_fm.add_argument('--output', '-o', required=True, dest='output_markdown', help='Path for the output Markdown snapshot file.')
    # Optional ignore patterns (remains the same)
    parser_fm.add_argument('--ignore', action='append', default=[], help='Additional ignore patterns (glob style). Can be used multiple times.')

    # --- Sub-parser for mf (Markdown to Folder) ---
    parser_mf = subparsers.add_parser('mf', help='Create Folder from Markdown.')
    # Positional argument for input markdown file
    parser_mf.add_argument('input_markdown', help='Path to the input Markdown snapshot file.')
    # Optional argument for output directory
    parser_mf.add_argument('--output', '-o', required=True, dest='output_directory', help='Path to the directory where the codebase will be recreated.')

    args = parser.parse_args()

    # --- Execute selected command ---
    if args.command == 'fm':
        print(f"Running: Folder to Markdown (fm)")
        success, processed, ignored, errors = create_codebase_snapshot(
            root_dir=args.input_directory,       # Use positional arg
            output_file=args.output_markdown,    # Use '-o' arg (renamed via dest)
            encoding=ENCODING,
            base_ignore_patterns=DEFAULT_IGNORE_PATTERNS,
            user_ignore_patterns=args.ignore
        )
        if success:
            print(f"\nSuccess! Snapshot created at: {args.output_markdown}")
            print(f"Processed {processed} files, ignored {ignored} items.")
            if errors: print(f"Completed with {len(errors)} errors/warnings during file processing.")
            sys.exit(0)
        else:
            print(f"\nFailed to create snapshot.", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'mf':
        print(f"Running: Markdown to Folder (mf)")
        success, created_count, errors = extract_codebase(
            md_file=args.input_markdown,       # Use positional arg
            output_dir=args.output_directory,  # Use '-o' arg (renamed via dest)
            encoding=ENCODING
        )
        if success:
             print(f"\nSuccess! Codebase extracted to: {args.output_directory}")
             print(f"Created {created_count} files.")
             if errors: print(f"Completed with {len(errors)} errors/warnings during file writing.")
             sys.exit(0)
        else:
            print(f"\nFailed to extract codebase.", file=sys.stderr)
            sys.exit(1)

# --- Main Execution Guard ---
if __name__ == '__main__':
    main()
```

## backend/main.py

```python
# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse # Or FileResponse
import uvicorn
import os
import sys
import json

# Add backend directory to sys.path to import mcp_client_logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mcp_client_logic import process_user_message_stream # We'll create this next

app = FastAPI()

# Mount static files (HTML, CSS, JS for frontend)
# Ensure this path is correct relative to where you run uvicorn
# If running uvicorn from chat_ui_project/, then 'static' is correct
app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    # Serve the main HTML page
    # For simplicity, reading it here. For complex apps, use FileResponse or templating.
    try:
        with open("../static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
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
```

## backend/mcp_client_logic.py

```python
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
```

## mcp/calculater_mcp.py

```python
# calculator_mcp_server_streamablehttp.py (Simplified run for Uvicorn defaults)
from mcp.server.fastmcp import FastMCP

# 1. Create an MCP server instance
mcp = FastMCP(
    name="CalculatorStreamableHttpServer",
    description="An MCP server using Streamable HTTP, providing basic arithmetic calculation tools.",
    stateless_http=True
)

# ... (TOOL DEFINITIONS - add, subtract, multiply, divide - same as before) ...
@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Adds two numbers together.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    """
    print(f"[Server Log StreamHTTP] Tool 'add' called with a={a}, b={b}")
    result = a + b
    print(f"[Server Log StreamHTTP] Tool 'add' result: {result}")
    return result
@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    Subtracts the second number from the first number.

    Args:
        a (float): The number to subtract from.
        b (float): The number to subtract.

    Returns:
        float: The result of a minus b.
    """
    print(f"[Server Log StreamHTTP] Tool 'subtract' called with a={a}, b={b}")
    result = a - b
    print(f"[Server Log StreamHTTP] Tool 'subtract' result: {result}")
    return result
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    print(f"[Server Log StreamHTTP] Tool 'multiply' called with a={a}, b={b}")
    result = a * b
    print(f"[Server Log StreamHTTP] Tool 'multiply' result: {result}")
    return result
@mcp.tool()
def divide(numerator: float, denominator: float) -> float | str:
    """
    Divides the numerator by the denominator.

    Args:
        numerator (float): The number to be divided.
        denominator (float): The number to divide by.

    Returns:
        float: The result of the division if denominator is not zero.
        str: An error message if denominator is zero.
    """
    print(f"[Server Log StreamHTTP] Tool 'divide' called with numerator={numerator}, denominator={denominator}")
    if denominator == 0:
        print("[Server Log StreamHTTP] Tool 'divide' error: Division by zero.")
        return "Error: Cannot divide by zero."
    result = numerator / denominator
    print(f"[Server Log StreamHTTP] Tool 'divide' result: {result}")
    return result

if __name__ == "__main__":
    print(f"Starting CalculatorStreamableHttpServer (FastMCP application defined).")
    print(f"When run with 'mcp run calculator_mcp_server_streamablehttp.py --transport streamable-http',")
    print(f"it will likely use Uvicorn's default host/port (e.g., 127.0.0.1:8000) or PORT/HOST env vars.")
    mcp.run(transport="streamable-http")
```

## static/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculon Chat</title>
    <link rel="stylesheet" href="/static/css/style.css"> <!-- We'll add Tailwind later -->
    <!-- Font Awesome (Get your kit code from fontawesome.com or use CDN) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        /* Basic temporary styles */
        body { font-family: sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }
        #chatContainer { max-width: 700px; margin: auto; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); overflow: hidden;}
        #messages { height: 400px; overflow-y: auto; padding: 20px; border-bottom: 1px solid #eee; }
        .message { margin-bottom: 15px; padding: 10px; border-radius: 6px; line-height: 1.4; }
        .user-message { background-color: #e1f5fe; text-align: right; margin-left: auto; max-width: 70%;}
        .ai-message { background-color: #f0f0f0; text-align: left; margin-right: auto; max-width: 70%;}
        .ai-message .sender { font-weight: bold; color: #555; display: block; margin-bottom: 5px;}
        .thought-message { background-color: #fff9c4; color: #777; font-style: italic; font-size: 0.9em; border-left: 3px solid #ffeb3b; padding-left: 10px; }
        .tool-call-message { background-color: #e8eaf6; color: #3f51b5; font-size: 0.9em; border-left: 3px solid #7986cb; padding-left: 10px; }
        .status-message { color: #888; font-style: italic; text-align: center; font-size: 0.9em; padding: 5px 0;}
        #inputArea { display: flex; padding: 10px; }
        #messageInput { flex-grow: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin-right: 10px;}
        #sendButton { padding: 10px 15px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        #sendButton:hover { background-color: #0056b3; }
        .message pre { white-space: pre-wrap; word-wrap: break-word; background: #2d2d2d; color: #f8f8f2; padding: 10px; border-radius: 5px; margin-top: 5px; }
    </style>
</head>
<body>
    <div id="chatContainer">
        <div id="messages">
            <!-- Messages will appear here -->
        </div>
        <div id="inputArea">
            <input type="text" id="messageInput" placeholder="Ask Calculon...">
            <button id="sendButton"><i class="fas fa-paper-plane"></i> Send</button>
        </div>
    </div>
    <script src="/static/js/app.js"></script>
</body>
</html>
```

## static/css/style.css

```css

```

## static/js/app.js

```javascript

document.addEventListener('DOMContentLoaded', () => { // Ensure DOM is loaded before accessing elements

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messagesDiv = document.getElementById('messages');
    let websocket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // Ensure this uses the host and port your FastAPI backend is running on.
        // If your FastAPI runs on 8001, window.location.host will be '127.0.0.1:8001' or 'localhost:8001'
        const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
        
        addMessageToDisplay('status', `Attempting to connect to ${wsUrl}...`);
        console.log(`Attempting to connect to WebSocket at ${wsUrl}`);
        websocket = new WebSocket(wsUrl);

        websocket.onopen = () => {
            addMessageToDisplay('status', 'Connected to Calculon\'s relay.');
            console.log('WebSocket connected');
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus(); // Focus on input field once connected
        };

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Received from WS:", data); // Log the raw data

            switch (data.type) {
                case 'text_chunk':
                    appendAiMessageChunk(data.content);
                    break;
                case 'thought':
                    addMessageToDisplay('thought', `${data.content}`); // Removed "Calculon's thought:" prefix here, as it's in the styling
                    startNewAiMessageIfNeeded(); 
                    break;
                case 'tool_call':
                    addMessageToDisplay('tool_call', `Wants to use tool: ${data.content.name} with args: ${JSON.stringify(data.content.args)}`);
                    startNewAiMessageIfNeeded();
                    break;
                case 'tool_response':
                    addMessageToDisplay('tool_call', `Tool ${data.content.name} responded.`); // Style as tool_call
                    startNewAiMessageIfNeeded();
                    break;
                case 'status':
                    addMessageToDisplay('status', data.content);
                    break;
                case 'mcp_tools':
                    // This is just an example of handling a custom message type
                    // addMessageToDisplay('status', `Available MCP Tools: ${data.content.join(', ')}`);
                    console.log(`Available MCP Tools from server: ${data.content.join(', ')}`);
                    break;
                case 'stream_end':
                    addMessageToDisplay('status', data.content);
                    currentAiMessageElement = null; // Reset for next AI message
                    messageInput.focus();
                    break;
                case 'error':
                    addMessageToDisplay('error', `Error from server: ${data.content}`, true);
                    currentAiMessageElement = null;
                    break;
                default:
                    console.warn('Unknown message type received:', data.type, data);
            }
        };

        websocket.onclose = (event) => {
            let reason = "";
            if (event.code) reason += `Code: ${event.code} `;
            if (event.reason) reason += `Reason: ${event.reason} `;
            if (event.wasClean) reason += `(Clean close) `; else reason += `(Unclean close) `;
            
            addMessageToDisplay('status', `Disconnected. ${reason}Attempting to reconnect...`, true);
            console.log(`WebSocket disconnected. ${reason}Attempting to reconnect...`);
            messageInput.disabled = true;
            sendButton.disabled = true;
            currentAiMessageElement = null;
            setTimeout(connectWebSocket, 3000); // Try to reconnect after 3 seconds
        };

        websocket.onerror = (error) => {
            // This event often fires just before onclose when there's a connection issue
            addMessageToDisplay('error', 'WebSocket connection error. Check console and server logs.', true);
            console.error('WebSocket error:', error);
            // onclose will likely handle disabling inputs and attempting reconnection
        };
    }

    let currentAiMessageElement = null;
    let currentAiTextContentDiv = null;

    function addMessageToDisplay(type, text, isError = false) {
        currentAiMessageElement = null; // New message, so not appending to previous AI
        currentAiTextContentDiv = null;

        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message-wrapper', `${type}-wrapper`); // For potential outer styling/flex alignment

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${type}-message`);
        
        let iconHtml = '';
        let senderText = '';

        switch (type) {
            case 'user':
                messageWrapper.classList.add('flex', 'justify-end');
                messageElement.classList.add('user-message'); // Tailwind: bg-blue-500 text-white
                messageElement.textContent = text;
                break;
            case 'thought':
                messageWrapper.classList.add('flex', 'justify-start');
                messageElement.classList.add('thought-message'); // Tailwind: bg-yellow-100 text-yellow-800 border-yellow-400
                iconHtml = '<i class="fas fa-brain fa-fw mr-2"></i>';
                senderText = 'Calculon\'s Internal Monologue';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                break;
            case 'tool_call':
                 messageWrapper.classList.add('flex', 'justify-start');
                messageElement.classList.add('tool-call-message'); // Tailwind: bg-indigo-100 text-indigo-800 border-indigo-400
                iconHtml = '<i class="fas fa-wrench fa-fw mr-2"></i>';
                senderText = 'Tool Interaction';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                break;
            case 'status':
                messageWrapper.classList.add('status-wrapper'); // No flex by default for status
                messageElement.classList.add('status-message'); // Tailwind: text-gray-500 italic text-center text-sm
                messageElement.textContent = text;
                break;
            case 'error':
                messageWrapper.classList.add('flex', 'justify-start'); // Or center, depending on desired error appearance
                messageElement.classList.add('error-message'); // Tailwind: bg-red-100 text-red-700 border-red-400
                iconHtml = '<i class="fas fa-exclamation-triangle fa-fw mr-2"></i>';
                senderText = 'System Error';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                break;
            // AI text chunks are handled by startNewAiMessageIfNeeded and appendAiMessageChunk
        }
        
        if (type !== 'text_chunk') { // text_chunk is handled differently
            messageWrapper.appendChild(messageElement);
            messagesDiv.appendChild(messageWrapper);
        }
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function startNewAiMessageIfNeeded() {
        // This function ensures that thoughts or tool calls create a new bubble
        // before any subsequent AI text starts appending to a new text bubble.
        if (currentAiMessageElement) { // If there was an AI text bubble being appended to
            currentAiMessageElement = null; // Force a new one for the next text_chunk
            currentAiTextContentDiv = null;
        }
    }

    function ensureAiMessageBubbleExists() {
        if (!currentAiMessageElement) {
            const messageWrapper = document.createElement('div');
            messageWrapper.classList.add('message-wrapper', 'ai-wrapper', 'flex', 'justify-start');

            currentAiMessageElement = document.createElement('div');
            currentAiMessageElement.classList.add('message', 'ai-message'); // Tailwind: bg-gray-200 text-gray-800
            
            const senderSpan = document.createElement('span');
            senderSpan.classList.add('sender', 'block', 'font-semibold', 'mb-1'); // Tailwind classes
            senderSpan.innerHTML = '<i class="fas fa-robot fa-fw mr-2"></i>Calculon';
            currentAiMessageElement.appendChild(senderSpan);

            currentAiTextContentDiv = document.createElement('div');
            currentAiTextContentDiv.classList.add('ai-text-content');
            currentAiMessageElement.appendChild(currentAiTextContentDiv);
            
            messageWrapper.appendChild(currentAiMessageElement);
            messagesDiv.appendChild(messageWrapper);
        }
    }

    function appendAiMessageChunk(textChunk) {
        ensureAiMessageBubbleExists(); // Make sure we have an AI message bubble
        if (currentAiTextContentDiv) {
            // Append formatted text. `escapeHtmlAndPreserveFormatting` handles <br> for newlines.
            currentAiTextContentDiv.innerHTML += escapeHtmlAndPreserveFormatting(textChunk);
        }
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function escapeHtml(unsafe) {
        if (unsafe === null || typeof unsafe === 'undefined') return '';
        return unsafe
             .toString()
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    function escapeHtmlAndPreserveFormatting(unsafe) {
        let escaped = escapeHtml(unsafe);
        escaped = escaped.replace(/\n/g, '<br>');
        // Basic Markdown-like code block handling (can be improved)
        escaped = escaped.replace(/```([\s\S]*?)```/g, (match, codeContent) => {
            // For code within pre, we need to escape HTML entities that might be in the code itself
            return `<pre class="bg-gray-800 text-white p-2 rounded overflow-x-auto text-sm"><code>${escapeHtml(codeContent.trim())}</code></pre>`;
        });
         // Basic bold and italic
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        escaped = escaped.replace(/\*(.*?)\*/g, '<em>$1</em>');
        return escaped;
    }

    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText && websocket && websocket.readyState === WebSocket.OPEN) {
            addMessageToDisplay('user', messageText);
            console.log('Sending message via WebSocket:', messageText);
            websocket.send(JSON.stringify({ message: messageText }));
            messageInput.value = '';
            // currentAiMessageElement = null; // Reset for next AI message. Done in addMessageToDisplay.
        } else if (!messageText) {
            console.log("Empty message, not sending.");
        } else {
            console.error('Cannot send message. WebSocket state:', websocket ? websocket.readyState : 'WebSocket not initialized', websocket);
            addMessageToDisplay('error', 'Not connected to server. Cannot send message.', true);
        }
    }

    // Event Listeners
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    } else {
        console.error("Send button not found!");
    }

    if (messageInput) {
        messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) { // Send on Enter, allow Shift+Enter for newline
                event.preventDefault(); // Prevent default Enter behavior (like form submission)
                sendMessage();
            }
        });
    } else {
        console.error("Message input not found!");
    }

    // Initialize: Disable inputs and attempt to connect
    if (messageInput) messageInput.disabled = true;
    if (sendButton) sendButton.disabled = true;
    
    connectWebSocket();

}); // End of DOMContentLoaded
```

