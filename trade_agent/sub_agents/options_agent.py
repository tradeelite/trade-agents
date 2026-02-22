"""Sub-agent: options position analysis."""

from google.adk.agents import LlmAgent

from trade_agent import prompt
from trade_agent.tools import (
    get_options_trades,
    get_options_suggestions,
    get_stock_quote,
)

MODEL = "gemini-2.0-flash"

options_agent = LlmAgent(
    model=MODEL,
    name="options_agent",
    description=(
        "Reviews open and closed options positions, calculates P&L, "
        "identifies DTE urgency, assignment risk, earnings conflicts, "
        "and recommends actions based on trading rules."
    ),
    instruction=prompt.OPTIONS_AGENT_PROMPT,
    output_key="options_analysis_output",
    tools=[get_options_trades, get_options_suggestions, get_stock_quote],
)
