"""Sub-agent: portfolio analysis."""

from google.adk.agents import LlmAgent

from trade_agent import prompt
from trade_agent.tools import get_portfolios, get_portfolio_holdings, get_stock_quote

MODEL = "gemini-2.0-flash"

portfolio_agent = LlmAgent(
    model=MODEL,
    name="portfolio_agent",
    description=(
        "Analyzes investment portfolio holdings, calculates live valuations, "
        "identifies top positions, concentration risk, and overall performance."
    ),
    instruction=prompt.PORTFOLIO_AGENT_PROMPT,
    output_key="portfolio_analysis_output",
    tools=[get_portfolios, get_portfolio_holdings, get_stock_quote],
)
