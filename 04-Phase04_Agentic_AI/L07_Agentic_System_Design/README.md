# Lesson 23: Agentic System Design
## The Architect's Decision Framework

> **This lesson is different.** No templates to copy-paste. No tool calls to parse. This is the architect's view: WHEN do you use agents, HOW many, WHAT tools, and WHERE to put the guardrails.

## Why This Lesson Exists

You can now read and recognize:
- The agent loop (L02)
- Tool schemas and dispatch (L03)
- Structured output (L04)
- Multi-agent orchestration (L05)
- MCP tool connections (L06)

**The question that remains:** When you sit down with a real problem — how do you decide WHICH of these patterns to use, and how to combine them?

That's agentic system design. It's the skill that separates someone who can read agent code from someone who can DIRECT the creation of agent systems.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to read design decisions in real systems (START HERE)
2. **PASS_C_VISUAL.md** — Decision trees and architecture diagrams
3. **PASS3_TEMPLATES.md** — Design decision frameworks (not code templates — thinking templates)
4. **CHEATSHEET_L07.py** — Quick reference for design choices

## The Core Questions of Agentic System Design

```
1. Does this NEED an agent?           → or is a single LLM call enough?
2. One agent or many?                 → when does splitting help?
3. What tools?                        → minimum viable tool set
4. What guardrails?                   → where can it go wrong?
5. What memory?                       → what needs to persist?
6. How do you know it's working?      → evaluation strategy
```

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (30 min)
**Step 2:** Study `PASS_C_VISUAL.md` (15 min)
**Step 3:** Work through `PASS3_TEMPLATES.md` (20 min — use as a design checklist)
