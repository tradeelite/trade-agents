"""Sub-agent: options position analysis."""

from google.adk.agents import LlmAgent

from trade_agent import prompt
from trade_agent.tools import get_mcp_tools

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
    tools=[get_mcp_tools()],
)
