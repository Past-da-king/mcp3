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