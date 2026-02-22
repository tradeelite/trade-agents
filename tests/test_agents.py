"""Unit tests for Trade Agent."""

import textwrap

import dotenv
import pytest
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

from trade_agent.agent import root_agent

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_portfolio_query():
    """Agent should handle portfolio analysis queries."""
    user_input = "How is my portfolio doing?"

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    assert response != ""
    assert any(
        word in response.lower()
        for word in ["portfolio", "holding", "value", "position"]
    )


@pytest.mark.asyncio
async def test_market_research_query():
    """Agent should handle market research queries for a ticker."""
    user_input = "Give me a quick analysis of AAPL"

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    assert response != ""
    assert "aapl" in response.lower() or "apple" in response.lower()


@pytest.mark.asyncio
async def test_options_query():
    """Agent should handle options position queries."""
    user_input = textwrap.dedent(
        """
        Do I have any urgent options actions I need to take?
        """
    ).strip()

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    assert response != ""
    assert any(
        word in response.lower()
        for word in ["option", "position", "expir", "dte", "trade"]
    )


@pytest.mark.asyncio
async def test_sentiment_query():
    """Agent should handle sentiment and news queries."""
    user_input = "What's the market sentiment on TSLA right now?"

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    assert response != ""
    assert "tsla" in response.lower() or "tesla" in response.lower()
