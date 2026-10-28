# L01 — Pass 1: RECOGNITION
## How to Spot Eval & Test Patterns in Real Code

**Goal:** After this pass, you can look at any test file or benchmark and instantly identify: What's being measured? What's the baseline? How do they know if it's good enough?

---

## Pattern 1: The `pytest` Shape

This is the universal testing shape in Python. Every test framework builds on this.

```python
# SHAPE: test function with assertions
def test_agent_returns_valid_json():
    result = agent.run("What is 2+2?")
    parsed = json.loads(result)        # ← crashes if not valid JSON
    assert "answer" in parsed          # ← fails if key missing
    assert isinstance(parsed["answer"], (int, str))  # ← type check
```

**What to recognize:**
- Function starts with `test_` → pytest will find and run it automatically
- `assert` → "this MUST be true, or the test fails"
- No `print()` needed — pytest reports pass/fail for you

**3-second recognition:** See `def test_*` + `assert` → you found a test.

---

## Pattern 2: The Fixture (Shared Setup)

When multiple tests need the same setup — a fixture provides it.

```python
# SHAPE: reusable test setup
import pytest

@pytest.fixture
def agent():
    """Create a fresh agent for each test."""
    return MyAgent(model="gpt-5-mini", system_prompt="Be concise.")

@pytest.fixture
def sample_queries():
    return ["What is AI?", "Explain async", "Define eval"]

def test_agent_responds(agent, sample_queries):
    for query in sample_queries:
        result = agent.run(query)
        assert len(result) > 0, f"Empty response for: {query}"
```

**What to recognize:**
- `@pytest.fixture` → "this function provides something tests need"
- Test functions receive fixtures by **name** — pytest injects them automatically
- Fixtures run fresh for each test (isolation)

---

## Pattern 3: The Eval Instance (From CLBench)

This is the pattern you saw in `continual-learning-bench`. Each task instance is a single evaluation point.

```python
# SHAPE: structured eval instance
@dataclass
class InstanceOutcome:
    instance_id: str         # ← which test case
    instance_index: int      # ← its position in the sequence
    reward: float            # ← 0.0 (worst) to 1.0 (best)
    success: bool | None     # ← binary pass/fail (optional)

# Usage in a benchmark:
outcomes = []
for i, instance in enumerate(task_instances):
    response = system.respond(instance.query)
    reward = evaluate(response, instance.expected)
    outcomes.append(InstanceOutcome(
        instance_id=instance.id,
        instance_index=i,
        reward=reward,
        success=reward > 0.5,
    ))

mean_reward = sum(o.reward for o in outcomes) / len(outcomes)
```

**What to recognize:**
- `reward: float` → numeric score per instance (not just pass/fail)
- `instance_index` → ordered sequence (so you can plot learning curves)
- Results are **accumulated**, not just checked individually

---

## Pattern 4: The Reward Curve (Learning Trajectory)

The whole point of continual learning evals — does the agent improve over time?

```python
# SHAPE: loss/reward curve computation
loss_curve = []
for i, outcome in enumerate(outcomes):
    optimal = 1.0                           # best possible
    loss = optimal - outcome.reward         # gap from perfect
    loss_curve.append(loss)

# Plotting the learning trajectory:
# Early instances: high loss (agent doesn't know the task)
# Later instances: low loss (agent has learned from feedback)
#
# loss_curve = [0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1, 0.05]
#              ↑ bad at first                    ↑ getting better
```

**What to recognize:**
- `loss_curve` or `reward_curve` → per-instance performance over time
- Downward loss curve = agent is learning
- Flat loss curve = agent is NOT learning (just repeating mistakes)
- This is exactly what CLBench's `EvalMetrics.loss_curve` tracks

---

## Pattern 5: Baseline Comparison (Gain Metric)

The real question isn't "how good is the agent?" — it's "how much BETTER is it than a naive baseline?"

```python
# SHAPE: stateful vs stateless comparison
# Baseline: agent with NO memory (reset between each instance)
baseline_rewards = []
for instance in instances:
    system.reset()                    # ← clear all memory
    result = system.respond(instance)
    baseline_rewards.append(evaluate(result))

# Stateful: agent WITH memory (carries learning across instances)
stateful_rewards = []
# system.reset() called only ONCE at the start
for instance in instances:
    result = system.respond(instance)
    stateful_rewards.append(evaluate(result))

# Gain = stateful - baseline
mean_gain = mean(stateful_rewards) - mean(baseline_rewards)
# Positive gain = memory is helping
# Zero gain = memory is useless
# Negative gain = memory is hurting!
```

**What to recognize:**
- Two runs: one with memory, one without
- `gain = stateful - baseline` → the value of learning
- This is exactly how CLBench computes `mean_gain`

---

## Pattern 6: Property-Based Testing (Schema Validation)

Instead of testing specific inputs, test that PROPERTIES hold for ANY input.

```python
# SHAPE: property-based test with hypothesis
from hypothesis import given, strategies as st

@given(prompt=st.text(min_size=1, max_size=500))
def test_agent_always_returns_valid_schema(prompt):
    """For ANY prompt, the agent must return valid JSON matching the schema."""
    result = agent.run(prompt)
    parsed = ResponseSchema.model_validate_json(result)  # ← Pydantic validates
    assert parsed.action is not None
    assert 0.0 <= parsed.confidence <= 1.0
```

**What to recognize:**
- `@given(...)` → "run this test with MANY random inputs"
- `strategies as st` → generators for random test data
- The test checks a PROPERTY ("always valid JSON") not a specific value
- Extremely powerful for finding edge cases in agent output

---

## Pattern 7: The `assert` Vocabulary

Different assertions test different things:

```python
# Exact match
assert result == "expected"

# Contains / membership
assert "error" not in result.lower()
assert "answer" in response_dict

# Type checking
assert isinstance(result, dict)

# Numeric bounds
assert 0.0 <= score <= 1.0
assert len(result) > 0

# Schema validation (Pydantic)
parsed = MySchema.model_validate_json(result)  # raises if invalid

# Custom message on failure
assert score > 0.5, f"Score {score} is below threshold for instance {i}"
```

---

## Recognition Drill: Read This Real Eval Code

```python
def evaluate_system(system, task, num_runs=3):
    all_scores = []

    for run_idx in range(num_runs):               # ← Pattern 5: multiple runs
        task.prepare_run(run_idx)                  # ← shuffle instance order
        query = task.reset()
        system.reset()
        outcomes = []

        while True:
            response = system.respond(query)       # ← agent produces action
            step = task.step(response)             # ← task evaluates it
            system.observe(step.observation)       # ← feedback to agent

            if step.instance_outcome:
                outcomes.append(step.instance_outcome)  # ← Pattern 3: collect

            if step.done:
                break
            query = step.next_query

        result = task.evaluate()
        all_scores.append(result.score)            # ← Pattern 4: reward curve

    return {
        "mean_score": mean(all_scores),            # ← Pattern 5: aggregate
        "std_score": std(all_scores),
        "num_runs": num_runs,
    }
```

**What you should spot:**
1. Three runs with different orderings (robust evaluation)
2. The system-task-observe loop (CLBench pattern)
3. Per-instance outcomes collected into a list
4. Mean + std aggregation (not just one number)

---

## Quick Reference: When You See...

| You See | It Means |
|---------|----------|
| `def test_*` | pytest test function |
| `@pytest.fixture` | Reusable test setup |
| `assert x == y` | Exact match check |
| `InstanceOutcome(reward=...)` | Numeric eval score |
| `loss_curve` | Performance over time |
| `baseline` vs `stateful` | Gain comparison |
| `@given(...)` | Property-based test (Hypothesis) |
| `num_runs=3` | Multiple runs for statistical robustness |
