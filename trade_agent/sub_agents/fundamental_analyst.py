"""Sub-agent: fundamental analysis specialist."""

from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

from trade_agent import prompt
from trade_agent.tools import get_mcp_tools

MODEL = "gemini-2.0-flash"

fundamental_analyst = LlmAgent(
    model=MODEL,
    name="fundamental_analyst",
    description=(
        "Performs deep fundamental analysis of stocks including valuation metrics (P/E, PEG, P/B), "
        "financial health (debt ratios, margins, ROE), growth metrics, analyst consensus ratings, "
        "and earnings history trends."
    ),
    instruction=prompt.FUNDAMENTAL_ANALYST_PROMPT,
    output_key="fundamental_analysis_output",
    tools=[get_mcp_tools(), GoogleSearchTool()],
)
