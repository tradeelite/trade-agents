"""MCP toolset — connects trade-agents to trade-backend via MCP over SSE."""

import os

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
from dotenv import load_dotenv

load_dotenv()

_BACKEND_URL = os.getenv("BACKEND_URL", "https://trade-backend-685436576212.us-central1.run.app")


class _DeployableMCPToolset(MCPToolset):
    """MCPToolset subclass that supports deep-copy for Vertex AI deployment."""

    def __deepcopy__(self, memo: dict):
        # Recreate from config-only attributes — avoids pickling open file handles
        return _DeployableMCPToolset(
            connection_params=self._connection_params,
            tool_filter=self.tool_filter,
            tool_name_prefix=self.tool_name_prefix,
        )


def get_mcp_tools() -> _DeployableMCPToolset:
    """Return an MCPToolset connected to the trade-backend MCP server."""
    return _DeployableMCPToolset(
        connection_params=SseConnectionParams(
            url=f"{_BACKEND_URL}/mcp/sse",
        )
    )
