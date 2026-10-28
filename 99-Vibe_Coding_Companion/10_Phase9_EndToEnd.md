# Phase 9 — End-to-End Projects (Ph9-L01, 4 architectures)

The capstone of the multi-agent landscape. In this phase, we move beyond single files and summon entire decomposed architectures. These prompts heavily utilize **Mode 5 (Integration)**, demonstrating how an AI Architect directs the generation of interfaces, agents, and orchestrators in sequence.

---

## 56. `Project1_Data_Pipeline` — Raw API Integration
**Level 3 (Contract) · Mode 5 (Integration)** — Pure determinism, no agents.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Pydantic schema for `CustomerRecord`. Use the Anthropic `AsyncAnthropic` client.
REQUEST: Build an async data pipeline.
  Step 1: Create `schema.py` defining the strict data structures.
  Step 2: Create `extractor.py` containing an LLM call that forces the model to use `tool_choice` matching the schema. (Forced `tool_choice` returns 400 on Opus 5.5 / Sonnet 5.5 / Fable 5.1, per the define-tools docs retrieved 2026-10-28; on those models ask for `client.messages.parse(output_format=Schema)` instead.)
  Step 3: Create `main.py` that processes a batch of raw strings concurrently using an `asyncio.Semaphore`.
VALIDATION: The orchestrator parses the strings into strict JSON, catching any validation errors without looping or hallucinating.
```
#### 💻 PRODUCES (essence)
*(Creates a 3-file architecture where `main.py` imports `extract_record` and gathers results concurrently.)*

---

## 57. `Project2_Research_Synthesizer` — Agent SDK Orchestration
**Level 3 (Contract) · Mode 5 (Integration)** — Delegating the loop to the SDK.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Anthropic Agent SDK. `DEMO_MODE=True` for simulated runs.
REQUEST: Build a multi-agent synthesizer.
  Step 1: Create `tools.py` with mock web search functions.
  Step 2: Create `agents.py` with a `run_researcher` agent that uses the tools and returns structured JSON, and a `run_synthesizer` agent that takes the JSON and writes a report.
  Step 3: Create `main.py` to launch 3 researchers in parallel via `gather`, then pass their combined output to the synthesizer.
VALIDATION: Clean handoff (JSON out -> prompt context in). Parallel execution of subagents.
```
#### 💻 PRODUCES (essence)
*(Creates a 3-file architecture highlighting how output of Agent A becomes the context of Agent B.)*

---

## 58. `Project3_Codebase_Auditor` — Custom Agent Loop & Evals
**Level 4 (Test Cases) · Mode 5 (Integration)** — Deep observability and self-correction.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Custom `while True` loop. Async I/O locks. Pydantic validation.
REQUEST: Build a self-correcting codebase auditor.
  Step 1: Create `trace_logger.py` to record every step to a .jsonl file.
  Step 2: Create `memory_ops.py` with an `asyncio.Lock()` for safe file writes.
  Step 3: Create `eval_loop.py` that runs the agent, catches `ValidationError`, logs it, and injects a dialectic repair prompt.
  Step 4: Create `main.py` to orchestrate multiple file audits simultaneously.
VALIDATION: The agent must successfully repair broken JSON on the second attempt, and the logger must capture the exact reasoning trace of the failure and recovery.
```
#### 💻 PRODUCES (essence)
*(Creates a 4-file architecture showing how to implement CLBench-style state machines and repair loops.)*

---

## 59. `Project4_Interactive_SQL_Agent` — Human-in-the-Loop (HITL)
**Level 3 (Contract) · Mode 5 (Integration)** — Pausing execution for human permission.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Custom exception handling.
REQUEST: Build an Interactive SQL Agent.
  Step 1: Create `tools.py` with safe queries and destructive queries. Destructive queries must require a confirmation token, raising `HumanApprovalRequired` otherwise.
  Step 2: Create `agents.py` with an agent that attempts a destructive query, allowing the exception to bubble up, but capable of resuming when passed the token in context.
  Step 3: Create `main.py` that orchestrates the agent, catches the exception, prints a warning to the console, uses `input()` to get a "yes/no" from the user, and resumes the agent with the token if approved.
VALIDATION: The agent successfully suspends itself before executing a destructive action, and cleanly resumes based on human feedback.
```
#### 💻 PRODUCES (essence)
*(Creates a 3-file architecture proving you can hard-stop an agent before it drops a database table.)*

---

## Outside this course (not counted in the 60)

The entry below describes a project that is **not** in `1-Course/`. Its files
(`orchestrator.py`, `prompts.py`, `agent_loop.py`, `judge.py`,
`dialectic_memory.py`, `dialectic_studio.py`) live in
`/home/niso4ever/AIarch/6-dialectic-last-mile/`. It is kept here as a worked
example of a larger prompt chain; it has no template in this course to compare against.

### `Project5_Dialectic_Studio` — Hegelian Dialectic Agent (external)
**Level 3 (Contract) · Mode 5 (Integration)** — Complex reasoning loops, ensemble judging, and interactive UI.

#### 📝 VIBE PROMPT
```text
CONSTRAINTS: Pydantic v2 schemas. Direct Messages API (no Agent SDK). Streamlit UI. DEMO_MODE toggle.
REQUEST: Build a Hegelian Dialectic Studio that answers contested questions.
  Step 1: Create `orchestrator.py` to define the data contracts and tool schemas. Use Pydantic v2 `BaseModel`s configured for strict Anthropic tool-use (`additionalProperties=False`) to enforce the exact JSON shape of the `emit_dialectic` output (bullets, confrontation matrix, binding constraint) and the `web_search` skill.
  Step 2: Create `prompts.py` to isolate the large system prompts. The prompt must force the LLM to act as a Hegelian dialectic engine, demanding a concrete thesis, antithesis, binding constraint, and an operational synthesis (aufhebung), while strictly forbidding abstract or metaphorical prose.
  Step 3: Create `agent_loop.py` to implement a `while True` loop interacting directly with the Anthropic Messages API. It must handle tool dispatch, track prompt caching breakpoints, and provide a fully mocked `DEMO_MODE` path that returns plausible canned responses for zero-cost UI testing.
  Step 4: Create `judge.py` to implement a cross-model ensemble evaluator (defaulting to a different model like GPT-5.4 to reduce self-bias). It must score K candidate dialectics across 4 strict dimensions: binding constraint capture (identifying true deal-killers), verdict decisiveness, groundedness, and coverage, returning the single best candidate.
  Step 5: Create `dialectic_memory.py` to manage a file-based structural memory store (`memory/` and `exemplars/`). It must persist previously discovered deal-killers, verified facts, and transcendence moves on a per-topic basis, dynamically injecting them back into the orchestrator's prompt.
  Step 6: Create `dialectic_studio.py` to build the Streamlit frontend. It must manage the execution loop across multiple threads to keep the UI responsive, rendering the final output through specialized visual components like a bipartite confrontation matrix, citation trees, and ensemble scorecards.
VALIDATION: The UI launches and operates flawlessly in DEMO_MODE with zero cost. In live mode, it successfully calls the web and emits a structured Hegelian dialectic response without hallucinating schema properties.
```
#### 💻 PRODUCES (essence)
*(Creates a 6+ file hyper-architecture demonstrating state-of-the-art prompt caching, strict output constraints, and Streamlit UI integration.)*
