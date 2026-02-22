"""Evaluation suite for Trade Agent using ADK evaluator."""

import dotenv
import pytest
from google.adk.evaluation import AgentEvaluator

dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_agent_eval():
    """Run full evaluation suite against test cases."""
    await AgentEvaluator.evaluate(
        agent_module="trade_agent",
        eval_dataset_file_path_or_dir="eval/data/trade-agent.test.json",
        num_runs=1,
    )
