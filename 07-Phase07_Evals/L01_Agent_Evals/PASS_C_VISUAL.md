# L01 — Pass C: VISUAL
## The Eval Pipeline — See How Benchmarks Work

---

## Diagram 1: The Eval Loop (What CLBench Does)

```
┌─────────┐    Query     ┌─────────┐    Response    ┌─────────┐
│  Task   │─────────────►│ System  │───────────────►│  Task   │
│(problem)│              │ (agent) │                │ (judge) │
└─────────┘              └─────────┘                └────┬────┘
     ▲                        ▲                          │
     │                        │                     Observation
     │                   Observation               (feedback +
     │                   (feedback)                  reward)
     │                        │                          │
     │                        └──────────────────────────┘
     │                                                   │
     └───────────────── next_query ──────────────────────┘

Repeats for each instance in the task schedule.
```

---

## Diagram 2: Single Test vs Eval Benchmark

```
Traditional Test (one check):
┌──────┐     ┌──────┐     ┌────────┐
│Input │────►│ Code │────►│Pass/Fail│
└──────┘     └──────┘     └────────┘


Agent Eval (many instances, learning curve):
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│  Inst  │  │  Inst  │  │  Inst  │  │  Inst  │  │  Inst  │
│   1    │  │   2    │  │   3    │  │   4    │  │   5    │
└───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘
    │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼
  r=0.2       r=0.4       r=0.6       r=0.7       r=0.9
    │           │           │           │           │
    └───────────┴───────────┴───────────┴───────────┘
                          │
                    mean_reward = 0.56
                    trend: improving ↑
```

---

## Diagram 3: Baseline vs Stateful Comparison

```
Baseline (no memory — reset between each instance):

Instance:  1      2      3      4      5
Reward:   0.3    0.4    0.3    0.2    0.4     mean = 0.32
          ───    ───    ───    ───    ───      (flat — no learning)


Stateful (memory carries across instances):

Instance:  1      2      3      4      5
Reward:   0.2    0.4    0.6    0.8    0.9     mean = 0.58
          ───    ───    ────   ────   ────     (rising — learning!)


Gain = stateful_mean - baseline_mean = 0.58 - 0.32 = +0.26
       ↑ positive = memory is helping
```

---

## Diagram 4: The Loss Curve (What You Want to See)

```
Loss (lower is better)
1.0 │ ■
    │  ■
0.8 │   ■
    │    ■
0.6 │     ■
    │
0.4 │       ■  ■
    │
0.2 │            ■  ■
    │                  ■  ■  ■
0.0 │─────────────────────────────►
    1  2  3  4  5  6  7  8  9  10
                Instance

Good: Loss decreases → agent is learning
Bad:  Loss stays flat → agent ignores feedback
Worst: Loss increases → agent is forgetting
```

---

## Diagram 5: pytest Execution Flow

```
$ pytest tests/

pytest discovers:
├── tests/test_agent_output.py
│   ├── test_returns_valid_json         ✓ PASS
│   ├── test_respects_schema            ✓ PASS
│   └── test_handles_empty_input        ✗ FAIL
├── tests/test_eval_rewards.py
│   ├── test_reward_above_baseline      ✓ PASS
│   └── test_no_regression              ✓ PASS

Results: 4 passed, 1 failed in 2.3s
```

```
How pytest finds tests:
1. Looks in files named test_*.py or *_test.py
2. Runs functions named test_*
3. Each assert that fails = test failure
4. Each assert that passes = silent (no news is good news)
```

---

## Diagram 6: The Full Eval Pipeline

```
┌──────────────────────────────────────────────────────────┐
│                    BENCHMARK RUNNER                        │
│                                                           │
│  ┌─────────┐   For each run (3x):                        │
│  │  Config  │                                             │
│  │ (system +├──► ┌──────────────────────────────────┐     │
│  │  task)   │    │  1. task.reset()                  │     │
│  └─────────┘    │  2. system.reset()                │     │
│                  │  3. Loop:                          │     │
│                  │     query = task.build_query()     │     │
│                  │     response = system.respond()    │     │
│                  │     step = task.step(response)     │     │
│                  │     system.observe(step.obs)       │     │
│                  │     collect outcome                │     │
│                  │  4. result = task.evaluate()       │     │
│                  └──────────────┬────────────────────┘     │
│                                 │                          │
│                                 ▼                          │
│                  ┌──────────────────────────┐              │
│                  │  Aggregate across runs:   │              │
│                  │  mean_score ± std          │              │
│                  │  loss_curve               │              │
│                  │  gain vs baseline         │              │
│                  └──────────────────────────┘              │
│                                 │                          │
│                                 ▼                          │
│                  ┌──────────────────────────┐              │
│                  │  Output:                  │              │
│                  │  - results.json           │              │
│                  │  - viewer artifacts       │              │
│                  │  - leaderboard entry      │              │
│                  └──────────────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

---

## Decision Flowchart: Which Test Type?

```
What are you checking?
├── "Does the output match a schema?"
│   └── Unit test (assert + Pydantic validation)
│
├── "Does the agent improve over time?"
│   └── Eval benchmark (reward curve + baseline comparison)
│
├── "Does the output work for ANY input?"
│   └── Property-based test (Hypothesis)
│
├── "Does the whole pipeline work end-to-end?"
│   └── Integration test (spin up agent + tools + run query)
│
└── "Did we break something that used to work?"
    └── Regression test (save golden outputs, compare)
```
