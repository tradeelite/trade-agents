"""Sub-agent: fundamental analysis specialist."""

from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

from trade_agent import prompt

MODEL = "gemini-2.0-flash"

_DESCRIPTION = (
    "Performs deep fundamental analysis of stocks including valuation metrics (P/E, PEG, P/B), "
    "financial health (debt ratios, margins, ROE), growth metrics, analyst consensus ratings, "
    "and earnings history trends."
)

# Use GoogleSearchTool only — MCP SSE fails with HTTP/2 on Cloud Run (421)
fundamental_analyst = LlmAgent(
    model=MODEL,
    name="fundamental_analyst",
    description=_DESCRIPTION,
    instruction=prompt.FUNDAMENTAL_ANALYST_PROMPT,
    output_key="fundamental_analysis_output",
    tools=[GoogleSearchTool()],
)
