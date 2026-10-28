"""
CHEATSHEET — Agent Evals & Testing (L01)
Keep this open while writing evals for your agents.

2026 Note: These are patterns, not rigid libraries. Adapt them to your needs.
"""

import json
from dataclasses import dataclass

# ─── PATTERN 1: The pytest Shape ────────────────────────────
# Save as test_*.py and run with `pytest tests/`
def test_agent_output():
    result = {"action": "search", "query": "python"}
    assert "action" in result            # fail if key missing
    assert result["action"] == "search"  # fail if wrong value


# ─── PATTERN 2: Pydantic Schema Validation ──────────────────
from pydantic import BaseModel, ValidationError

class OutputSchema(BaseModel):
    confidence: float
    reasoning: str

def test_schema(raw_json_string: str):
    try:
        # Pydantic validates the JSON matches the schema exactly
        parsed = OutputSchema.model_validate_json(raw_json_string)
        assert 0.0 <= parsed.confidence <= 1.0
    except ValidationError as e:
        assert False, f"Agent returned invalid schema: {e}"


# ─── PATTERN 3: The Eval Instance (CLBench style) ───────────
@dataclass
class InstanceOutcome:
    instance_id: str
    instance_index: int
    reward: float        # 0.0 to 1.0

# Collect these during a run:
# outcomes.append(InstanceOutcome("q1", 0, 0.8))


# ─── PATTERN 4: Reward & Loss Curves ────────────────────────
def calculate_metrics(outcomes: list[InstanceOutcome]) -> dict:
    rewards = [o.reward for o in outcomes]
    return {
        "mean_reward": sum(rewards) / len(rewards),
        # Loss curve shows learning over time (down is good)
        "loss_curve": [1.0 - r for r in rewards],
        # Did the agent improve from start to finish?
        "is_learning": rewards[-1] > rewards[0],
    }


# ─── PATTERN 5: Baseline vs Stateful (Gain) ─────────────────
def evaluate_gain(stateful_rewards: list[float], baseline_rewards: list[float]):
    stateful_mean = sum(stateful_rewards) / len(stateful_rewards)
    baseline_mean = sum(baseline_rewards) / len(baseline_rewards)

    # Gain = how much did memory/learning help?
    gain = stateful_mean - baseline_mean
    return gain


# ─── COMMON ASSERTIONS VOCABULARY ───────────────────────────
#
# Exact match:          assert result == "expected"
# Substring:            assert "error" not in result.lower()
# Dict key:             assert "answer" in result_dict
# Type check:           assert isinstance(result, list)
# Numeric bounds:       assert 0.0 <= score <= 1.0
# Length check:         assert len(results) == 5
# Custom message:       assert score > 0.5, f"Score {score} too low"


# ═══ QUICK REFERENCE TABLE ═════════════════════════════════
#
# | Question                        | Use                              |
# |---------------------------------|----------------------------------|
# | Is the JSON formatted right?    | Pydantic model_validate_json     |
# | Does it work for basic inputs?  | Unit test (pytest)               |
# | Did it get better over time?    | Reward curve / Loss curve        |
# | Is memory actually helping?     | Gain (Stateful vs Baseline)      |
# | Did we break an old feature?    | Regression test (Golden output)  |
# | Is the score reliable?          | Multi-run eval (mean ± std)      |
