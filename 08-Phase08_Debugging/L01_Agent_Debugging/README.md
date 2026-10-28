# Lesson: Code Review & Debugging for Agents
## When "Print" Isn't Enough: Traces, Logs, and State

> **2026 Note:** When a traditional app fails, it crashes. You get a stack trace, you fix the bug. When an agent fails, it *doesn't* crash. It just confidently gives you the wrong answer. You can't fix that with a stack trace. You need a reasoning trace.

## Why This Lesson Exists

You know how to build:
- Tool schemas (Phase 3) and single agents (Phase 4)
- Multi-agent systems (Phase 4 L05) and SDK subagents (Phase 5)
- Concurrent agents (L01 Async)
- Agent evaluations (L01 Evals)

**What's missing:** What do you do when the eval fails? When the agent gets stuck in a loop? When it hallucinates a tool call? When three agents fighting over the same memory file corrupt it?

This lesson covers the specific failure modes of agentic systems and the tools you need to debug them.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to spot debugging patterns and failure modes (START HERE)
2. **PASS_C_VISUAL.md** — Failure mode diagrams
3. **PASS3_TEMPLATES.md** — 5 debugging tools you can copy and use

## Templates
4. **CHEATSHEET_L01.py** — Quick reference for agent debugging
5. **template_trace_debugger.py** — Runnable demo: an agent logger and trace analyzer

## The Three Agent Failure Modes

1. **Reasoning Failures** (Hallucinations, loops, ignoring instructions)
   - *Fix:* Trace analysis, prompt engineering, better tool descriptions
2. **State Failures** (Corrupt memory, forgotten context, context window overflow)
   - *Fix:* Context window monitoring, memory diffs, state checkpointing
3. **Concurrency Failures** (Race conditions, deadlocks)
   - *Fix:* Locks, semaphores, queues (Async Patterns)

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (25 min)
**Step 2:** Study `PASS_C_VISUAL.md` (10 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (15 min)
**Step 4:** Run `template_trace_debugger.py` to see a trace logger in action
