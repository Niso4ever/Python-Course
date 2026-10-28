# Lesson: Agent Evals & Testing
## How to Know If Your Agent Is Actually Getting Better

> **2026 Note:** You just reviewed the `continual-learning-bench` — a real benchmark framework that measures how well agents learn from experience. This lesson teaches you to BUILD eval systems like that, not just read them. Evals are the #1 skill separating hobby agents from production agents.

## Why This Lesson Exists

You can now build agents that:
- Loop, use tools, produce structured output (Phase 4)
- Run concurrently (L01 Async)
- Use memory and skills (Anthropic SDK)

**What's missing:** How do you know any of it WORKS? How do you measure improvement? How do you catch regressions before they reach users?

That's what evals and testing are for.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to spot eval/test patterns in real code (START HERE)
2. **PASS_C_VISUAL.md** — Eval pipeline diagrams
3. **PASS3_TEMPLATES.md** — 6 eval templates you can copy and run (the 6th uses the `pydantic-evals` library)

## Templates
4. **CHEATSHEET_L01.py** — Quick reference (KEEP OPEN while writing evals)
5. **template_agent_eval.py** — Runnable demo: compare a learning agent with a stateless baseline over 10 instances, with reward tracking

## The Two Worlds of Agent Quality

```
Traditional Testing                 Agent Evals
─────────────────                  ───────────
"Does it crash?"                    "Does it improve?"
Pass / Fail                         Reward curve (0.0 → 1.0)
assert x == y                       assert score > baseline
Run once                            Run N episodes
Deterministic                       Stochastic (run 3x, take mean)
Unit test                           Benchmark instance
```

**The key insight:** Traditional tests ask "is the output correct?" Agent evals ask "is the output BETTER than last time?"

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (30 min)
**Step 2:** Study `PASS_C_VISUAL.md` (10 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (15 min)
**Step 4:** Run `template_agent_eval.py` to watch reward tracking in action
