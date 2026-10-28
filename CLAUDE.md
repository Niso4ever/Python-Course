# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running Code

**Template files** (all `template_*.py` and `CHEATSHEET_*.py`):
```bash
python template_name.py          # run from inside the lesson folder
```
Templates run without an API key and print simulated output. Templates in Phases 4–6 set `DEMO_MODE = True` at the top (the Phase 7 and Phase 8 templates use no flag). In Phases 0, 1 and 4 only `L24_Evaluation_Metrics/template_evaluator.py` has the flag; the other 40 have none and simply never call an API from their `__main__` block (counted 2026-10-28).

**Phase 2 projects** (require real API key):
```bash
cd 02-Phase02_Real_Systems/ProjectN_Name
pip install -r requirements.txt
cp .env.example .env             # then add ANTHROPIC_API_KEY
python main.py
```
Each Phase 2 `main.py` also takes `--demo` (`python main.py --demo`), which runs simulated output with no key.

**Phase 5 SDK lessons** (`05-Phase05_Agent_SDK/`) — templates also default to `DEMO_MODE = True`. Real runs need `pip install -r 05-Phase05_Agent_SDK/requirements.txt`, which adds `claude-agent-sdk>=0.1.0` on top of `anthropic` + `pydantic`. `claude-agent-sdk` is not installed in the shared venv; PyPI showed 0.2.174 on 2026-10-24, so raise the floor when you first install it.

**Lesson cheatsheets** are not executable programs — they are reference files, meant to stay open while reading. Do not run them expecting output unless they have a `if __name__ == "__main__":` block. Several (L01–L05, L20) deliberately contain broken lines as "spot the error" examples and stop with a `SyntaxError` or `NameError` if run.

## Lesson File Format

Most lessons in Phase 1(A), Phase 1(B), Phase 4, Phase 5 and Phases 6–8 use the files below. Not every lesson has every file (checked against the tree on 2026-10-28): `PASS_B_REVERSE.md` exists only in Phase 1(A) L01–L07; `PASS_C_VISUAL.md` is missing from L01, L02, L07, L11–L13, L18–L20 and L22–L24; `PASS3_TEMPLATES.md` exists only in L02 (as `PASS3_TEMPLATES_L01_L02.md`), L03–L06, L08, L09 and L16; `L22_PydanticAI_Framework` and `L23_Structured_Outputs` are a single README with no cheatsheet or template; L10 and L07 have no `template_*.py`. Phase 3 uses its own layout (`README.md` per lesson plus phase-level `CHEATSHEET.md`, `INDEX.md`, `QUICKSTART.md`, `SUMMARY.md`).

| File | Purpose |
|------|---------|
| `README.md` / `Lxx_Name.md` | Main lesson content |
| `PASS1_RECOGNITION.md` | Read-only pattern recognition — 8 examples, no writing |
| `PASS_C_VISUAL.md` | Flowcharts and diagrams |
| `PASS3_TEMPLATES.md` | Template overview and usage |
| `CHEATSHEET_Lxx.py` | Quick reference — keep open while working |
| `template_*.py` | Copy-paste starting points; each runs independently |
| `PASS_B_REVERSE.md` | Path B: find this lesson's patterns inside `template_rag_pipeline.py` |

**The 3-pass learning method:** PASS1 (recognize) → PASS_C_VISUAL (diagram) → PASS3 (use templates). Path B reverses this: start from `template_rag_pipeline.py` and find L01–L07 patterns inside it.

## Phase and Lesson Numbering

```
Folder                            Phase       Lessons
00-Phase00_OOP_Introduction       Phase 0     warm-up, no Lxx numbers
01-Phase01_Foundation/Phase1(A)   Phase 1A    L00 (setup file), L01–L07
01-Phase01_Foundation/Phase1(B)   Phase 1B    L08–L24
02-Phase02_Real_Systems           Phase 2     4 projects, no Lxx
03-Phase03_Tool_Use               Phase 3     L01–L04
04-Phase04_Agentic_AI             Phase 4     L01–L08
05-Phase05_Agent_SDK              Phase 5     L01–L06
06-Phase06_Async                  Phase 6     L01
07-Phase07_Evals                  Phase 7     L01
08-Phase08_Debugging              Phase 8     L01
09-Phase09_End_to_End_Projects    Phase 9     4 projects, no Lxx
99-Vibe_Coding_Companion          companion   prompt answer-key for every template; no lessons
```

The folder number is the phase number. Each phase numbers its own lessons from L01. Phase 1 is the exception: its two parts share one sequence (L01–L24), with `Lesson0_Setup_and_First_Steps.md` before L01.

When a lesson in another phase is referenced, it carries the phase prefix: `Ph4-L04` is Agentic AI lesson 4 (Structured Output), while a bare `L04` in Phase 1 text is Loops and Iteration. Phase 1 lessons are referenced without a prefix.

Renumbered on 2026-10-28 (`_maintenance/renumber.py`). Old → new: Phase 3–10 became Phase 2–9 (there was never a Phase 2). Agentic AI L00, L25–L31 became L01–L08. The second Phase 1B track L18 PydanticAI, L19 Structured Outputs, L20 Evaluation Metrics became L22, L23, L24, so no two lessons share a number. Documents written before that date, such as `UPDATE_LOG_2026-10-28.md`, use the old numbers.

## Key Files

- `01-Phase01_Foundation/Templates/template_rag_pipeline.py` — the most important single file in the course. L01–L07 patterns all appear here. Path B uses it as the source of truth.
- `REVISED_CURRICULUM_MAP.md` — the 4-tier learning hierarchy (Permanent → Architectural → Reading → Reference) and 8-week plan.
- `VIBE_CODERS_FIELD_MANUAL.md` — how to direct AI as an architect: Specification Spectrum (Levels 0–4), five session modes, Constraint Sandwich technique.
- `AGENTS.md` — three agent personas (Tutor, Vibe Coder, Dialectic Auditor) and handoff protocol.
- `05-Phase05_Agent_SDK/README.md` — the Phase 5 entry point and the "three-tier landscape" framing the later phases build toward.
- `99-Vibe_Coding_Companion/` — reverse-engineers the 56 `template_*.py` files (plus the 4 end-to-end projects) into vibe-coding prompts (one per template, the prompt-→-code direction), 60 documented entries total. Each entry is tagged with its Spec Level (0–4) and Mode (1–5) and structured as a Constraint Sandwich. Companion answer-key to `VIBE_CODERS_FIELD_MANUAL.md`; start at its `README.md`.

## The Three-Tier Agent Progression (Phases 4–5)

The curriculum teaches agents at three escalating levels of abstraction. Knowing which tier a lesson targets explains why its templates look the way they do:

- **Tier 1 — Raw API** (Phase 4 L02–Ph4-L06): `import anthropic`, `client.messages.create()`, you hand-write the agent loop and tool dispatch.
- **Tier 2 — Agent SDK** (Phase 5, L01–L05): `from claude_agent_sdk import query`; the SDK owns the loop, tool execution, context, and retries. You supply tools + system prompt + task.
- **Tier 3 — Managed Agents** (Phase 5, L06): `client.beta.agents.create()` + `client.beta.sessions...`; Anthropic's servers run the agent. Public beta since April 2026, still beta on 2026-10-28 (platform.claude.com/docs/en/managed-agents/overview).

Phase 5 assumes Phase 4 L02 (the hand-written loop) and Phase 3 L01–L02 (type hints + Pydantic, which back the tool schemas) are already understood.

## Architecture of a Phase 2 Project

Each project separates concerns across three files:
- **`ingest.py` / `agents.py` / `signatures.py`** — setup and definitions (run once or imported)
- **`main.py`** — entry point and orchestration
- **`tools.py` / `retriever.py` / `pipeline.py`** — core logic

Project 1 (RAG): `ingest.py` loads and embeds docs into ChromaDB → `retriever.py` searches and generates → `main.py` runs the loop.

Project 4 (DSPy): `signatures.py` declares input/output contracts → `pipeline.py` assembles the module → `optimizer.py` trains prompts from examples → `main.py` runs inference.

## Current Claude API facts (checked 2026-10-28)

Re-check these against platform.claude.com before relying on them; they change.

- **Models:** `claude-opus-5-5` (recommended default), `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-fable-5-1` (hardest reasoning). Prices per million tokens in/out: $4/$20, $2/$10, from $0.10/$0.50, $10/$50. All have a 1M-token context window. Every Claude 3.x ID used in older lessons is retired and fails. Source: models overview and model-deprecations pages.
- **`temperature`, `top_p`, `top_k` are gone.** Removed in API version 2026-10-21; sending them returns a 400 error. Phase 1 lessons still use `temperature` as an example of a `float`, with a note.
- **Forced tool use returns 400 on Opus 5.5, Sonnet 5.5 and Fable 5.1.** `tool_choice` `"any"` or `"tool"` only works on older models and Haiku 5.5. For structured output use `client.messages.parse(output_format=Model)`; Ph4-L04 teaches this. The Ph4-L03/Ph4-L04/Ph4-L05 files that still show forced `tool_choice` as a legacy pattern deliberately keep a 4.x model ID so the example stays valid. Source: tool-use define-tools page.
- **Thinking is adaptive, set by `effort`** (`low`/`medium`/`high`/`xhigh`/`max`); `budget_tokens` is rejected on 4.7 and later.
- `Phase1(B)/L09_Error_Reading` uses fake model IDs (`claude-99`, `gpt-99`) on purpose. Don't "fix" them.

## Coding Standards (for new code in this repo)

- `DEMO_MODE = True` at top of every new template; the demo path must run with zero external calls.
- Type hints on all function parameters and return types.
- Pydantic `BaseModel` for data validation; every field needs `Field(description="...")`.
- `@dataclass` for config/dependency containers (stateless structures).
- Google-style docstrings on all tool functions with `Args:` and `Returns:` sections.
- No `.ipynb` files — `.py` only.
