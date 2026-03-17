# CLAUDE.md — trade-agent

## Summary
Google ADK multi-agent system powering TradeElite AI capabilities.

## Active Agents
- `portfolio_agent`
- `options_agent`
- `market_agent`
- `stock_analyst` (orchestrates technical/fundamental/news)
- `technical_analyst`
- `fundamental_analyst` (sub-agent of stock_analyst)
- `fundamental_analyst_direct` (direct sub-agent of root_agent, used by /fundamental-analysis endpoint)
- `news_analyst`

## Prompt Direction

- `FUNDAMENTAL_ANALYST_PROMPT` targets rich schema: header, valuation, profitability, financialHealth, growth, earnings, dividends, verdict, keyRisk, intro, summary, sources.
- `ORCHESTRATOR_PROMPT` routes "fundamental analysis" requests to `fundamental_analyst_direct` (bypasses stock_analyst).
- `STOCK_ANALYST_PROMPT` updated to reference new rich fundamental schema fields.

## Deployment
`deployment/deploy.py --create` deploys a new reasoning engine revision.
Backend selects active revision via `TRADEVIEW_AGENT_RESOURCE_ID`.
