from fastapi import FastAPI
from .routes import router

app = FastAPI(title="MCP Server", description="A simple, extensible MCP server for agent development.")

app.include_router(router)
