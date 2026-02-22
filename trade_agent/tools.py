"""Tools that call the TradeView API to give agents access to live trading data."""

import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

_BASE_URL = os.getenv("TRADEVIEW_API_URL", "http://localhost:3000")


def _get(path: str, params: dict | None = None) -> Any:
    """Make a GET request to the TradeView API."""
    url = f"{_BASE_URL}{path}"
    response = httpx.get(url, params=params, timeout=10.0)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Portfolio tools
# ---------------------------------------------------------------------------

def get_portfolios() -> list[dict]:
    """Get all portfolios with their current total value and performance.

    Returns a list of portfolios including id, name, total value, cost basis,
    and overall gain/loss.
    """
    return _get("/api/portfolios")


def get_portfolio_holdings(portfolio_id: int) -> list[dict]:
    """Get all holdings for a specific portfolio with live price valuations.

    Args:
        portfolio_id: The numeric ID of the portfolio.

    Returns a list of holdings with ticker, shares, average cost, current price,
    current value, and gain/loss for each position.
    """
    return _get(f"/api/portfolios/{portfolio_id}/holdings")


# ---------------------------------------------------------------------------
# Market / stock tools
# ---------------------------------------------------------------------------

def get_stock_quote(ticker: str) -> dict:
    """Get the current real-time price quote for a stock or ETF.

    Args:
        ticker: The stock ticker symbol (e.g. AAPL, MSFT, SPY).

    Returns current price, change, change percent, open, high, low,
    volume, market cap, P/E ratio, and 52-week range.
    """
    return _get(f"/api/stocks/{ticker.upper()}/quote")


def get_stock_news(ticker: str) -> list[dict]:
    """Get the latest news articles for a stock or ETF.

    Args:
        ticker: The stock ticker symbol (e.g. AAPL, TSLA).

    Returns up to 10 recent news items with title, publisher, URL, and timestamp.
    """
    return _get(f"/api/stocks/{ticker.upper()}/news")


def get_stock_sentiment(ticker: str) -> dict:
    """Get StockTwits social media sentiment for a stock.

    Args:
        ticker: The stock ticker symbol.

    Returns bullish/bearish percentage, watchlist count, and latest community messages
    with sentiment tags.
    """
    return _get(f"/api/stocks/{ticker.upper()}/sentiment")


def get_company_info(ticker: str) -> dict:
    """Get company background information for a stock.

    Args:
        ticker: The stock ticker symbol.

    Returns sector, industry, description, employee count, and website.
    """
    return _get(f"/api/stocks/{ticker.upper()}/summary")


def get_technical_indicators(ticker: str, range: str = "3M") -> dict:
    """Get technical indicator values for a stock (SMA, EMA, RSI, MACD, Bollinger Bands).

    Args:
        ticker: The stock ticker symbol.
        range: Time range — one of 1D, 1W, 1M, 3M, 1Y, 5Y. Defaults to 3M.

    Returns computed SMA (20/50/200), EMA (12/26), RSI (14), MACD, and Bollinger Bands
    as time-series arrays.
    """
    return _get(f"/api/stocks/{ticker.upper()}/indicators", params={"range": range})


# ---------------------------------------------------------------------------
# Options tools
# ---------------------------------------------------------------------------

def get_options_trades(status: str = "open") -> list[dict]:
    """Get options trades tracked in TradeView.

    Args:
        status: Filter by trade status — "open", "closed", or "all". Defaults to "open".

    Returns a list of options trades with ticker, option type (call/put), direction
    (buy/sell), strike price, expiry date, premium, quantity, current status, and P&L.
    """
    return _get("/api/options", params={"status": status})


def get_options_suggestions() -> list[dict]:
    """Get AI-generated rule-based suggestions for open options positions.

    Returns actionable alerts including profit target closures (50% profit),
    DTE roll warnings (<21 days), assignment risk alerts (within 3% of strike),
    and earnings conflict warnings.
    """
    return _get("/api/options/suggestions")
