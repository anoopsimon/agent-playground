
# MCP Server

Minimal Python MCP server for tool invocation and agent prototyping.

## About

This server exposes a simple REST API for listing tools and invoking them with JSON arguments. It is designed for quick experiments and easy extension.

## Tools

Only the following tools are included by default:

- `brave_search` — Web search using the Brave Search API.
- `wikipedia_person` — Summary info about a person from Wikipedia.

## How to Use

### Install and Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### List Tools

```bash
curl http://localhost:8000/tools
```

### Sample API Calls

Wikipedia person search:
```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool": "wikipedia_person", "arguments": {"name": "Albert Einstein"}}'
```

Brave web search (requires `BRAVE_API_KEY` in `.env`):
```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool": "brave_search", "arguments": {"query": "FastAPI MCP server", "count": 5}}'
```

## How to Add a New Tool

1. Create a new tool function in `app/routes.py`.
2. Register it in the tool registry using `register_tool(...)`.
3. Define its `name`, `description`, and JSON `parameters`.
4. Restart the server and confirm it appears in `GET /tools`.

## Contributions Welcome

Issues and PRs are welcome. If you add a new tool, include a short description and a curl example in this README.

## License
MIT
