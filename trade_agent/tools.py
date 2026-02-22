"""MCP toolset — connects trade-agents to trade-backend via MCP over SSE."""

import os

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from dotenv import load_dotenv

load_dotenv()

_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_mcp_tools() -> MCPToolset:
    """Return an MCPToolset connected to the trade-backend MCP server."""
    return MCPToolset(
        connection_params=SseServerParams(
            url=f"{_BACKEND_URL}/mcp/sse",
        )
    )
