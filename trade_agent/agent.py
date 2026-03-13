"""Trade Agent: root orchestrator agent for TradeView."""

from google.adk.agents import LlmAgent

from trade_agent import prompt
from trade_agent.sub_agents import market_agent, options_agent, portfolio_agent, stock_analyst

MODEL = "gemini-2.0-flash"

trade_orchestrator = LlmAgent(
    model=MODEL,
    name="trade_orchestrator",
    description=(
        "AI-powered trading assistant for TradeView. Routes requests to specialist "
        "sub-agents for portfolio analysis, options position review, market research, "
        "and comprehensive stock analysis."
    ),
    instruction=prompt.ORCHESTRATOR_PROMPT,
    sub_agents=[portfolio_agent, options_agent, market_agent, stock_analyst],
)

root_agent = trade_orchestrator
