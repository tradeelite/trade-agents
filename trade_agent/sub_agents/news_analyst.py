"""Sub-agent: news and sentiment analyst."""

from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

from trade_agent import prompt
from trade_agent.tools import get_mcp_tools

MODEL = "gemini-2.0-flash"

news_analyst = LlmAgent(
    model=MODEL,
    name="news_analyst",
    description=(
        "Analyzes news and social sentiment for stocks including StockTwits sentiment, "
        "news article sentiment, key catalysts, risks, recent headlines, and overall "
        "bullish/bearish/neutral sentiment signal."
    ),
    instruction=prompt.NEWS_ANALYST_PROMPT,
    output_key="news_analysis_output",
    tools=[get_mcp_tools(), GoogleSearchTool()],
)
