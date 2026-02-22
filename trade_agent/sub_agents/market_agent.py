"""Sub-agent: market research for individual stocks."""

from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

from trade_agent import prompt
from trade_agent.tools import (
    get_stock_quote,
    get_stock_news,
    get_stock_sentiment,
    get_technical_indicators,
    get_company_info,
)

MODEL = "gemini-2.0-flash"

market_agent = LlmAgent(
    model=MODEL,
    name="market_agent",
    description=(
        "Researches any stock or ETF using live price data, recent news, "
        "StockTwits social sentiment, and technical indicators (RSI, MACD, "
        "Bollinger Bands). Returns a comprehensive bullish/bearish signal."
    ),
    instruction=prompt.MARKET_AGENT_PROMPT,
    output_key="market_research_output",
    tools=[
        get_stock_quote,
        get_stock_news,
        get_stock_sentiment,
        get_technical_indicators,
        get_company_info,
        GoogleSearchTool(),
    ],
)
