# trade-agent

AI-powered trading assistant built with **Google ADK** (Agent Development Kit). Provides intelligent analysis of portfolios, options positions, and market data by connecting to the [TradeView](../trade) dashboard's API.

## Architecture

Three specialist sub-agents orchestrated by a root agent:

```
trade_orchestrator
├── portfolio_agent   — Portfolio holdings, valuations, P&L, concentration risk
├── options_agent     — Open positions, DTE urgency, assignment risk, suggestions
└── market_agent      — Stock quotes, news, StockTwits sentiment, technical indicators
```

Each sub-agent has dedicated tools that call the TradeView API, plus `market_agent` uses `GoogleSearchTool` for broader research.

## Requirements

- Python 3.11–3.12
- [uv](https://docs.astral.sh/uv/) package manager
- GCP project with Vertex AI and Agent Engine APIs enabled
- TradeView app running (local or deployed)

## Setup

```bash
# 1. Copy env file and fill in your values
cp .env.example .env

# 2. Authenticate with GCP
gcloud auth application-default login

# 3. Install dependencies
uv sync
```

### `.env` variables

```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-staging-bucket
TRADEVIEW_API_URL=http://localhost:3000
```

## Local Development

Make sure TradeView is running on `http://localhost:3000` first.

```bash
# Interactive CLI
adk run trade_agent

# Local web UI (chat interface at http://localhost:8000)
adk web trade_agent

# HTTP API server
adk api_server trade_agent
```

### Example queries to try

- `How is my portfolio doing?`
- `Any urgent options actions I need to take?`
- `Give me a full analysis of AAPL`
- `What's the StockTwits sentiment on NVDA?`
- `Should I roll my expiring positions?`

## Running Tests

```bash
uv sync --group dev

# Unit tests (uses InMemoryRunner — requires live TradeView + Vertex AI)
uv run pytest tests/ -v

# Evaluation suite
uv run pytest eval/ -v
```

## Deployment to Vertex AI Agent Engine

```bash
uv sync --group deployment

# Deploy (takes a few minutes)
uv run python deployment/deploy.py --create

# List deployed agents
uv run python deployment/deploy.py --list

# Test the deployed agent interactively
uv run python deployment/test_deployment.py \
  --resource_id=projects/PROJECT_ID/locations/us-central1/reasoningEngines/AGENT_ID \
  --user_id=my-user

# Delete an agent
uv run python deployment/deploy.py --delete --resource_id=RESOURCE_ID
```

## Project Structure

```
trade-agent/
├── trade_agent/
│   ├── __init__.py              # GCP env bootstrap
│   ├── agent.py                 # root_agent (orchestrator)
│   ├── prompt.py                # System prompts for all agents
│   ├── tools.py                 # TradeView API tool functions
│   └── sub_agents/
│       ├── portfolio_agent.py
│       ├── options_agent.py
│       └── market_agent.py
├── deployment/
│   ├── deploy.py                # Vertex AI Agent Engine management
│   └── test_deployment.py       # Interactive test after deploy
├── tests/
│   └── test_agents.py
├── eval/
│   ├── test_eval.py
│   └── data/trade-agent.test.json
├── pyproject.toml
└── .env.example
```

## Calling from TradeView

Once deployed, add an API route to the TradeView Next.js app to proxy requests to the Vertex AI Agent Engine endpoint. The resource ID returned by `--create` is the endpoint to call.

```typescript
// Example: src/app/api/agent/route.ts
// POST { message: string, sessionId: string }
// → calls Vertex AI Agent Engine REST API with GCP auth
// ← returns agent response text
```
