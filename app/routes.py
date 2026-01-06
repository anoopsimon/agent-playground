
import os
import requests
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, Callable
from .llm_openai import query_openai


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

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

# New tool: Brave web search
def brave_search_tool(query: str, count: int = 5) -> Dict[str, Any]:
    """Search the web using Brave Search API."""
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        raise ValueError("BRAVE_API_KEY is not set.")
    params = {"q": query, "count": count}
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
        "User-Agent": "agent-101-mcp-server/1.0 (https://github.com/your-repo)"
    }
    resp = requests.get("https://api.search.brave.com/res/v1/web/search", params=params, headers=headers)
    if resp.status_code != 200:
        return {"error": f"Brave Search API error: {resp.status_code}", "details": resp.text}
    data = resp.json()
    results = []
    for item in data.get("web", {}).get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "snippet": item.get("description")
        })
    return {"results": results}

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

register_tool(Tool(
    name="brave_search",
    description="Search the web using Brave Search API.",
    parameters={
        "query": {"type": "string", "description": "Search query."},
        "count": {"type": "integer", "description": "Number of results to return.", "default": 5}
    },
    func=brave_search_tool
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
    logger.info(f"/invoke called with tool: {req.tool}, arguments: {req.arguments}")
    tool = tool_registry.get(req.tool)
    if not tool:
        logger.warning(f"Tool '{req.tool}' not found.")
        return JSONResponse(status_code=404, content={"error": f"Tool '{req.tool}' not found."})
    try:
        result = tool.func(**req.arguments)
        logger.info(f"Tool '{req.tool}' executed successfully.")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error invoking tool '{req.tool}': {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
