"""Sub-agent: deep technical analysis specialist."""

from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

from trade_agent import prompt
from trade_agent.tools import get_mcp_tools

MODEL = "gemini-2.0-flash"

technical_analyst = LlmAgent(
    model=MODEL,
    name="technical_analyst",
    description=(
        "Performs deep technical analysis of stocks including trend direction and strength, "
        "momentum signals (RSI, MACD, Bollinger Bands), volume analysis, support/resistance "
        "levels, and short/medium/long-term directional signals."
    ),
    instruction=prompt.TECHNICAL_ANALYST_PROMPT,
    output_key="technical_analysis_output",
    tools=[get_mcp_tools(), GoogleSearchTool()],
)
