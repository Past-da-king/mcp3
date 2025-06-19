# Calculon: AI Math Chatbot with MCP Tool Integration

Calculon is a web-based AI chatbot that specializes in mathematical calculations. It leverages Google's Gemini AI and a custom MCP (Modular Calculation Protocol) server to perform arithmetic operations using defined tools, ensuring all calculations are delegated to the backend for accuracy and transparency.

## Features

| Feature                   | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| Conversational Math AI    | Interact with "Calculon," an AI mathematician.                              |
| MCP Tool Integration      | Arithmetic performed by backend tools for accuracy.                         |
| Extended Math Tools       | Includes `power`, `sqrt`, `get_constant` in addition to basic arithmetic.   |
| Streaming Responses       | Real-time display of AI thoughts, tool calls, and results.                  |
| WebSocket Communication   | Fast, interactive chat experience.                                          |
| Chat History              | Saves conversation in browser; persists across sessions.                    |
| Clear Chat                | Button to clear displayed messages and stored history.                      |
| Simple Frontend           | HTML/CSS/JS interface (no heavy frameworks).                                |
| FastAPI Backend           | Connects frontend, Gemini AI, and MCP server.                               |
| Codebase Snapshot Utility | `ss.py` tool for creating and restoring project snapshots.                  |

- **Conversational Math Chatbot:** Interact with "Calculon," an AI mathematician with a personality, via a web chat interface.
- **MCP Tool Integration:** All arithmetic is performed using backend tools, not by the AI directly. This ensures accuracy and transparency in calculations.
- **Streaming Responses:** Real-time, chunked responses including AI thoughts, tool calls, and final results are streamed to the frontend.
- **WebSocket Communication:** Enables a fast and interactive chat experience.
- **Simple Frontend:** Built with plain HTML, CSS, and JavaScript, requiring no complex framework installations.
- **FastAPI Backend:** Efficiently handles communication between the frontend, Gemini AI, and the MCP server.

### Chat Interface Features
- **Chat History:** Conversations with Calculon are automatically saved in your browser's `localStorage`. This means your chat history will persist even if you reload the page or close and reopen your browser.
- **Clear Chat:** A "Clear Chat" button ( <i class="fas fa-trash"></i> icon) is available to remove all messages from the current display and simultaneously erase the stored chat history from `localStorage`.

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

### Calculator Tools
Calculon has access to the following mathematical tools via the MCP server:
- `add(a, b)`: Adds two numbers.
  - *Example Query:* "User: What is 123 + 456?"
- `subtract(a, b)`: Subtracts the second number from the first.
  - *Example Query:* "User: What is 100 - 33?"
- `multiply(a, b)`: Multiplies two numbers.
  - *Example Query:* "User: What is 15 * 10?"
- `divide(numerator, denominator)`: Divides two numbers. It includes error handling for division by zero.
  - *Example Query:* "User: What is 100 / 4?"
- `power(base, exponent)`: Calculates `base` raised to the `exponent`.
  - *Example Query:* "User: What is 5 to the power of 3?"
- `sqrt(number)`: Calculates the square root of `number`. Returns an error for negative inputs.
  - *Example Query:* "User: What is the square root of 144?"
- `get_constant(name)`: Retrieves mathematical constants. Currently supports "pi" and "e".
  - *Example Query:* "User: What is the value of pi?"
- `sin(angle, unit="radians")`: Calculates the sine of an angle.
  - The `unit` parameter can be "radians" (default) or "degrees".
  - *Example Query:* "User: What is the sine of 90 degrees?"
- `cos(angle, unit="radians")`: Calculates the cosine of an angle.
  - The `unit` parameter can be "radians" (default) or "degrees".
  - *Example Query:* "User: Calculate cos(pi/2 radians)."
- `tan(angle, unit="radians")`: Calculates the tangent of an angle.
  - The `unit` parameter can be "radians" (default) or "degrees".
  - *Example Query:* "User: Find the tangent of 45 degrees."
- `asin_op(value, unit="radians")`: Calculates the arcsine (inverse sine) of a value.
  - The input `value` must be between -1 and 1, inclusive.
  - The `unit` parameter specifies the result's unit ("radians" or "degrees").
  - *Example Query:* "User: What is asin_op(0.5) in degrees?"
- `acos_op(value, unit="radians")`: Calculates the arccosine (inverse cosine) of a value.
  - The input `value` must be between -1 and 1, inclusive.
  - The `unit` parameter specifies the result's unit ("radians" or "degrees").
  - *Example Query:* "User: Give me acos_op(-1) in degrees."
- `atan_op(value, unit="radians")`: Calculates the arctangent (inverse tangent) of a value.
  - The `unit` parameter specifies the result's unit ("radians" or "degrees").
  - *Example Query:* "User: atan_op(1) in radians please."

## Setup & Running

### Prerequisites

- Python 3.10+
- Node.js (optional, for frontend development)
- [Google Gemini API key](https://ai.google.dev/)
- MCP Python package (and dependencies)

### 1. Install Python Dependencies

Ensure you have Python 3.10 or newer.
```sh
pip install fastapi uvicorn python-dotenv google-generativeai mcp httpx websockets
```
(Note: `httpx` and `websockets` are often dependencies of `fastapi` and `uvicorn` or `mcp`, but listing them explicitly can be helpful.)

### 2. Configure Environment

Create a `.env` file in the project root:

```
GEMINI_API_KEY="your-gemini-api-key"
MCP_SERVER_URL=http://127.0.0.1:8000/mcp
```


## Running the Project

Open two terminals and run the following commands:

**1. Start the backend server (FastAPI + WebSocket):**
Navigate to the `backend` directory:
```sh
cd backend
uvicorn main:app --reload --port 8001
```
(If `main.py` is in the root, run from the root directory: `uvicorn backend.main:app --reload --port 8001`)

**2. Start the MCP calculator server:**
Navigate to the `mcp` directory (or project root if `calculater_mcp.py` is there and paths are adjusted):
```sh
cd mcp
# If calculater_mcp.py is in the root, adjust path or run from root
mcp run calculater_mcp.py --transport streamable-http
# This typically defaults to port 8000. Ensure MCP_SERVER_URL in .env matches.
```

Then, open [http://localhost:8001/](http://localhost:8001/) in your browser to use the chat interface.

## Usage

- Type a math question (e.g., "What is (5 + 3) * 2?") and send.
- Calculon will explain each step, call the appropriate tool, and show the result.

## Codebase Snapshot Tool (`ss.py`)

The `ss.py` script is a utility for creating a single Markdown file that encapsulates the entire project's codebase (excluding specified ignored files/directories). It can also reconstruct the project from such a Markdown file. This is particularly useful for sharing the exact state of the codebase, for archival purposes, or for contexts where transferring multiple files is inconvenient.

**Key Features:**
- Converts project files into a structured Markdown format.
- Recreates the project directory and files from the Markdown snapshot.
- Allows specifying ignored files and directories (defaults in `ss_config.json`).

**Usage Examples:**

- **Create a snapshot:**
  To create a snapshot of the current directory (`./`) and save it as `snapshot.md`:
  ```sh
  python ss.py fm ./ -o snapshot.md
  ```

- **Recreate from a snapshot:**
  To recreate the project from `snapshot.md` into a new directory named `recreated_project`:
  ```sh
  python ss.py mf snapshot.md -o ./recreated_project
  ```

Make sure `ss_config.json` is configured if you have specific files or directories (like `.env`, `__pycache__`, etc.) you wish to exclude from snapshots.

## License

MIT License

---

**Note:** This project is for educational/demo purposes. Do not expose your API keys in production environments.