# L01 — Pass 3: TEMPLATES
## Your Agent Eval Copy-Paste Library

**Goal:** Six ready-to-use eval patterns (five hand-built, one library). Copy, configure, run.

> **2026 Note:** All templates work standalone — no API keys needed. They eval simulated agents so you see the patterns in action.

---

## Template 1: Basic Unit Test (pytest)

**Use when:** Checking that agent output matches a schema or format.

```python
# File: tests/test_agent_output.py
import json
import pytest
from pydantic import BaseModel

class AgentResponse(BaseModel):
    action: str
    confidence: float

# ─── Fixture: shared agent setup ─────────────────────
@pytest.fixture
def agent_output():
    """Simulate what an agent returns."""
    return '{"action": "fold", "confidence": 0.85}'

# ─── Tests ────────────────────────────────────────────
def test_output_is_valid_json(agent_output):
    parsed = json.loads(agent_output)
    assert isinstance(parsed, dict)

def test_output_matches_schema(agent_output):
    response = AgentResponse.model_validate_json(agent_output)
    assert response.action in ["fold", "call", "raise"]
    assert 0.0 <= response.confidence <= 1.0

def test_output_has_required_fields(agent_output):
    parsed = json.loads(agent_output)
    assert "action" in parsed, "Missing 'action' field"
    assert "confidence" in parsed, "Missing 'confidence' field"

# Run with: pytest tests/test_agent_output.py -v
```

---

## Template 2: Reward-Based Eval (CLBench Style)

**Use when:** Measuring how well an agent performs across multiple instances.

```python
"""Eval: Does the agent score above a threshold?"""
from dataclasses import dataclass
import statistics

@dataclass
class InstanceOutcome:
    instance_id: str
    instance_index: int
    reward: float

def simulate_agent_rewards(num_instances: int = 10) -> list[InstanceOutcome]:
    """Simulate an agent that slowly learns."""
    import random
    random.seed(42)
    outcomes = []
    base_skill = 0.3  # starts bad

    for i in range(num_instances):
        # Agent improves slightly each round
        noise = random.uniform(-0.1, 0.1)
        reward = min(1.0, base_skill + (i * 0.06) + noise)
        outcomes.append(InstanceOutcome(
            instance_id=f"instance_{i}",
            instance_index=i,
            reward=round(reward, 3),
        ))
    return outcomes

def evaluate(outcomes: list[InstanceOutcome]) -> dict:
    rewards = [o.reward for o in outcomes]
    loss_curve = [round(1.0 - r, 3) for r in rewards]
    return {
        "mean_reward": round(statistics.mean(rewards), 4),
        "std_reward": round(statistics.stdev(rewards), 4) if len(rewards) > 1 else 0,
        "loss_curve": loss_curve,
        "best_instance": max(outcomes, key=lambda o: o.reward).instance_id,
        "worst_instance": min(outcomes, key=lambda o: o.reward).instance_id,
        "improving": rewards[-1] > rewards[0],  # last > first?
    }

# Run:
outcomes = simulate_agent_rewards(10)
results = evaluate(outcomes)
print(f"Mean reward: {results['mean_reward']}")
print(f"Improving: {results['improving']}")
print(f"Loss curve: {results['loss_curve']}")
```

---

## Template 3: Baseline Comparison (Gain Metric)

**Use when:** Measuring if memory/learning actually helps vs a stateless baseline.

```python
"""Eval: Is stateful better than stateless?"""
import random
import statistics

def run_stateless_baseline(num_instances: int = 10, seed: int = 42) -> list[float]:
    """Agent with NO memory — same performance every time."""
    rng = random.Random(seed)
    return [round(rng.uniform(0.2, 0.5), 3) for _ in range(num_instances)]

def run_stateful_agent(num_instances: int = 10, seed: int = 42) -> list[float]:
    """Agent WITH memory — improves over time."""
    rng = random.Random(seed)
    rewards = []
    skill = 0.3
    for i in range(num_instances):
        reward = min(1.0, skill + rng.uniform(-0.05, 0.1))
        rewards.append(round(reward, 3))
        skill += 0.05  # learning!
    return rewards

def compute_gain(stateful: list[float], baseline: list[float]) -> dict:
    gain = statistics.mean(stateful) - statistics.mean(baseline)
    return {
        "stateful_mean": round(statistics.mean(stateful), 4),
        "baseline_mean": round(statistics.mean(baseline), 4),
        "gain": round(gain, 4),
        "memory_helps": gain > 0,
        "relative_improvement": f"{(gain / statistics.mean(baseline)) * 100:.1f}%"
            if statistics.mean(baseline) > 0 else "N/A",
    }

# Run:
baseline = run_stateless_baseline()
stateful = run_stateful_agent()
results = compute_gain(stateful, baseline)
print(f"Baseline: {results['baseline_mean']}")
print(f"Stateful: {results['stateful_mean']}")
print(f"Gain: {results['gain']} ({'✓ memory helps' if results['memory_helps'] else '✗ memory hurts'})")
print(f"Improvement: {results['relative_improvement']}")
```

---

## Template 4: Regression Test (Golden Output)

**Use when:** Making sure changes don't break what already works.

```python
"""Eval: Did we break something?"""
import json
from pathlib import Path

GOLDEN_DIR = Path("tests/golden_outputs")

def save_golden(test_name: str, output: dict):
    """Save a known-good output as the golden reference."""
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    path = GOLDEN_DIR / f"{test_name}.json"
    path.write_text(json.dumps(output, indent=2))
    print(f"Saved golden: {path}")

def check_regression(test_name: str, current_output: dict) -> dict:
    """Compare current output against saved golden."""
    path = GOLDEN_DIR / f"{test_name}.json"
    if not path.exists():
        return {"status": "no_golden", "message": "No golden file — run save_golden first"}

    golden = json.loads(path.read_text())

    diffs = {}
    for key in set(list(golden.keys()) + list(current_output.keys())):
        old = golden.get(key)
        new = current_output.get(key)
        if old != new:
            diffs[key] = {"golden": old, "current": new}

    if not diffs:
        return {"status": "pass", "message": "No regression detected"}
    return {"status": "fail", "message": f"Regression in {len(diffs)} field(s)", "diffs": diffs}

# Usage:
# First run (save baseline):
# save_golden("poker_eval", {"mean_reward": 0.65, "improving": True})

# Later runs (check for regression):
# result = check_regression("poker_eval", {"mean_reward": 0.60, "improving": True})
# → {"status": "fail", "diffs": {"mean_reward": {"golden": 0.65, "current": 0.60}}}
```

---

## Template 5: Multi-Run Statistical Eval

**Use when:** Agent outputs are stochastic — one run isn't enough.

```python
"""Eval: Run N times, report mean ± std."""
import random
import statistics

def run_eval_once(run_index: int, num_instances: int = 10) -> float:
    """Single eval run — returns mean reward."""
    rng = random.Random(42 + run_index)  # different seed per run
    rewards = []
    skill = 0.3
    for i in range(num_instances):
        reward = min(1.0, skill + rng.uniform(-0.1, 0.15))
        rewards.append(reward)
        skill += 0.04
    return statistics.mean(rewards)

def run_multi_eval(num_runs: int = 5, num_instances: int = 10) -> dict:
    """Run the eval multiple times and aggregate."""
    scores = [run_eval_once(i, num_instances) for i in range(num_runs)]
    return {
        "num_runs": num_runs,
        "scores": [round(s, 4) for s in scores],
        "mean": round(statistics.mean(scores), 4),
        "std": round(statistics.stdev(scores), 4) if len(scores) > 1 else 0,
        "min": round(min(scores), 4),
        "max": round(max(scores), 4),
        "confidence": "high" if statistics.stdev(scores) < 0.05 else "low",
    }

# Run:
results = run_multi_eval(num_runs=5)
print(f"Score: {results['mean']} ± {results['std']} ({results['confidence']} confidence)")
print(f"Range: [{results['min']}, {results['max']}]")
print(f"Individual runs: {results['scores']}")
```

---

## Template 6: The Same Idea With a Library (`pydantic-evals`)

**Use when:** You have more than a handful of cases and want a ready-made report instead of hand-rolled loops.

Templates 1–5 build the eval machinery by hand so you can see it. In real 2026 code you will often see a library doing the same job. `pydantic-evals` (installed in the course venv) uses the same three ideas: **cases** (inputs + expected output), a **task** (your agent function), and **evaluators** (the scoring rules).

```python
"""Eval: a dataset of cases, scored by evaluators. Runs offline."""
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EqualsExpected

def classify(text: str) -> str:
    """Stand-in for your agent. Swap in the real call later."""
    return "refund" if "money back" in text else "other"

dataset = Dataset(
    name="intent_classifier",          # required in the installed version
    cases=[
        Case(name="refund", inputs="I want my money back", expected_output="refund"),
        Case(name="other", inputs="Where is my order?", expected_output="other"),
    ],
    evaluators=[EqualsExpected()],     # output must equal expected_output
)

report = dataset.evaluate_sync(classify)   # runs every case, collects scores
report.print(include_input=True, include_output=True)
```

**What to recognize:**
- `Case(...)` = one test instance (like `InstanceOutcome`, but defined *before* the run)
- `Dataset(cases=..., evaluators=...)` = the benchmark
- `evaluate_sync(task)` = "run my agent on every case and give me the table"
- The library also ships an `LLMJudge` evaluator (a model grades the output against a rubric). That one makes API calls, so keep it out of demo mode.

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| Check output format/schema | Template 1: Unit Test |
| Measure performance across instances | Template 2: Reward Eval |
| Compare memory vs no-memory | Template 3: Baseline Comparison |
| Catch regressions after changes | Template 4: Golden Output |
| Statistically robust evaluation | Template 5: Multi-Run |
| Many cases, ready-made report | Template 6: pydantic-evals |
