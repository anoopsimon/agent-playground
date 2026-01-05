import requests
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, Callable
from .llm_openai import query_openai

router = APIRouter()

# --- Tool registry ---
class Tool:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any], func: Callable):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.func = func

tool_registry = {}

def register_tool(tool: Tool):
    tool_registry[tool.name] = tool

# Example tool: OpenAI chat
# Example tool: OpenAI chat
def openai_chat_tool(prompt: str) -> str:
    return query_openai(prompt)

# New tool: Wikipedia person info
def wikipedia_person_tool(name: str) -> str:
    """Fetch summary info about a person from Wikipedia."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name.replace(' ', '_')}"
    headers = {"User-Agent": "agent-101-mcp-server/1.0 (https://github.com/your-repo)"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("extract", "No summary available.")
    elif resp.status_code == 404:
        return "No Wikipedia page found for this person."
    else:
        return f"Wikipedia API error: {resp.status_code}"

register_tool(Tool(
    name="openai_chat",
    description="Send a prompt to OpenAI and get a response.",
    parameters={"prompt": {"type": "string", "description": "Prompt for the LLM."}},
    func=openai_chat_tool
))

register_tool(Tool(
    name="wikipedia_person",
    description="Fetch summary info about a person from Wikipedia.",
    parameters={"name": {"type": "string", "description": "Full name of the person."}},
    func=wikipedia_person_tool
))

# --- API endpoints ---
@router.get("/")
def root():
    return {"message": "MCP Server is running."}

@router.get("/tools")
def list_tools():
    """List all available tools and their schemas."""
    return {
        "tools": [
            {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters
            } for t in tool_registry.values()
        ]
    }

class ToolInvokeRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any]

@router.post("/invoke")
def invoke_tool(req: ToolInvokeRequest):
    tool = tool_registry.get(req.tool)
    if not tool:
        return JSONResponse(status_code=404, content={"error": f"Tool '{req.tool}' not found."})
    try:
        result = tool.func(**req.arguments)
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
