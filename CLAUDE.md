# CLAUDE.md — trade-agent

## Summary
Google ADK multi-agent system powering TradeElite AI capabilities.

## Active Agents
- `portfolio_agent`
- `options_agent`
- `market_agent`
- `stock_analyst` (orchestrates technical/fundamental/news)
- `technical_analyst`
- `fundamental_analyst`
- `news_analyst`

## Prompt Direction

- `FUNDAMENTAL_ANALYST_PROMPT` targets rich attribute-level schema for dedicated fundamental analysis.
- `STOCK_ANALYST_PROMPT` must remain compatible with production orchestrator reliability requirements.

## Deployment
`deployment/deploy.py --create` deploys a new reasoning engine revision.
Backend selects active revision via `TRADEVIEW_AGENT_RESOURCE_ID`.
