# MCP Server

A simple, extensible Model Context Protocol (MCP) server in Python for agent development learning. No authentication required initially. Designed to be easy to extend and well-documented for others to use as a base for their own agent projects.


## Features
- MCP-compliant tool registry and invocation
- Simple REST API for agent communication
- Extensible architecture for adding new tools and logic
- No authentication required (can be added later)
- Well-documented and easy to understand

## Getting Started

### Requirements
- Python 3.8+
- pip

### Installation
1. Clone this repository or copy the project files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Project Structure
- `app/` - Main application code
- `tests/` - Unit and integration tests
- `.github/` - Project instructions and automation

## MCP Tools API

This server exposes tools as per the Model Context Protocol (MCP):

- `GET /tools` — List all available tools and their schemas.
- `POST /invoke` — Invoke a tool by name with arguments.

### Example: List Tools
```bash
curl http://localhost:8000/tools
```

### Example: Invoke OpenAI Chat Tool
```bash
curl -X POST http://localhost:8000/invoke -H "Content-Type: application/json" -d '{"tool": "openai_chat", "arguments": {"prompt": "Hello, who are you?"}}'
```


### Available Tools

- **openai_chat**: Send a prompt to OpenAI and get a response.
   - Parameters:
      - `prompt` (string): Prompt for the LLM.

- **wikipedia_person**: Fetch summary info about a person from Wikipedia.
   - Parameters:
      - `name` (string): Full name of the person.

#### Example: Invoke Wikipedia Person Tool
```bash
curl -X POST http://localhost:8000/invoke -H "Content-Type: application/json" -d '{"tool": "wikipedia_person", "arguments": {"name": "Albert Einstein"}}'
```

## Extending the Server
- Add new tools in `app/routes.py` or create new modules in `app/`.
- Register tools with a name, description, parameters, and function.
- Follow the examples and docstrings for guidance.

## License
MIT
