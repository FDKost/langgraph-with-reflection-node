import os
import json

from graph import run_agent

def test_full_flow():
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    question = "Explain the difference between a cat and a dog."
    result = run_agent(question, max_rounds=2)
    assert "draft" in result
    assert "critique" in result
    assert "verdict" in result
    assert result["round"] <= 2
    critique = json.loads(result["critique"])
    assert "verdict" in critique
    assert "feedback" in critique
    assert critique["verdict"] in ("ok", "needs_revision")
