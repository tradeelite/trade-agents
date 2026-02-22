# CLAUDE.md — trade-agent Project Context

## Project Summary

`trade-agent` is a Google ADK multi-agent system that provides AI-powered trading intelligence for the TradeView dashboard. It connects to the TradeView Next.js app via HTTP and provides three specialist sub-agents: portfolio analysis, options position review, and market research.

## Tech Stack

- **Framework:** Google ADK (`google-adk >= 1.0.0`)
- **Model:** `gemini-2.0-flash`
- **Deployment:** Vertex AI Agent Engine (`google-cloud-aiplatform[adk,agent-engines]`)
- **HTTP client:** `httpx` (calls TradeView API)
- **Package manager:** `uv`
- **Python:** 3.11–3.12

## Project Structure

```
trade-agent/
├── trade_agent/
│   ├── __init__.py          # GCP env setup + google.auth.default()
│   ├── agent.py             # Root orchestrator agent (root_agent)
│   ├── prompt.py            # System prompts for all agents
│   ├── tools.py             # Functions that call TradeView API
│   └── sub_agents/
│       ├── __init__.py
│       ├── portfolio_agent.py   # Portfolio analysis
│       ├── options_agent.py     # Options position review
│       └── market_agent.py      # Market research (news, sentiment, technicals)
├── deployment/
│   ├── deploy.py            # Create/delete/list agents on Vertex AI
│   └── test_deployment.py   # Interactive test against deployed agent
├── tests/
│   └── test_agents.py       # Unit tests using InMemoryRunner
├── eval/
│   ├── test_eval.py         # ADK evaluation suite
│   └── data/
│       └── trade-agent.test.json
├── pyproject.toml
├── .env.example
└── .gitignore
```

## Agent Architecture

```
root_agent (trade_orchestrator)
├── portfolio_agent     ← get_portfolios, get_portfolio_holdings, get_stock_quote
├── options_agent       ← get_options_trades, get_options_suggestions, get_stock_quote
└── market_agent        ← get_stock_quote, get_stock_news, get_stock_sentiment,
                           get_technical_indicators, get_company_info, GoogleSearchTool
```

## Environment Variables

```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-staging-bucket
TRADEVIEW_API_URL=http://localhost:3000   # URL of running TradeView app
```

## Common Commands

```bash
# Setup
cp .env.example .env        # Fill in your GCP project details
uv sync                     # Install dependencies
uv sync --group dev         # Install with dev tools

# Local development
adk run trade_agent                        # Run agent in CLI
adk web trade_agent                        # Run with local web UI
adk api_server trade_agent                 # Run as HTTP API server

# Tests
uv run pytest tests/                       # Unit tests
uv run pytest eval/                        # Evaluation suite

# Deployment
uv sync --group deployment
uv run python deployment/deploy.py --create                         # Deploy to Vertex AI
uv run python deployment/deploy.py --list                           # List deployed agents
uv run python deployment/deploy.py --delete --resource_id=RESOURCE  # Delete agent

# Test deployed agent
uv run python deployment/test_deployment.py \
  --resource_id=projects/.../reasoningEngines/... \
  --user_id=test-user
```

## TradeView API Tools

| Tool | Endpoint | Purpose |
|------|----------|---------|
| `get_portfolios()` | `GET /api/portfolios` | All portfolios |
| `get_portfolio_holdings(id)` | `GET /api/portfolios/{id}/holdings` | Holdings with live prices |
| `get_stock_quote(ticker)` | `GET /api/stocks/{ticker}/quote` | Real-time quote |
| `get_stock_news(ticker)` | `GET /api/stocks/{ticker}/news` | Latest news |
| `get_stock_sentiment(ticker)` | `GET /api/stocks/{ticker}/sentiment` | StockTwits sentiment |
| `get_technical_indicators(ticker, range)` | `GET /api/stocks/{ticker}/indicators` | RSI, MACD, SMA, BB |
| `get_company_info(ticker)` | `GET /api/stocks/{ticker}/summary` | Company details |
| `get_options_trades(status)` | `GET /api/options?status=` | Options positions |
| `get_options_suggestions()` | `GET /api/options/suggestions` | Rule-based suggestions |

## Key Implementation Notes

- `root_agent` in `agent.py` is the entrypoint — ADK and Vertex AI Agent Engine look for this
- `__init__.py` loads GCP credentials via `google.auth.default()` — ensure `gcloud auth login` is run locally
- `TRADEVIEW_API_URL` must point to a running TradeView instance; locally use `http://localhost:3000`
- Tools are plain Python functions — ADK auto-generates the schema from type hints and docstrings
- All agents return structured JSON enforced by their system prompts
- The orchestrator uses `sub_agents=[]` to delegate — ADK handles routing automatically
