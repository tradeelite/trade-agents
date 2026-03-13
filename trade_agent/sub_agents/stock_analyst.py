"""Sub-agent: master stock analysis orchestrator."""

from google.adk.agents import LlmAgent

from trade_agent import prompt
from trade_agent.sub_agents.technical_analyst import technical_analyst
from trade_agent.sub_agents.fundamental_analyst import fundamental_analyst
from trade_agent.sub_agents.news_analyst import news_analyst

MODEL = "gemini-2.0-flash"

stock_analyst = LlmAgent(
    model=MODEL,
    name="stock_analyst",
    description=(
        "Comprehensive stock analysis orchestrator. Delegates to technical_analyst, "
        "fundamental_analyst, and news_analyst sub-agents, then synthesizes all three "
        "into a unified structured JSON with overall signal, recommendation, and confidence."
    ),
    instruction=prompt.STOCK_ANALYST_PROMPT,
    output_key="stock_analysis_output",
    sub_agents=[technical_analyst, fundamental_analyst, news_analyst],
)
