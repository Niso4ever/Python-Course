# Phase 9: End-to-End Projects (Vibe Coding)

Welcome to the capstone. You know how to read agent code, you know how to write individual components, and you know how to debug them. 

Now, you are the **AI Architect**. Your job is to design the entire system, break it down into manageable pieces, and direct an AI (via Vibe Coding) to build it for you.

## The Architect's First Decision: Choose Your Engine

Before you write a single prompt, you must choose the underlying engine for your project. Choosing the wrong engine leads to slow, flaky, or overly complex code.

### 1. The Raw API (No Agents)
* **When to use:** Data pipelines, structured extraction, deterministic tasks.
* **Why:** You need 100% reliability. Agents hallucinate and loop; raw API calls constrained to a schema do not.
* **2026 note:** The project forces the schema with `tool_choice={"type": "tool"}`. The newest Claude models (Opus 5.5, Sonnet 5.5, Fable 5.1, Mythos 5.1) reject forced `tool_choice` with a 400 error; on those, use strict tool use (`strict: true`) or structured outputs (`output_config.format`) instead. See the comment in `extractor.py`.
* **See:** `Project1_Data_Pipeline/`

### 2. The Agent SDK
* **When to use:** Multi-step reasoning, external tool use (search, APIs), and parallel tasks.
* **Why:** You don't want to write the `while True` loop yourself. The SDK handles tool dispatch, memory, and routing automatically.
* **See:** `Project2_Research_Synthesizer/`

### 3. The Custom Agent Loop
* **When to use:** Complex state machines, file I/O operations, self-correction (repair loops), and situations requiring deep observability (trace logs).
* **Why:** Standard SDKs hide the loop. If you need to catch a `ValidationError`, inject a custom prompt, and retry, you must own the loop yourself.
* **See:** `Project3_Codebase_Auditor/`

### 4. The Human-in-the-Loop (HITL) Agent
* **When to use:** Destructive operations (DROP TABLE, DELETE, payment processing, sending emails).
* **Why:** You want the autonomy of an agent, but require a hard stop for a human to review the tool arguments before it actually executes.
* **See:** `Project4_Interactive_SQL_Agent/`

---

## How to Read These Projects

Each project folder is decomposed the way an AI Architect designs systems:

1.  **`schema.py` or `tools.py`**: The contracts. Always build these first.
2.  **`agents.py` or `extractor.py`**: The logic. Built second.
3.  **`main.py`**: The orchestrator. Built last, wiring it all together.
4.  **`vibe_prompts.md`**: The exact prompts you would copy/paste into Claude or Gemini to generate these files from scratch.

> [!TIP]
> **The Secret to Vibe Coding:** Never ask the AI to "build a research app." Ask it to build `schema.py`. Then ask it to build `tools.py` using `schema.py`. Then ask it to build `main.py` using the tools. Decomposition is your superpower.
