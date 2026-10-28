# Vibe Coding Companion — Reverse-Engineered

## What this folder is

Every other phase teaches you to **read** code. This phase teaches you to **summon** it.

We took the **56 templates** in this course (plus the 4 end-to-end projects) and ran them backwards. Instead of
"here is the code, understand it," each entry shows:

```
📝 THE VIBE PROMPT   →   💻 THE CODE IT PRODUCES
(what you type)          (the existing template)
```

This is the missing half of the field manual, `../01-Phase01_Foundation/Phase1(B)/L21_Vibe_Coding/VIBE_CODERS_FIELD_MANUAL.md`. The manual taught the
*theory* (Spec Levels, the 5 Modes, the Constraint Sandwich). This folder is the
*worked answer key* — every finished template, each with the prompt that would
have produced it.

---

## The metaphor

> A **recipe** lists ingredients and steps. A **finished dish** is what you eat.
> The whole course hands you finished dishes. This folder reverse-engineers the
> **recipe** from each dish — so next time you can cook it yourself, from scratch,
> just by describing what you want.

---

## How to read each entry

Every entry is one template, tagged with two things from the Field Manual:

| Tag | Meaning | Where it's defined |
|-----|---------|--------------------|
| **Level 0–4** | How precise the spec is (Vibes → Features → Behavior → Contract → Test Cases) | Field Manual: *Specification Spectrum* |
| **Mode 1–5** | The kind of session (Exploration / Specification / Iteration / Debugging / Integration) | Field Manual: *The Five Modes* |

The prompt itself follows the **Constraint Sandwich**:
1. **Constraints** — rules you've already decided (so the AI doesn't decide them).
2. **Request** — the one thing you want built.
3. **Validation** — the checklist the output must pass.

---

## The map

| File | Covers | Templates |
|------|--------|-----------|
| [`01_Phase1A_Foundation.md`](01_Phase1A_Foundation.md) | L01–L06 syntax patterns, incl. L06 Part 0 OOP anatomy | 21 |
| [`02_Phase1B_Patterns.md`](02_Phase1B_Patterns.md) | L11–L21 architecture patterns | 13 |
| [`03_Core_Templates.md`](03_Core_Templates.md) | The 3 reusable `Templates/` files | 3 |
| [`04_Phase3_ToolUse.md`](04_Phase3_ToolUse.md) | Tool schemas + Pydantic | 4 |
| [`05_Phase4_Agentic.md`](05_Phase4_Agentic.md) | Raw-API agent patterns | 6 |
| [`06_Phase5_SDK.md`](06_Phase5_SDK.md) | Anthropic Agent SDK | 6 |
| [`07_Phase6_Async.md`](07_Phase6_Async.md) | Async for Agents | 1 |
| [`08_Phase7_Evals.md`](08_Phase7_Evals.md) | Evals & Testing | 1 |
| [`09_Phase8_Debugging.md`](09_Phase8_Debugging.md) | Code Review & Debugging | 1 |
| [`10_Phase9_EndToEnd.md`](10_Phase9_EndToEnd.md) | End-to-End Architectures | 4 (projects) |
| **Total** | | **56 templates + 4 projects = 60** |

> **Start here for the rules, not the answers:**
> [`VIBE_CODING_BEST_PRACTICES_2026.md`](VIBE_CODING_BEST_PRACTICES_2026.md) —
> the 10 rules behind this answer-key (current models, adaptive thinking, MCP),
> plus a pre-flight checklist. The entries below show *what* good prompts produce;
> that file explains *how* to write them.

---

## The one rule to remember

**Start at the highest Spec Level that matches your certainty.**

- Don't know what you want? → Level 1 (features)
- Know what it should *do*? → Level 2 (behavior)
- Know the *interface*? → Level 3 (contract) ← your default as an Architect
- Know the *edge cases*? → Level 4 (test cases)

Notice while reading: the boring templates (configs, lists) were summoned at
Level 1–2. The valuable ones (tools, agents, RAG) were summoned at Level 3–4.
**Precision is the whole job.**
