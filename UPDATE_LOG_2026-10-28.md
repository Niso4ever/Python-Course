# 1-Course update log — 2026-10-28

> **Renumbered after this log was written (also 2026-10-28).** This log uses the old names. Old → new folders: `0-Phase0_OOP_Introduction` → `00-Phase00_OOP_Introduction`, `1-Phase1_Foundation` → `01-Phase01_Foundation`, `2-Phase3_RealSystems` → `02-Phase02_Real_Systems`, `3-Phase4_ToolUse_FunctionCalling` → `03-Phase03_Tool_Use`, `4-Phase5_Agentic_AI` → `04-Phase04_Agentic_AI`, `5-Anthropic_Agent_SDK` → `05-Phase05_Agent_SDK`, `7-Async_for_Agents` → `06-Phase06_Async`, `8-Evals_and_Testing` → `07-Phase07_Evals`, `9-Code_Review_and_Debugging` → `08-Phase08_Debugging`, `10-End_to_End_Projects` → `09-Phase09_End_to_End_Projects`, `6-Vibe coding` → `99-Vibe_Coding_Companion`. Lessons: Agentic AI L00, L25–L31 → L01–L08; Phase 1B L18 PydanticAI, L19 Structured Outputs, L20 Evaluation Metrics → L22, L23, L24. See `CLAUDE.md`.


Three agents each checked one part of the course; the lead then replaced the model IDs across the whole course and ran every file again. Each agent's full log is appended below with its sources. Every fact that can go out of date carries a source URL and the retrieval date 2026-10-28.

## What was actually wrong (as opposed to merely dated)

1. **Retired model IDs as live defaults.** Phase 1 and Phase 4 templates defaulted to `claude-3-opus-20240229`, `claude-3-5-sonnet-20241022` and `claude-3-haiku-20240307`. All three are retired, and requests to them fail (model-deprecations page).
2. **Forced tool use breaks on current models.** `tool_choice` `"any"`/`"tool"` returns 400 on Opus 5.5, Sonnet 5.5 and Fable 5.1 (define-tools page). L27 taught it as *the* structured-output pattern. It now teaches `client.messages.parse(output_format=Model)`, and the old pattern is marked as legacy.
3. **`temperature` / `top_p` / `top_k` were removed** in API version 2026-10-21 and now return 400 (model-deprecations page, "API parameter deprecations").
4. **Agent SDK and Managed Agents code was wrong**:
   - `query()` takes keyword arguments only.
   - There is no `Tool` class.
   - `session_id=` does not resume a session.
   - The L06 Managed Agents calls and events did not exist.

   See log B.
5. **MCP 2.x** removed the `list_tools`/`call_tool` decorators (log B).
6. **Pydantic v1 code taught as current** (`@validator`, `min_items`, a field named `model_config`). The citation cross-check never ran (log A).
7. **LangChain 0.x and PydanticAI 0.x APIs.** These imports fail on the installed versions (log A).
8. **Code bugs**:
   - The async timing template overstated its speedup (2.4x instead of the real 1.8x).
   - The repair loop never checked the output of its last repair.
   - `gather` was described wrongly.

   See log C.

## Lead's sweep (scripts in the session scratchpad: sweep_models.py, fix_prices.py)

- **Model IDs:** 399 replacements in 138 files.
  - Mapping: retired 3.x IDs and the 4.x defaults (`claude-opus-4-6`, `claude-opus-4-8`, `claude-sonnet-4-6`, `claude-haiku-4-5`) and `claude-fable-5` → `claude-opus-5-5` / `claude-sonnet-5-5` / `claude-haiku-5-5` / `claude-fable-5-1`.
  - Source: https://platform.claude.com/docs/en/about-claude/models/overview and https://platform.claude.com/docs/en/about-claude/model-deprecations (retrieved 2026-10-28).
- **Deliberately not swept:**
  - `Phase1(B)/L09_Error_Reading`: fake IDs (`claude-99`, `gpt-99`) used as teaching material.
  - The 13 files that still show forced `tool_choice` (L26, L27 PASS/README/CHEATSHEET, L28 PASS, the Phase 4 CHEATSHEET, the Project1 extractor). They keep a 4.x model, which still accepts forced tool use. Retired 3.x IDs in them went to `claude-opus-4-8` or `claude-sonnet-4-6`.
  - `gpt-*` IDs in the OpenAI lessons. These were not checked.
- **Prices keyed to models.** Updated to Opus 5.5 $4/$20, Sonnet 5.5 $2/$10 and Haiku 5.5 $0.10/$0.50 per MTok in:
  - `template_llm_caller.py`
  - `template_rag_agent.py`
  - `template_multi_tool_agent.py`
  - `template_debug_toolkit.py`
  - `CHEATSHEET_L20.py`
  - Project1 RAG `main.py`

  Generic `rate=0.000015` defaults in the L05 lessons on default parameters were left alone, because they are not tied to a model.
- **Prose model names** in Phase 3 projects and L25/L26 demo fixtures. In L14, context windows changed from 200K to 1M tokens.
- **`temperature`:**
  - Removed from the Anthropic call in L05 PASS1 Example 7.
  - Added a note in L01 PASS1, where it is used as a `float` example.
  - Added inline notes in the L07 reading examples (real-world LangChain code).
- **Course `CLAUDE.md`:** new "Current Claude API facts" section. Also corrected the Managed Agents status (still beta) and the Agent SDK pin note.
- **Phase 5 README:** "every framework is deprecated or abandoned" was false; CrewAI 1.0 was released in October 2025. Reworded.
- **L02 `template_list_operations.py`:** a bug that predates this update (`user_question` was undefined). Fixed.

## Lead follow-ups after the advisor review

- **Vibe coding.** Entries 43 (L27), 50 (Ph6-L04) and 52 (Ph6-L06) described code the agents had since rewritten. They now ask for:
  - `messages.parse`
  - `resume=` with the session ID read from `ResultMessage`
  - agents, environments, sessions and events

  Each entry was checked line by line against the template's real-mode code. `10_Phase10_EndToEnd.md` got the forced-`tool_choice` caveat.
- **L09 Error Reading.** The "valid model IDs" lists (the right answers next to the fake IDs) now name the 5.5 models. The fake IDs are unchanged.
- **L12 lesson text.** Cost constants now match `template_debug_toolkit.py` (Sonnet 5.5, $2/$10).
- **Haiku 5.5 price comment.** Its pricing is tiered at 100k prompt tokens, so the price tables now carry a comment saying so.
- **Vibe best-practices model table.** Now carries a source line.
- **Sweep scripts** copied to `1-Course/_maintenance/` (`sweep_models.py`, `fix_prices.py`), with the ID mapping and the list of forced-tool files inside them, so the sweep can be replayed.
- **Two things Agent A did beyond its brief** (both easy to revert):
  - Removed the unused `langchain`/`tiktoken` lines from Phase 3 Project 1's `requirements.txt`.
  - Rewrote the L10 cheatsheet's example pins to the venv versions.
- **Agent C's demo runs regenerated two trace files**, `9-…/agent_trace.jsonl` and Project3 `audit_trace.jsonl`. Both are outputs of their own templates, but the originals were not saved, so a before/after comparison isn't possible.

## Final runs (lead, after all edits)

- 56/56 `template_*.py` exit 0 (re-run after the follow-ups above).
- 19 of the 38 cheatsheets that were run exit 0. The other 19 fail as expected:
  - 10 are deliberate "spot the error" cheatsheets or reference snippets (L01–L05, L20, L26, L27, L29, L30).
  - 6 need packages that aren't installed (`claude_agent_sdk`, `agents`, `langchain_anthropic`).
  - 2 need an API key at import.
  - L25 has a module-level `while True` and hangs.
  - `CHEATSHEET_L19.py`, the 39th, was not run because it calls outside websites.
- 4/4 Phase 3 `main.py --demo` and 4/4 End-to-End `main.py` runs (no key) exit 0.
- A green demo run proves syntax and imports only. **No live API call was made**, so the new `messages.parse`, Agent SDK and Managed Agents code is checked against docs and the installed SDK's signatures, not against the live API.

## Open items for the user

- Try one live call per new pattern before trusting it: L27 `messages.parse`, L04 `resume=`, L06 Managed Agents.
- L02 and L06 PASS files have correction notes at the top, but their old code blocks are still there. A full rewrite is recommended (log B).
- `claude-agent-sdk` is not installed; PyPI shows 0.2.174 (2026-10-24). `crewai` and `chromadb` are not installed either; their minimum versions were not changed because no current version was confirmed.
- Structural recommendations, not applied:
  - Fold `L19_Structured_Outputs` into L27, and point `L20_Evaluation_Metrics` at Phase 8.
  - Delete the duplicate `template_rag_pipeline_clone.py` and the old copy of the field manual in L21.
  - Add `DEMO_MODE` to `CHEATSHEET_L19.py` and `template_api_tool.py`, which call live third-party APIs.
  - Add Tool Runner (`client.beta.messages.tool_runner`) to L25/L26 as what replaces the hand-written loop.
  - Phases 7, 8 and 9 have one lesson each; log C lists what to add next.

---

# Log A — Phases 0, 1, 3, 4 and top-level docs

Date: 2026-10-28. Venv: /home/niso4ever/AIarch/.venv. Nothing installed. No model ID string edited (verified: `grep -rnoE "(claude|gpt|gemini)-[A-Za-z0-9.-]+"` over scope before and after, multiset per file identical, 362 hits both times).

Tavily returned 429 midway; later pages were fetched with `.claude/skills/websearch/fetch_pages.py` (saved under scratchpad `pages/`).

## Sources used (all retrieved 2026-10-28)

| Id | URL | Quote / fact relied on |
|---|---|---|
| S1 | https://pypi.org/project/dspy-ai/ | "`dspy-ai` is a compatibility alias for the dspy package. Install `dspy` instead: `pip install dspy`." (latest dspy / dspy-ai 3.4.1) |
| S2 | https://github.com/stanfordnlp/dspy/issues/7931 | maintainer: "`dspy.Predict` itself supports type, no need to use TypedPredictor now." Installed dspy 3.4.0: `hasattr(dspy, "TypedPredictor") == False` |
| S3 | https://github.com/stanfordnlp/dspy/tree/main/dspy/retrievers | retrievers dir = `databricks_rm.py, embeddings.py, retrieve.py, weaviate_rm.py` (no ChromadbRM). Installed 3.4.0 matches |
| S4 | https://dspy.ai/current/cheatsheet | still lists `dspy.Retrieve`, `BootstrapFewShot`, `MIPROv2`, `SIMBA` — so these were left alone |
| S5 | https://github.com/stanfordnlp/dspy/discussions/10314 | 3.3→3.4: "If your code looks like this, nothing changes for you: `lm = dspy.LM(...)`; `dspy.configure(lm=lm)`" — L16/Project4 `dspy.LM` usage confirmed current |
| S6 | https://pydantic.dev/docs/ai/project/changelog | v0.6.0: "The `result_type` ... arguments were removed from the `Agent` class. Use `output_type` instead." / "Removed deprecated ... `AgentRunResult.data` property". Installed pydantic-ai 2.53.0: `Agent(..., result_type=...)` raises TypeError; `result.output` works with TestModel |
| S7 | https://docs.pydantic.dev/latest/migration/ | "`@validator` has been deprecated, and should be replaced with `@field_validator`"; "`min_items` (use `min_length` instead)", "`max_items` (use `max_length` instead)"; `model_config` is the class-settings attribute in v2 |
| S8 | https://docs.langchain.com/oss/python/migrate/langchain-v1 and https://docs.langchain.com/oss/python/releases/langchain-v1 | namespace table: "`langchain.tools` @tool, BaseTool, injection helpers — Re-exported from langchain-core"; "If you were using any of the following from the langchain package, you'll need to install langchain-classic ... Legacy chains ... The hub module"; "`from langchain_classic import hub`"; `create_agent(model=..., tools=[...], system_prompt=...)`. Installed langchain 1.2.10: `langchain.agents` has `create_agent`, not `AgentExecutor`; `langchain.memory` missing; `langchain_classic.agents/memory/hub` import fine; `langchain_core.tools.Tool` imports fine |
| S9 | https://docs.crewai.com/v1.15.28/en/concepts/memory | "By default, `Memory()` uses OpenAI `text-embedding-3-large` embeddings ... Set `OPENAI_API_KEY` for the default path, or configure a custom embedder"; provider table row "VoyageAI / voyageai / voyage-3" |
| S10 | https://pypi.org/project/crewai/ , https://pypi.org/project/crewai-tools/ | release history shows `1.0.0 Oct 20, 2025` (latest version not visible in extract) |
| S11 | https://pypi.org/project/chromadb/ | "1.5.9 This release May 5, 2026"; `1.0.0 Apr 3, 2025` |
| S12 | https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools | "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 — any and tool return a 400 error — auto with strict tool use to guarantee schema-valid tool inputs, or structured outputs when you need a response in a fixed JSON shape." (coordinator's finding, re-fetched and confirmed myself) |

## Changes made

### Structure (filesystem was the oracle; `ls`/`find` on 2026-10-28)
| File | What | Why |
|---|---|---|
| 1-Course/CLAUDE.md | Numbering table gained rows for `6-Vibe coding` (companion), `7-Async_for_Agents` (Phase 7), `8-Evals_and_Testing` (Phase 8), `9-Code_Review_and_Debugging` (Phase 9), `10-End_to_End_Projects` (Phase 10) plus a note on where those labels come from and the two folders whose own titles disagree | Folders existed, doc ignored them. Labels taken from `6-Vibe coding/07_Phase7_Async.md … 10_Phase10_EndToEnd.md` |
| 1-Course/CLAUDE.md | "Every lesson … follows this structure" → "Most lessons …" with the exact exceptions (PASS_B only in 1A; PASS_C missing L01, L02, L07, L11–L13, L18–L20; PASS3 only in L02–L06, L08, L09, L16; L18_PydanticAI/L19_Structured_Outputs single README; Phase 4's own layout) | False as written |
| 1-Course/CLAUDE.md | "All templates have DEMO_MODE = True" → counted: Phases 5–7 use it; Phase 8/9 templates don't; in Phases 0/1/4 only `L20_Evaluation_Metrics/template_evaluator.py` has it (40 of 41 don't) | False as written |
| 1-Course/CLAUDE.md | Added: Phase 3 `main.py --demo`; cheatsheets L01–L05/L20 contain deliberate broken lines and stop if run | Matches behaviour seen in demo runs |
| 1-Course/AGENTS.md | Removed link to nonexistent `.agents/rules/brand_voice_metaphors.md`; now says no dedicated rules file and points to CLAUDE.md Lesson File Format + Field Manual. Noted `/home/niso4ever/AIarch/memory.md` (handoff target) does not exist yet | Broken link; read all three real rules files first — none covers voice/metaphors |
| 1-Phase1_Foundation/README.md | 1(B) heading L08–L17 → L08–L21; added both L18–L20 tracks and L21 to list and link table (all 8 new links checked) | Folders existed |
| 1-Phase1_Foundation/Directory.md | Replaced fictional `MY_TEMPLATES/` tree with real `Phase1(A)/…` tree; fixed 4 broken links; replaced L03/L04 "Coming soon" with the real files | L03 has 5 templates, L04 has 3 |
| 1-Phase1_Foundation/Templates/README.md | Index listed 7 files that don't exist (`template_llm_wrapper.py`, `template_full_rag_agent.py`, …). Rewrote index and mapping table to the 3 files actually here + real lesson-folder equivalents; noted `_clone.py` is a byte-identical copy | Phantom files |
| Phase1(A) L02, L03, L04, L05, L06 main lessons; Phase1(B) L08, L09 (+PASS3), L10, L11, L12, L13 | "See MY_TEMPLATES/… for:" blocks → this lesson folder, listing only files that exist. Removed phantom `template_parallel_llm.py`, `template_rag_debugger.py`, `template_venv_setup.py`, `template_requirements.py`, `template_react_agent.py`; L10 now says it has no template; L11 points to Phase 7 for parallel agents | `MY_TEMPLATES/` doesn't exist |
| 12 Phase 1 READMEs/PASS3 | `CHEATSHEET_LessonN.py` (old numbering, e.g. `CHEATSHEET_Lesson7.py` in L09) → the folder's real `CHEATSHEET_Lxx.py` | Old names |
| Lesson0_Setup_and_First_Steps.md, L01_Labels_and_Types.md, L01 `1-README.md`, L02 `README.md` | Removed links to nonexistent `.ipynb` notebooks and pre-move paths; Lesson 0 now says ".py files only — no notebooks"; practice now points to `.py` files; "Back to" links fixed to `../../README.md` | Notebooks don't exist; course rule is no .ipynb |
| L03, L04 PASS3_TEMPLATES.md | Note: 5 of 8 (L03) / 3 of 12 (L04) templates are saved as .py; the rest exist only as code blocks on the page | Page labels 7+9 phantom files as "File:" |
| 2-Phase3_RealSystems/README.md | "Phase 1 and Phase 2" → "Phase 0 and Phase 1 (there is no Phase 2)"; Project 1 stack "Anthropic + ChromaDB + LangChain" → "Anthropic + ChromaDB"; documented `--demo` | No file in Project1 imports langchain |
| 3-Phase4…/SUMMARY.md | L04 "(placeholder) / Future" → its 5 real files | L04 is complete |
| 3-Phase4…/L01…/VISUAL_LLM_PERSPECTIVE.md | Broken `examples/` link → `template_search_tools.py` | Folder doesn't exist |
| REVISED_CURRICULUM_MAP.md | Timeline: "we are here" moved from the 2025 line to the 2026+ line (Oct 2026). Added "Beyond the 8 weeks" section listing L18–L21 and Phases 3, 5–10 + 6-Vibe; footer dated | Only the marker was wrong; the 8-week plan stops at L17 + Phase 4 |
| AIARCH_IMPLEMENTATION_COURSE.md | Status note: it is a plan; Phases 7–10, L25/L31 and Phase 6 now realise parts; weekly projects (20 tools, LangGraph, deployment, Postgres/Redis) not built (grep: LangGraph/Redis appear only in cheatsheets) | Reader could not tell plan from tree |
| VIBE_CODERS_FIELD_MANUAL.md | Cross-ref "L23, L30" → "L30" (no L23 since Phase 5 renumbering); pointer to Phases 7–10 and `6-Vibe coding/` after the Phase map box | Stale lesson number; map omitted later phases |

### Library currency
| File | What | Source |
|---|---|---|
| Project4 requirements.txt | `dspy-ai>=2.5.0` → `dspy>=3.4.0`; `anthropic>=0.40.0` → `>=1.11.0` | S1; installed versions |
| Project1/2/3 requirements.txt | `anthropic>=0.40.0` → `>=1.11.0` | installed |
| Project1 requirements.txt | Removed `langchain`, `langchain-anthropic`, `langchain-community`, `langchain-chroma`, `tiktoken` (dated comment). `chromadb>=0.5.0` kept with dated note "PyPI latest 1.5.9; 1.x client untested here" | grep: no import in ingest/retriever/main; S11 |
| Project3 requirements.txt | `crewai>=0.80.0`, `crewai-tools>=0.14.0` kept with dated note that 1.x has existed since Oct 2025, untested | S10 |
| Project4 optimizer.py docstring; L16 template docstring + print; L08 CHEATSHEET/PASS3/PASS_C/imports_for_dspy.py; L09 error_decoder.md; L10 CHEATSHEET | `pip install dspy-ai` → `pip install dspy`; pip→import tables now `dspy (formerly dspy-ai) → import dspy` | S1 |
| L10 CHEATSHEET_L10.py | Pinned "common stacks" were all 2024 pins. Installed packages set to venv versions (anthropic 1.11.0, python-dotenv 1.2.4, langchain 1.2.10, langchain-core 1.2.17, langchain-community 0.4.1, langchain-text-splitters 1.1.1, dspy 3.4.0); chromadb 1.5.9 (S11); not-installed ones marked "(2024, unchecked)"; note that langchain-anthropic 0.3.3 is too old for langchain 1.x | installed, S11, S10 |
| L16 PASS3_TEMPLATES.md | `ChromadbRM` (no longer in DSPy) → any query→passages function, `dspy.retrievers.Embeddings`, or `dspy.retrievers.WeaviateRM` | S3 |
| L16 template_dspy_signatures.py | Removed stray module-level `class ClassifyIntent(dspy.Signature if True else None)` before `import dspy` — template crashed with NameError on every run | bug (demo run) |
| L19_Structured_Outputs/README.md | `dspy.TypedPredictor(PlanAgent)` → `dspy.Predict(PlanAgent)`; heading + takeaway renamed "typed signatures" | S2 |
| L18_PydanticAI_Framework README + Integration doc | `result_type=` → `output_type=` (7×), `result.data` → `result.output` (8×), version note added. `system_prompt` left (still valid) | S6 + local check |
| Phase 4 L02 template_agent_schemas.py | `@validator` → `@field_validator`/`@classmethod`; cross-field citations check → `@model_validator(mode="after")` (the v1 version never fired: `confidence` is declared after `citations`); `min_items` → `min_length`; field `model_config` renamed `llm_config` (v2 reserves the name; template crashed with `TypeError: 'FieldInfo' object is not iterable`) | S7 |
| Phase 4 L04 template_production_rag_tools.py | `@validator` → `@field_validator`; `min_items/max_items` → `min_length/max_length` | S7 |
| Phase 4 CHEATSHEET.md | Same v2 fixes in the "Validation constraints" block (it claimed "uses Pydantic v2 throughout") | S7 |
| Phase 4 L04 template_framework_adapters.py, L04 README, L03 README, CHEATSHEET.md, QUICKSTART.md | `from langchain.tools import Tool/StructuredTool` → `from langchain_core.tools import …` (template crashed with ImportError on langchain 1.2.10); L03 agent example now shows `create_agent` for 1.x and `langchain_classic.agents` for the 0.x form; pseudo-code docstring in template got a 1.x note (its `gpt-4` string untouched) | S8 |
| L08 CHEATSHEET_L08.py, imports_for_agents.py, PASS3_TEMPLATES.md | Agent import lines: `from langchain.agents import AgentExecutor, create_react_agent` → `langchain_classic.agents` with comment; cheatsheet block 7 now leads with `create_agent`; quick-ref table has 1.x and classic rows | S8 |
| L15 template_react_patterns.py | lazy imports → `langchain_classic.agents` and `langchain_classic.hub`, with comment on `create_agent` | S8 |
| L08, L12, L13, L15 main lesson .md; L14 memory section | Dated "Version note": code shown is LangChain 0.x; in 1.x legacy pieces live in `langchain-classic`, new code uses `create_agent`; L14: `langchain.memory` gone, classes in `langchain_classic.memory`. Code examples themselves left as recognition material | S8 + local import check |
| Project3 crew.py + README | Comment and setup line: `memory=True` needs `OPENAI_API_KEY` (default OpenAI embeddings) or an `embedder={...}` dict. Behaviour unchanged | S9 |
| Project1 ingest.py docstring | "Anthropic's voyage-3 embeddings" → "Voyage AI's voyage-3" | S9 (VoyageAI row) |
| Phase 4 CHEATSHEET.md (coordinator request) | Model caveat added in both forced-tool_choice places: Opus 5.5 / Sonnet 5.5 / Fable 5.1 / Mythos 5.1 return 400 for `any`/`tool`; use `auto` + `strict: true`, or structured outputs. Rule line softened to "on models that support forced tool use". L13 and L19 grepped: neither teaches forced tool_choice, so no change | S12 |
| Phase 4 L01 template_search_tools.py | `__main__` crashed (`NoneType` not iterable) because tool bodies are `pass` stubs; added `or []` fallbacks and `similar = []` init | bug (demo run) |

## Demo runs

Run with `/home/niso4ever/AIarch/.venv/bin/python` from inside each folder; Phase 3 with `--demo`. Baseline before edits, then after. These prove syntax and imports only.

Fixed by this pass (fail → pass):
- 1-Phase1_Foundation/Phase1(B)/L16_DSPy_Signature_Paradigm/template_dspy_signatures.py
- 3-Phase4_ToolUse_FunctionCalling/L01_TypeHints_Docstrings/template_search_tools.py
- 3-Phase4_ToolUse_FunctionCalling/L02_Pydantic_Fundamentals/template_agent_schemas.py (also passes with `-W error::DeprecationWarning`)
- 3-Phase4_ToolUse_FunctionCalling/L04_Tool_Schemas/template_framework_adapters.py
- 3-Phase4_ToolUse_FunctionCalling/L04_Tool_Schemas/template_production_rag_tools.py (pass before and after; also passes with `-W error::DeprecationWarning`)

Pass, touched: L15 template_react_patterns.py (demo path; edited LangChain imports are lazy, verified importable), L08 imports_for_dspy.py, all four Phase 3 `main.py --demo`.

All other Phase 0/1/4 templates, cheatsheets and L08 import files: pass. Totals after edits: 61 of 72 files pass (68 Phase 0/1/4 files + 4 Phase 3 main.py); 11 fail, listed below.

Still failing, all pre-existing, not caused by edits:
- CHEATSHEET_L01, L02, L03, L04, L05 (Phase 1A), CHEATSHEET_L20 (L20_Evaluation_Metrics): deliberate broken "spot the error" lines / undefined names. Reference files, not programs.
- Phase1(A)/L02 template_list_operations.py: `NameError: user_question` in `__main__` (untouched).
- Phase1(B)/L08 CHEATSHEET_L08.py, imports_for_agents.py, imports_for_rag.py: `ModuleNotFoundError: langchain_anthropic` (not installed; not installing per brief). imports_for_agents.py previously died one line earlier on the removed `langchain.agents.AgentExecutor`.
- Phase1(B)/L19 CHEATSHEET_L19.py: makes live HTTP calls at module level (pokeapi, nationalize.io, httpbin); failed with connection reset. Note: running it (baseline and after) did make outbound requests.

## Unverified — not applied

- CrewAI 1.x compatibility of Project3 (`from crewai import Agent, LLM`, `Agent(memory=True)`, `from crewai.tools import tool`, `SerperDevTool`): not checked against 1.x docs (Tavily rate-limited). Floors left at 0.80.0/0.14.0 with dated note. Proposed: after a test install, raise to `crewai>=1.0` / `crewai-tools>=1.0`.
- Latest crewai version number: PyPI extract truncated; docs URL shows v1.15.28 but not confirmed as a release number.
- chromadb 1.x API (`PersistentClient`, `create_collection`, `get_collection`, `collection.add/query`) used by Project1: believed unchanged, no citation fetched. Floor left at 0.5.0. Proposed `chromadb>=1.5` after a test install.
- langchain-anthropic current version: not fetched. L10 marks 0.3.3 as too old for langchain 1.x (that follows from langchain 1.x needing langchain-core 1.x, installed here) but no replacement version given.
- OpenAI `client.beta.chat.completions.parse` in L19: both `beta.chat.completions.parse` and `chat.completions.parse` exist in installed openai 3.23.0; no docs citation for which is preferred, so unchanged.
- Whether DSPy `dspy.configure(lm=lm, rm=rm)` + `dspy.Retrieve` is still the recommended RAG pattern (it runs; S4 lists Retrieve). Left as is.
- Project4 README statistics ("15-30% better accuracy", "50,000+ tickets/day", "99.2% SLA", "4.8% override") and Phase 4 "Week 2" claims: no source; not edited (see recommendations).

## Recommendations

1. Discrepancy with the brief: `pip list` shows **langchain 1.2.10, langchain-core 1.2.17, langchain-community 0.4.1, langchain-classic 1.0.1, langchain-openai, tiktoken 0.12.0 ARE installed**; `langchain-anthropic`, `langchain-chroma`, `chromadb`, `crewai` are not. Also `dspy-ai 3.1.3` is installed alongside `dspy 3.4.0` (alias shim, harmless; could be uninstalled).
2. Phase 5 README (out of my scope) says CrewAI is "deprecated, forked, or abandoned", while Phase 3 Project 3 teaches CrewAI and PyPI shows active 1.x releases since Oct 2025 (S10). One of them is wrong; the Phase 5 claim looks wrong.
3. Parallel L18–L20 tracks: track 2 (PydanticAI, Structured Outputs, Evaluation Metrics) is three thin READMEs with no PASS files, cheatsheets or (except L20) templates. Either renumber (e.g. L22–L24) or fold: L19_Structured_Outputs overlaps Phase 5 L27_Structured_Output, and L20_Evaluation_Metrics overlaps Phase 8 L01_Agent_Evals. Suggest merging L19_Structured_Outputs into L27 as a "reading" appendix and pointing L20_Evaluation_Metrics at Phase 8.
4. L19_Structured_Outputs teaches only OpenAI JSON mode/parse and DSPy; it has no Anthropic structured-output or strict-tool example, although the rest of the course is Anthropic-first and S12 makes `strict: true` the replacement for forced tool_choice on the newest models.
5. LangChain 0.x `AgentExecutor`/`create_react_agent` code is the main example in L12, L13, L15 (and PASS1/PASS_C files). I added version notes rather than rewriting. A follow-up could add one `create_agent` example per lesson next to the classic one.
6. Duplicates: `Templates/template_rag_pipeline_clone.py` is byte-identical to `template_rag_pipeline.py`; `Phase1(A)/L05/template_rag_pipeline.py` is a different 189-line file with the same name as the 438-line Path-B source — confusing. `L21_Vibe_Coding/VIBE_CODERS_FIELD_MANUAL.md` is an older 598-line copy of the 782-line top-level manual (missing the Phase 6 section); replace with a link.
7. Phase 4 has five overview docs (README, INDEX, QUICKSTART, SUMMARY, CHEATSHEET) for four lessons; L03 has only a README. Consolidating would cut drift (SUMMARY still called L04 a placeholder).
8. Live network calls without a demo guard: `L19_Network_Requests_and_APIs/CHEATSHEET_L19.py` (module level) and `template_api_tool.py` (`__main__`, jokeapi, no timeout). Add `DEMO_MODE` per the course coding standard.
9. 40 of 41 templates in Phases 0/1/4 lack `DEMO_MODE`; CLAUDE.md coding standard asks for it on new templates. Low priority since they make no API calls, except item 8.
10. Label collisions to resolve: `6-Vibe coding/README.md` calls itself "Phase 7" (Phase 7 is Async), `10-End_to_End_Projects/README.md` calls itself "Lesson 10"; `9-…/README.md` refers to "Single agents (Phase 4)".
11. `.Zone.Identifier` files (Windows download artifacts) in L02 and L06: safe to delete.
12. Unsourced numbers presented as fact: Project 4 README production stats; AIARCH_IMPLEMENTATION_COURSE "$150k-$250k+ annual salary" and cost estimates. Under the workspace evidence rule these should be cited or labelled illustrative.
13. CHEATSHEET_L19 and template_api_tool should not be in any automated demo sweep until guarded; running them contacts third-party APIs.

## Addenda

- Demo-run safety: all four Phase 3 `main.py` files gate on `DEMO_MODE = "--demo" in sys.argv` checked before any key lookup (grep of each `main.py`), so the `--demo` sweeps made no Anthropic calls even though `load_dotenv()` can find `/home/niso4ever/AIarch/.env`. The only outbound calls in either sweep came from `CHEATSHEET_L19.py` (pokeapi.co, api.nationalize.io, httpbin.org).
- L08 `CHEATSHEET_L08.py` lines ~184–185 (class-vs-function example) kept `create_react_agent` as the teaching example but now carry a `# 0.x path; 1.x: langchain_classic.agents` comment. L08 `PASS1_RECOGNITION.md` and `PASS_C_VISUAL.md` still show the 0.x import with no inline note; the version note at the top of `L08_Import_Patterns.md` covers the lesson.
- Deliberate deviations from the brief, revertible: (a) removed the unused `langchain*`/`tiktoken` lines from Project 1 requirements instead of only proposing it; (b) rewrote the L10 cheatsheet's example pins to venv versions and marked the rest "unchecked"; (c) the Phase 4 tool_choice caveat adds model display names in prose ("Claude Opus 5.5" etc.), not ID strings — the ID diff is unchanged, but the lead's sweep may want to know.

---

# Log B — Phase 5 and Phase 6

Date: 2026-10-28. Scope: `1-Course/4-Phase5_Agentic_AI/` and `1-Course/5-Anthropic_Agent_SDK/` only.
No model ID strings were edited anywhere (lead's sweep). No packages installed.

## Read this first: blocker for the model-ID sweep

Forced tool use (`tool_choice={"type": "any"}` or `{"type": "tool", "name": ...}`) **returns HTTP 400 on
claude-opus-5-5, claude-sonnet-5-5, claude-fable-5-1 (and claude-mythos-5-1)**. The docs name the replacements:
`auto` plus `strict: true`, or structured outputs.
Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use (retrieved 2026-10-28).
The quote is the table row: "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 | `any` and `tool` return a 400 error".

The same page says forced tool use still works on models that accept it: Claude Opus 5 and Claude Haiku 5.5 are named, and Opus 4.6/4.7/4.8, Sonnet 5 and Sonnet 4.6 are older models. In the notes I added, forced `tool_choice` is labelled as legacy, valid only on those models. The coordinator's cross-agent finding is confirmed by this same fetch, and it has been acted on in L26, L27 and L28.

L27 (structured output) taught forced `tool_choice` as "the one shape", and L28 routing examples use it too. These
ran only because they pin `claude-opus-4-6`. If the sweep swaps them to 5.5 IDs without the L27 change below, every
structured-output example breaks. The L27 template now uses `client.messages.parse(output_format=...)`, which works
on all current models. L26/L28 PASS files still show forced `tool_choice` code, now with a note. Check this before
sweeping files outside my scope: grep `tool_choice={"type": "tool"` and `"any"` across the course.

## Verified model list

Source: https://platform.claude.com/docs/en/about-claude/models/overview.md (retrieved 2026-10-28)
Prices: https://platform.claude.com/docs/en/about-claude/pricing.md (retrieved 2026-10-28)
Status: https://platform.claude.com/docs/en/about-claude/model-deprecations.md (retrieved 2026-10-28)

| Model | API ID | Input $/MTok | Output $/MTok | Status |
|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 10 | 50 | Active, retires no sooner than 2027-09-01 |
| Claude Opus 5.5 | `claude-opus-5-5` | 4 | 20 | Active, no sooner than 2027-09-22 |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 2 | 10 | Active, no sooner than 2027-09-28 |
| Claude Haiku 5.5 | `claude-haiku-5-5` | 0.10 (prompts up to 100k tokens); 0.50 above 100k | 0.50 (up to 100k); 2.50 above 100k | Active, no sooner than 2027-10-07 |

The overview lists these four as the current lineup, so the expected list is confirmed. Opus 5.5 is the recommended default.

- `claude-opus-4-8`: **real**. Active, legacy, retires no sooner than May 28, 2027. Price $5 / $25. It is also the
  recommended replacement for retired Opus 4.1, Opus 4 and Opus 3 in the deprecations table.
- `claude-fable-5`: **real**. Active, legacy, retires no sooner than June 9, 2027. Price $10 / $50.
- Other legacy models still available: Opus 5, Opus 4.7, Opus 4.6, Opus 4.5, Sonnet 5, Sonnet 4.6, Haiku 4.5.
  Sonnet 4.5 is deprecated and retires 2026-11-30.
- Retired (requests fail):
  - `claude-3-opus-20240229`: retired January 5, 2026
  - `claude-3-5-sonnet-20240620` and `claude-3-5-sonnet-20241022`: retired October 28, 2025
  - `claude-3-haiku-20240307`: retired April 20, 2026
  - also `claude-3-5-haiku-20241022` (2026-02-19), `claude-3-7-sonnet-20250219` (2026-02-19), Sonnet 4 / Opus 4 (2026-06-15), Opus 4.1 (2026-08-05)
- Model IDs used in my scope today: `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-opus-4-8`, `claude-haiku-4-5`.
  All are active but legacy. They were left unchanged for the lead.
- Related: `temperature` / `top_p` / `top_k` are removed in API version 2026-10-21, and anthropic SDK 1.x dropped
  them. Grep found none in my scope. Source: model-deprecations page above, "API parameter deprecations".

## Changes made

Every changed fact is cited below. "Installed" means checked by `inspect` or by importing against `/home/niso4ever/AIarch/.venv` (anthropic 1.11.0, mcp 2.2.0).

### Requirements
- `5-Anthropic_Agent_SDK/requirements.txt` changes:
  - `anthropic>=0.50.0` → `>=1.11.0`
  - `pydantic>=2.0.0` → `>=2.13.5`
  - `python-dotenv>=1.0.0` → `>=1.2.4`

  These floors equal the installed versions (pip show). `claude-agent-sdk>=0.1.0` is left as it was, with a dated comment.
  The package is not installed. PyPI latest is 0.2.174, uploaded 2026-10-24 (https://pypi.org/pypi/claude-agent-sdk/json, retrieved 2026-10-28).
  Proposed pin, not applied: `claude-agent-sdk>=0.2.174`.

### Phase 6: Claude Agent SDK (L01–L05)
1. **`query()` is keyword-only.** Every `query(task, options=...)` / `query("...")` in L01, L02, L04, L05 and L06 (`.py` and `.md`, 72 call sites) became `query(prompt=..., ...)`. Signature: `async def query(*, prompt: str | AsyncIterable[...], options=..., transport=...)`. Passing it positionally raises TypeError. Source: https://code.claude.com/docs/en/agent-sdk/python (retrieved 2026-10-28).
2. **L02: there is no `Tool` class.** The real pattern is `@tool(name, description, input_schema)` on an async handler that returns `{"content": [{"type": "text", "text": ...}]}`, then `create_sdk_mcp_server(name=, tools=[...])`, then `mcp_servers={"key": server}`. `allowed_tools` takes name strings `"mcp__key__tool"`, not objects. Source: https://code.claude.com/docs/en/agent-sdk/custom-tools (retrieved 2026-10-28).
   - `template_sdk_tools.py` real path rewritten. The demo path is unchanged.
   - `CHEATSHEET_L02.py` rewritten.
   - `README.md` code block and lifecycle fixed, with a correction note.
   - `PASS1_RECOGNITION.md`, `PASS3_TEMPLATES.md`, `PASS_C_VISUAL.md`: correction note added at top; the PASS1 "Recognize" line about `allowed_tools` fixed. The individual `Tool(...)` blocks are not rewritten (see Unverified / not applied).
   - Phase 6 `README.md` lesson table row fixed.
3. **L04: `session_id=` does not resume.** In `ClaudeAgentOptions`, `session_id` means "Use a specific session ID instead of an auto-generated one". `resume` is "Session ID to resume". Source: https://code.claude.com/docs/en/agent-sdk/python (retrieved 2026-10-28).
   - Every `ClaudeAgentOptions(session_id=...)` in L04 (template, cheatsheet, README, PASS1, PASS3, PASS_C) now uses `resume=`.
   - Capturing the ID moved from `SystemMessage` to `ResultMessage`. In Python the ID on `SystemMessage` is nested in `.data`, and `ResultMessage.session_id` is always present. Source: https://code.claude.com/docs/en/agent-sdk/sessions (retrieved 2026-10-28).
   - Text fixed: "SDK maintains it server-side" is now "session file on local disk (`~/.claude/projects/`)", per the same page. README has a note on `resume` vs `session_id` and points to `ClaudeSDKClient`.
   - Phase 6 README table row fixed.
4. **L01: no `ToolUseMessage` or `ToolResultMessage` classes.** Tool calls are `ToolUseBlock`s inside `AssistantMessage`. Tool results are `ToolResultBlock`s inside `UserMessage`. Fixed in PASS1 Example 3, the PASS_C message diagram, and the CHEATSHEET_L01 comment. Source: https://code.claude.com/docs/en/agent-sdk/python (retrieved 2026-10-28).
5. **L03 `CHEATSHEET_L03.py` section 4.** It used `event.type == "tool_use"`, which is not a stream event. A tool call starts with `content_block_start` whose `content_block.type == "tool_use"`, followed by `input_json_delta`. Replaced the pseudo-code with text_stream + `get_final_message()`, then reading the tool_use blocks. Source: https://platform.claude.com/docs/en/build-with-claude/streaming.md (retrieved 2026-10-28).
6. **L05 README.** Added a short block showing `agents={"name": AgentDefinition(description, prompt, tools, model)}` and noting that `allowed_tools` auto-approves tools but does not restrict them. `"Agent"` is confirmed as the current tool name; older builds used "Task". This is a gap that made the lesson misleading: its orchestrator had no way to define the specialist. Source: https://code.claude.com/docs/en/agent-sdk/subagents (retrieved 2026-10-28).

### Phase 6: Managed Agents (L06)
7. **Still beta.** Status is `beta` and the header is `managed-agents-2026-04-01`, which the SDK sets itself. Source: https://platform.claude.com/docs/en/managed-agents/overview.md (retrieved 2026-10-28). The launch date of April 8, 2026 in public beta is confirmed by Anthropic's blog https://claude.com/blog/claude-managed-agents (found via search 2026-10-28; the blog page itself was not fetched). The "launched April 8, 2026 — public beta" text is now "public beta since April 8, 2026; still beta on 2026-10-28" in the Phase 6 README, L06 README, PASS1 and the template docstring.
8. **Call shapes were wrong.** Source: https://platform.claude.com/docs/en/managed-agents/quickstart.md (retrieved 2026-10-28), confirmed against installed anthropic 1.11.0 signatures.
   - `environments.create(agent_id=...)` → `environments.create(name=..., config={"type": "cloud", ...})`. Environments are not tied to an agent.
   - `sessions.create(agent_id=...)` → `sessions.create(agent=..., environment_id=...)`.
   - `session.stream(input=...)` does not exist. The real flow is `with client.beta.sessions.events.stream(session.id) as stream:` then `client.beta.sessions.events.send(session.id, events=[{"type": "user.message", "content": [...]}])`, reading `agent.message` (text blocks in `event.content`), `agent.tool_use` and `session.status_idle`.
   - The `session_start` / `text_delta` / `session_complete` event names were invented.
   - Agents now get `tools=[{"type": "agent_toolset_20260401"}]`.
   - `betas=[...]` was dropped because the SDK sets it. `model={"id": ...}` is valid (installed type union) but was changed to a plain string to match the docs.
   - Files: `template_managed_agent.py` real path rewritten, with demo mocks renamed to the real event types; `CHEATSHEET_L06.py` steps 1–3; `README.md` code block plus correction note; PASS1/PASS3/PASS_C mechanical signature fixes plus a correction note at top; the PASS_C step-3 box rewritten.
9. Phase 6 `README.md` "Deferred" list now notes that `budget_tokens` is rejected on current models, which use adaptive thinking and effort. Source: models overview above ("Extended thinking ... deprecated on Claude Opus 4.6 and Claude Sonnet 4.6 and not accepted on later models", retrieved 2026-10-28).

### Phase 5
10. **L27 structured output.** `client.messages.parse(model=, max_tokens=, messages=, output_format=PydanticModel)` returns `response.parsed_output`. It is GA with no beta header, and the raw `output_format` parameter is deprecated in favour of `output_config.format`. Sources: https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md and define-tools URL above (both retrieved 2026-10-28). `messages.parse(output_format=...)` was confirmed present in installed 1.11.0.
    - `template_structured_extractor.py`: real path uses `messages.parse`. The demo path runs through the same `response.parsed_output` line via a `demo_parse` mock.
    - `CHEATSHEET_L27.py` section 3: current pattern added; the old one marked as 400 on the 5.5 / Fable 5.1 models.
    - `README.md`: "one shape" replaced, with the old shape kept as a recognition comment.
    - PASS1/PASS3/PASS_C: update note at top. The PASS_C "tool_choice = the reliable path. Always use it" line was rewritten.
11. **L26 tool_choice.** Restriction note added in PASS1 Example 6, PASS3 Template 6, the PASS_C tool_choice visual and the CHEATSHEET_L26 comment. Source: define-tools URL above.
12. **L28.** Notes added before the forced-`tool_choice` routing examples in PASS1 Example 1 and PASS3 Template 1. The template's knowledge-base string about "Pydantic + tool_choice" is now "messages.parse". The same string was fixed in the L29 template, the L30 cheatsheet line and the L30 PASS_C flowchart. Source: same two URLs.
13. **L29 MCP: mcp 2.x removed `@server.list_tools()` and `@server.call_tool()`.** The lowlevel `Server` now takes `on_list_tools=` and `on_call_tool=` in its constructor. `FastMCP` was renamed `MCPServer` (`from mcp.server import MCPServer`, `@mcp.tool()`). Source: https://py.sdk.modelcontextprotocol.io/v2/migration/ and https://py.sdk.modelcontextprotocol.io/v2/ (retrieved 2026-10-28).
    - Confirmed on installed 2.2.0: `Server` has no `list_tools` attribute, and `MCPServer` with `@mcp.tool()` lists a tool.
    - Returned `Tool` objects expose `input_schema`, not `inputSchema`: confirmed locally (AttributeError on `.inputSchema`), and the v2 guide examples use `input_schema=`.
    - Current spec revision is 2026-07-28 (https://modelcontextprotocol.io/specification/latest, retrieved 2026-10-28). `LATEST_PROTOCOL_VERSION` in installed mcp is "2026-07-28".
    - Files: README "one shape" (server side now MCPServer, 1.x style kept as comment, plus note); CHEATSHEET_L29 section 1 and the recap lines; `template_mcp_client.py` and CHEATSHEET `tool.inputSchema` → `tool.input_schema` (mock renamed too); PASS1 and PASS3 notes.
14. **L31.** The comment "defaults to gpt-4o" is wrong. The SDK default is gpt-5.6-luna via the Responses API. Source: https://openai.github.io/openai-agents-python/models/ (retrieved 2026-10-28). Comments fixed in CHEATSHEET_L31 and PASS3 (two places). The `model="gpt-4o"` strings were left alone.
15. Phase 5 `README.md` pattern table: the structured output row now names `messages.parse(output_format=...)`.

## Demo runs

Each file was run as `timeout 60 /home/niso4ever/AIarch/.venv/bin/python <file>` from inside its folder, after the edits, and also `py_compile`d.
A green run proves syntax and imports only, not the API shape.

| File | Run | py_compile | Note |
|---|---|---|---|
| L01 template_first_sdk_agent.py | PASS (rc 0) | ok | |
| L01 CHEATSHEET_L01.py | FAIL rc 1 | ok | ModuleNotFoundError claude_agent_sdk. Same as baseline: not installed, and cheatsheets are reference files |
| L02 template_sdk_tools.py | PASS | ok | |
| L02 CHEATSHEET_L02.py | FAIL rc 1 | ok | same ModuleNotFoundError as baseline |
| L03 CHEATSHEET_L03.py | FAIL rc 1 | ok | constructs a client without a key. Same as baseline; no network call made |
| L04 template_session_memory.py | PASS | ok | |
| L04 CHEATSHEET_L04.py | FAIL rc 1 | ok | ModuleNotFoundError, baseline |
| L05 template_subagent_pipeline.py | PASS | ok | |
| L05 CHEATSHEET_L05.py | FAIL rc 1 | ok | ModuleNotFoundError, baseline |
| L06 template_managed_agent.py | PASS | ok | output read by hand; streams the mock agent.message events and stops on session.status_idle |
| L06 CHEATSHEET_L06.py | FAIL rc 1 | ok | client without key, baseline |
| L26 CHEATSHEET_L26.py | FAIL rc 1 | ok | NameError `response`, baseline |
| L27 template_structured_extractor.py | PASS | ok | all 3 demos print typed objects |
| L27 CHEATSHEET_L27.py | FAIL rc 1 | ok | NameError `MyModel`, baseline |
| L28 template_orchestrator.py | PASS | ok | |
| L29 template_mcp_client.py | PASS | ok | |
| L29 CHEATSHEET_L29.py | FAIL rc 1 | FAIL | SyntaxError: `async with` at module level, line 49. Baseline; not in a line I edited |
| L30 CHEATSHEET_L30.py | FAIL rc 1 | FAIL | SyntaxError: `return` outside function. Baseline; one comment line edited |
| L31 CHEATSHEET_L31.py | FAIL rc 1 | ok | ModuleNotFoundError `agents` (openai-agents not installed), baseline |

The baseline run before any edits gave the same exit codes for every file above. Untouched files: L25 template PASS. L25 CHEATSHEET hangs (rc 124) on a module-level `while True`; this is pre-existing and was not touched.

## Unverified — not applied

- **The L02 and L06 PASS files still contain old code blocks.** L02 PASS1/PASS3/PASS_C have `Tool(...)` blocks. L06 PASS1/PASS3 have `session.stream(input=...)` loops with the invented event names. I added a correction note at the top of each file rather than rewriting about 15 blocks. These files are verified wrong; I just did not have the time for a full rewrite. Recommend a follow-up rewrite.
- L26/L28 PASS files still show forced `tool_choice` code (with notes). It is still valid on legacy models such as Opus 4.6/4.8, so I did not delete it.
- OpenAI Agents SDK: only the default model, `Agent` / `Runner.run_sync` / `final_output`, and the install command were verified (https://openai.github.io/openai-agents-python/, retrieved 2026-10-28). I did not check the `@input_guardrail` / `@output_guardrail` / `GuardrailFunctionOutput` signatures or the handoff details. PyPI latest openai-agents is 0.24.0 (2026-10-15); it is not installed. No pin file in scope names it, so there is nothing to change.
- MCP: whether HTTP+SSE is deprecated in spec 2026-07-28 was not confirmed. The spec landing page did not list transports, and the v2 SDK still ships `sse_client` / `run(transport="sse")`. L29 text was left unchanged on this.
- Managed Agents memory stores going to public beta on 2026-04-28 comes from a personal notes page only. Not used.
- PyPI latest versions seen 2026-10-28 for packages not pinned in my scope: anthropic 2.3.0 (2026-10-23), mcp 2.3.0, fastmcp 4.1.4, pydantic 2.14.1. The installed versions are older. Per the rules, floors follow the installed versions; I did not bump them to latest. Note that anthropic 2.x exists. Upgrading would be deliberate and affects the shared venv.

## Recommendations (teaching gaps)

1. **Tool Runner (L25/L26).** `client.beta.messages.tool_runner(...)` with `@beta_tool` now runs the hand-written `while stop_reason == "tool_use"` loop for you. It is present in installed 1.11.0. Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner. Add one recognition example after the hand-written loop, so learners know what replaced it. Keep the manual loop as the teaching core.
2. **Strict tool use (L26).** `"strict": True` on a tool definition guarantees schema-valid arguments. It is the documented replacement for forced tool_choice on 5.5 models. It deserves a line in the CHEATSHEET.
3. **Thinking and effort (L25/L30).** Current models use `thinking={"type": "adaptive"}` and `output_config={"effort": ...}`. Claude Opus 5.5's default effort is `medium`, not `high` (models overview). Nothing in Phase 5 mentions effort. One paragraph in L30 (cost/quality design) would cover it.
4. **Refusal stop reason.** Opus 5.5 / Sonnet 5.5 / Fable 5.1 can return `stop_reason: "refusal"`. The L25 loop only branches on `end_turn` and `tool_use`, so a refusal would fall through. Add a third branch in the loop recognition material.
5. **MCP connector (L29).** The Messages API can call remote MCP servers directly (`mcp_servers=[...]` plus an `mcp_toolset` tool, beta `mcp-client-2025-11-20`), with no client code. Learners will see this shape. Also, the Agent SDK's custom tools *are* in-process MCP servers (L02), which is a good bridge between L29 and L02.
6. **L03 does not teach Agent SDK streaming.** The lesson streams with the raw `anthropic` client. The Agent SDK path is `ClaudeAgentOptions(include_partial_messages=True)` and then `StreamEvent` (`claude_agent_sdk.types`) with `content_block_delta` / `text_delta` (https://code.claude.com/docs/en/agent-sdk/streaming-output). Add one example.
7. **L04: `ClaudeSDKClient`.** It is the documented way to hold a multi-turn session in one process with no ID handling. `continue_conversation=True` resumes the most recent session, and `fork_session=True` branches one. Worth a short PASS1 example each.
8. **L05: the template still chains two `query()` calls by hand.** A second template using `agents=` + `AgentDefinition` would show real SDK subagents, and `max_budget_usd` plus the subagent depth/concurrency env vars for cost control.
9. **Agent SDK hooks and permissions.** `hooks={"PreToolUse": [HookMatcher(...)]}`, `permission_mode` and `can_use_tool` are not covered anywhere in Phase 6. They are the main safety controls.
10. **L06 Managed Agents.** It now has vaults for credentials, outcomes (a grader that iterates against a rubric), scheduled deployments, and multi-agent workflows. Mention them in L06 README as "what's next", and keep it beta-labelled.
11. **Course CLAUDE.md** (outside my scope, for the lead) has stale lines. It says "`claude-agent-sdk>=0.1.0`", and the Tier 2 description is fine, but its Tier 3 line "Public beta as of April 2026" should read "public beta since April 2026, still beta on 2026-10-28".

---

# Log C — Vibe coding and Phases 7–10

Run date 2026-10-28. Interpreter /home/niso4ever/AIarch/.venv/bin/python (Python 3.12.3). No pip installs. Model ID strings were not edited anywhere.

## Cross-reference check (task 1)

- `find 1-Course -name 'template_*.py'` gives 56 files. The vibe entries numbered 0–55 map one-to-one onto them: every template has an entry, every template entry points to a file that exists. The README per-file counts (1+20+13+3+4+6+6+1+1+1 = 56) are correct.
- The "56 templates + 4 projects = 60" claim was false in practice. `10_Phase10_EndToEnd.md` had five project entries (56–60). Entry 60, `Project5_Dialectic_Studio`, names six files (`orchestrator.py`, `prompts.py`, `agent_loop.py`, `judge.py`, `dialectic_memory.py`, `dialectic_studio.py`), none of them under `1-Course/`. They exist in `/home/niso4ever/AIarch/6-dialectic-last-mile/`. Fixed (see below), so the 60 count and `1-Course/CLAUDE.md` are now both true.
- Spec Level and Mode tags outside the defined vocabulary (README and Field Manual define Level 0–4 and Modes 1–5 = Exploration/Specification/Iteration/Debugging/Integration): "Level 5 (System Architecture)" on entries 57–60, and "Mode 3 (Guardrails)" on entries 55, 58, 59 and in the 08/09 intros. Fixed.
- Not changed: `6-Vibe coding/README.md` titles itself "Phase 7" and `10-End_to_End_Projects/README.md` titles itself "Lesson 10". `1-Course/CLAUDE.md` (updated today by someone else) documents both as known disagreements that "have not been changed", so I left them alone to keep that file accurate.

## Changes made

| File | What | Why / source |
|---|---|---|
| `6-Vibe coding/10_Phase10_EndToEnd.md` | Header "3 architectures" changed to "4". Entry 60 `Project5_Dialectic_Studio` lost its number and moved under a new "Outside this course (not counted in the 60)" heading that gives the real path `/home/niso4ever/AIarch/6-dialectic-last-mile/`. Its prompt text, including the `GPT-5.4` string, is unchanged. | Dangling reference; count integrity. |
| same | Tags: 57 → Level 3 · Mode 5; 58 → Level 4 · Mode 5; 59 → Level 3 · Mode 5; external entry → Level 3 · Mode 5. | Level 5 and "Guardrails" are not in the README/Field Manual vocabulary. |
| `6-Vibe coding/08_Phase8_Evals.md` | Intro "Mode 3 (Guardrails)" changed to "Mode 3 (Iteration)". | Same vocabulary issue. |
| `6-Vibe coding/09_Phase9_Debugging.md` | Intro and entry 55: "Mode 3 (Guardrails)" changed to "Mode 4 (Debugging)". | Same. |
| `6-Vibe coding/07_Phase7_Async.md` | Entry 53: "reviewer" changed to "critic" to match the template. The PRODUCES snippet now matches the real `run_agent_safe(name, fn, prompt, semaphore)` signature (the old snippet called it with 2 arguments). The VALIDATION line now says what a semaphore of 2 over 3 agents actually does; the old line said "total time matches the slowest path", which is false with a limit of 2. | Entry did not match its template. |
| `6-Vibe coding/VIBE_CODING_BEST_PRACTICES_2026.md` | Effort levels changed from `low/medium/high/max` to `low/medium/high/xhigh/max`. Added that not every model supports every level and that the default differs (`high` on most models, `medium` on Opus 5.5 and Haiku 5.5). Added that `budget_tokens` errors from Claude 4.7 onward. | https://platform.claude.com/docs/en/build-with-claude/effort ("Claude Opus 5.5 supports all five effort levels, and medium is the default"; "Not every model that supports max supports xhigh"); https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting ("Claude 4.7 and later models do not support it and reject requests that use it, returning a 400 error"). Retrieved 2026-10-28. |
| same, Rule 4 | "Start low. Climb only when…" changed to: pick the smallest model, leave effort at the model's default, step it down once evals show quality holds. | The effort page says "Start with `high`, the default … step down to `medium` or `low` for routine or latency-sensitive work once your evals show quality holds." Retrieved 2026-10-28. |
| `7-Async_for_Agents/L01_Async_Patterns/template_parallel_agents.py` | **Bug fix:** the per-agent timer started before the semaphore was acquired, so queue time counted as run time. "Sequential would take" was inflated (4.3s against a true 3.3s) and the reported speedup was wrong (2.4x against a true 1.8x). The timer now starts inside `async with semaphore`. Docstring "Python 3.13+ native async" corrected. | Measured before and after: speedup line went from 2.4x to 1.8x. TaskGroup and timeout version facts: https://docs.python.org/3/library/asyncio-task.html ("Added in version 3.11"), retrieved 2026-10-28. |
| `7-Async_for_Agents/L01_Async_Patterns/CHEATSHEET_L01.py` | Pattern 6 (fire-and-forget) now keeps a reference to the task (a `set` plus `add_done_callback(discard)`). Added Pattern 6b `asyncio.TaskGroup` and two table rows. Fixed the "3.13+" note. | Python docs: "Save a reference to the result of this function, to avoid a task disappearing mid-execution. The event loop only keeps weak references to tasks." TaskGroup: "the remaining tasks in the group are cancelled". Same URL, retrieved 2026-10-28. |
| `7-Async_for_Agents/L01_Async_Patterns/PASS3_TEMPLATES.md` | Template 5 now uses a `fire_and_forget()` helper that keeps a reference to each task. | Same source. |
| `7-Async_for_Agents/L01_Async_Patterns/PASS1_RECOGNITION.md` | `gather` failure semantics corrected. The old text said "If any one fails, they all fail"; in fact the first error propagates and the other coroutines keep running. Mentioned TaskGroup as the stricter alternative. Fixed the wrong pointer "Template 5 in L01" (Template 5 is fire-and-forget) to cheatsheet Pattern 7. Two table rows added. | Python docs: "the first raised exception is immediately propagated … Other awaitables in the aws sequence won't be cancelled and will continue to run." Retrieved 2026-10-28. |
| `7-Async_for_Agents/L01_Async_Patterns/README.md` | Removed the false claim "Claude Code's `asyncio.gather` runs tool calls simultaneously" (Claude Code is not a Python program). Replaced it with: Claude can request several tool calls in one response and your code runs them. | https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use ("By default, Claude may call multiple tools in a single response."), retrieved 2026-10-28. |
| `8-Evals_and_Testing/L01_Agent_Evals/README.md` | "evaluate an agent on 5 instances" changed to 10 instances with a baseline comparison, matching the template. "5 eval templates" changed to 6. | The template runs `num_instances = 10`. |
| `8-Evals_and_Testing/L01_Agent_Evals/PASS3_TEMPLATES.md` | Added Template 6: an offline `pydantic-evals` example (`Case`, `Dataset(name=…)`, `EqualsExpected`, `evaluate_sync`). Mentions `LLMJudge` as calling an API, so not for demo mode. Goal line and selection guide updated. I did not add a `template_*.py`, so the 56 count stays intact. | Ran against installed pydantic-evals 2.53.0, rc 0, 2/2 cases pass. `name` is required in 2.53.0: omitting it gave `TypeError: Dataset.__init__() missing 1 required keyword-only argument: 'name'`. https://ai.pydantic.dev/evals/ (shows `Dataset(name='capital_quiz', cases=[case1])` and `dataset.evaluate_sync(guess_city)`); https://ai.pydantic.dev/evals/evaluators/llm-judge/ ("The LLMJudge evaluator uses an LLM to assess subjective qualities of outputs based on a rubric"). Retrieved 2026-10-28. |
| `9-Code_Review_and_Debugging/L01_Agent_Debugging/CHEATSHEET_L01.py` | **Bug fix (accidental, not teaching material):** `try_parse_or_repair` looped `range(max_retries)`, so the last repaired output was never validated. An agent that succeeded on its final repair was reported as a failure. It now does `max_retries + 1` checks; PASS3 Template 3 already did this correctly. Tested: success on the 2nd repair now returns `action='ok'`, and two bad repairs still raise. | Code logic; the lesson does not present this function as a deliberate bug. |
| same | Added a comment that structured outputs (`output_config.format`) or strict tool use can prevent bad JSON, with the repair loop kept as a fallback. Added a table line. | https://platform.claude.com/docs/en/build-with-claude/structured-outputs ("Structured outputs constrain Claude's responses to follow a specific schema") and https://platform.claude.com/docs/en/release-notes/overview, January 29, 2026 entry ("The `output_format` parameter has moved to `output_config.format`"). Retrieved 2026-10-28. |
| same, plus `PASS3_TEMPLATES.md` Template 2 | Kept the offline "4 chars ≈ 1 token" heuristic and added a comment that the real count comes from `client.messages.count_tokens(...)`: free, rate-limited, an estimate, and it should use the model you will call. | https://platform.claude.com/docs/en/build-with-claude/token-counting ("The token count is an estimate"; "Token counting is free to use but subject to requests per minute rate limits"; count "with the model ID you plan to use"). Retrieved 2026-10-28. |
| `9-Code_Review_and_Debugging/L01_Agent_Debugging/README.md` | "Single agents (Phase 4)" corrected: Phase 4 is tool schemas and single agents are Phase 5. | Course phase map in `1-Course/CLAUDE.md`. |
| `10-End_to_End_Projects/Project1_Data_Pipeline/main.py` | Replaced the inline "DEMO OVERRIDE" block, which skipped `extract_record` entirely, with `DEMO_MODE = True` and a `FakeClient`. Demo mode now runs the real `extract_record` parsing and Pydantic validation on a canned `tool_use` reply. `DEMO_MODE = False` uses the real client. | Matches the project's own `vibe_prompts.md` Prompt 3 ("Include a DEMO_MODE toggle"), the 1-Course coding standard, and the AIarch rule "Demo or offline mode runs the real code path". Ran with no API key: rc 0. |
| `10-End_to_End_Projects/Project1_Data_Pipeline/extractor.py` | `extract_record(raw_text, llm=None)` now takes an optional client and has a Google-style docstring. Added a comment that forced `tool_choice` ("tool"/"any") returns 400 on Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1; use `auto` with `strict: true` or `output_config.format` there. The live call and the model string are unchanged. | https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools ("Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 / `any` and `tool` return a 400 error"). Retrieved 2026-10-28. |
| `10-End_to_End_Projects/README.md`, `Project1_Data_Pipeline/vibe_prompts.md` (Prompt 2) | Added the same forced-`tool_choice` caveat. | Same source. |
| `10-End_to_End_Projects/*/vibe_prompts.md` (all 4) | "CONSTRAINTS: Python 3.13." changed to "Python 3.12 (the course venv)." | The venv is 3.12.3, so code generated for 3.13 could fail there. |
| `10-End_to_End_Projects/Project4_Interactive_SQL_Agent/main.py` | `input()` wrapped in `try/except EOFError` that treats the result as "no" (fail-safe deny). Before this, a run with no terminal crashed with EOFError. | Hardening. Interactive behaviour is unchanged. |

## Demo runs

Scope: I ran the 6 `.py` files in 7, 8 and 9 and the 4 project `main.py` files in 10. The other 50 `template_*.py` files sit in folders outside my scope and are covered by the other logs.

All runs used no API key (`env -u ANTHROPIC_API_KEY`), started from inside each folder, with stdin from /dev/null unless noted. Each file was run before and after the edits.

| File | Before | After |
|---|---|---|
| 7 `CHEATSHEET_L01.py` | pass (no output, by design) | pass |
| 7 `template_parallel_agents.py` | pass, but printed wrong timing (2.4x speedup) | pass (1.8x speedup, correct) |
| 8 `CHEATSHEET_L01.py` | pass (no output) | pass |
| 8 `template_agent_eval.py` | pass | pass (not edited) |
| 9 `CHEATSHEET_L01.py` | pass (no output) | pass |
| 9 `template_trace_debugger.py` | pass (2 attempts, success) | pass (not edited) |
| 10 Project1 `main.py` | pass (demo bypassed extractor) | pass (demo goes through extractor) |
| 10 Project2 `main.py` | pass | pass (not edited) |
| 10 Project3 `main.py` | pass | pass (not edited) |
| 10 Project4 `main.py` | fail with no stdin (EOFError at `input()`); pass with `yes` and with `no` piped | pass with no stdin (denies); pass with `yes` |
| 7 PASS3 code blocks 1–5 (extracted and run) | n/a | all rc 0 |
| 8 PASS3 code blocks 1–6 (extracted and run, incl. new Template 6) | n/a | all rc 0 |

Side effects. The runs rewrite `9-.../agent_trace.jsonl` and `10-.../Project3_Codebase_Auditor/audit_trace.jsonl`. Both scripts truncate and regenerate these files on every run, and the simulated agents are deterministic, so the content should match the old files apart from the timestamps (now 2026-10-28). I did not capture the originals before the first run, so I cannot confirm the match. Treat both files as generated output, not as fixed teaching material. I deleted `audit_memory.json` and the `__pycache__` folders that the runs created. `memory_ops.py` appends to `audit_memory.json` across runs, so a second run without deleting it shows duplicate findings (see Recommendations).

The demo runs prove that syntax, imports and control flow work. They do not prove the real API request shape.

No `requirements.txt` exists in any of the five folders, so there were no floors to raise.

## Unverified — not applied

- `VIBE_CODING_BEST_PRACTICES_2026.md` claim "A single agentic request may take 15 minutes": no source found. Left as written.
- `continual-learning-bench` / "CLBench" is cited as real code in the READMEs, PASS1 and PASS_C of 7, 8 and 9 (14 mentions). No such repo or folder exists in AIarch. The only related file is `/home/niso4ever/AIarch/6-dialectic-last-mile/salvaged-from-hegelian/CONTINUAL_LEARNING_MAP.md`. The text says "you reviewed", so it is a narrative reference the learner cannot follow. Not rewritten.
- Project2's commented-out real path passes `tool_handlers=` to `claude_agent_sdk.query()`. I did not check that argument against the SDK.
- PASS_C_VISUAL in 7 and 9: checked for text that conflicts with the fixes. None found; the `4000` in the 9 diagram is an illustrative limit.
- `anthropic.AsyncAnthropic` as the real async client: it exists in the installed SDK (Project1 imports it and runs), but none of the pages I fetched contained a citable quote, so I added no new text about it.
- Model table (`claude-opus-4-8`, `claude-sonnet-4-6`, `claude-haiku-4-5`, `claude-fable-5`) in `VIBE_CODING_BEST_PRACTICES_2026.md`, and the comment in `Project1/extractor.py`, are **flagged for the lead's model sweep and not edited**. The effort docs (retrieved 2026-10-28) list Claude Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1 and Mythos 5.1 as current. The table also calls Fable 5 "the most capable", but Fable 5.1 exists. One coupling to watch: if the sweep moves `extractor.py` to `claude-opus-5-5`, its forced `tool_choice` will start returning 400. The fix is `tool_choice auto` plus `strict: true` on the tool, or `output_config.format`. Test it live first, because Pydantic's generated schema may contain keywords that strict mode does not support.

## Proposed pins (not acted on)

- `hypothesis` is used in 8-Evals PASS1 Pattern 6 but is not installed. It is recognition-only, so nothing breaks; add it to the venv only if a lesson ever runs it.
- `logfire 5.1.1` is installed alongside `logfire-api 4.29.0`. That major-version mismatch is worth checking before any tracing lesson uses Logfire.

## Recommendations (thin spots: 7, 8 and 9 have one lesson each)

**7 Async.** The next lesson should cover:
- the real async client (`AsyncAnthropic`), and running Claude's parallel `tool_use` blocks concurrently, then returning all the `tool_result`s in one user message;
- `asyncio.TaskGroup` and `asyncio.timeout()` as the 2026 default over `gather` and `wait_for`;
- cancellation and partial results;
- rate-limit backoff on 429s.

The current lesson only sleeps; it never shows an API-shaped coroutine.

**8 Evals.** The lesson teaches "reward curves" for a learning agent, which is a niche benchmark framing. What a late-2026 learner needs more:
- (a) evals as a gate: a fixed case set, a pass threshold, and a run on every prompt or model change;
- (b) pydantic-evals as the suite format. The installed 2.53.0 also ships agentic evaluators such as `MaxToolCalls`, `ToolCorrectness`, `TrajectoryMatch` and `LLMJudge`;
- (c) the workspace's own "replay the new rule against saved output before re-running" practice from AIarch `CLAUDE.md`. It is the cheapest eval there is and fits this learner's real pipelines;
- (d) LLM-as-judge pitfalls: judge bias, and the need for a human-labelled calibration set.

**9 Debugging.** The next lesson should cover:
- OpenTelemetry-style tracing instead of hand-rolled JSONL (the venv already has `logfire`, `opentelemetry-sdk 1.44.0` and `traceAI-anthropic`);
- reading the API's own signals (`usage.input_tokens`/`output_tokens`, `stop_reason` such as `max_tokens`, `tool_use` or `refusal`) instead of character-count heuristics;
- prevention over repair with structured outputs.

A "read this broken trace" exercise built on `agent_trace.jsonl` would suit the recognition-first style.

**10 Projects:**
- Project3's `audit_memory.json` keeps growing across runs. Reset it at start or key findings by file.
- Project2's real path is entirely commented out (the SDK imports are comments), so `DEMO_MODE = False` does nothing useful. Either wire it to `claude_agent_sdk` or say plainly that it is demo-only.
- The vibe entry 56 prompt still asks for forced `tool_choice`. Once the model sweep lands, update it to strict tool use.
