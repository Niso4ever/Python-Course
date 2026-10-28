# Phase 1: The Structural Foundation
## Architectural Overview

Welcome to the first phase of your journey as a **Senior AI Architect**. This phase was designed to strip away the complexity of "programming" and focus on the **Materials** and **Blueprints** required to build intelligent systems.

---

## Phase 0 — OOP Fundamentals (Before L06)

**Read this before L06 if you are new to object-oriented programming:**

- **Phase 0: OOP Introduction**
  - Why functions forget and classes remember — the core problem OOP solves.
  - Factory model: Class = blueprint, Instance = product, `self` = this product.
  - 4 building blocks: class declaration, `__init__`, attributes (`self.x`), methods.
  - Three class styles in 2026: standard `class`, `@dataclass`, Pydantic `BaseModel`.
  - Folder: [../00-Phase00_OOP_Introduction/](../00-Phase00_OOP_Introduction/)

---

## Phase 1(A) — Core Foundation (L00–L07)

**Start here if you have zero coding experience:**

- **L00: Python Setup & First Steps**
  - Install Python and set up your development environment.
  - Learn the `print()` function and how Python reads code top-to-bottom.

- **L01: Labels & Types (Drawer & Sticker Theory)**
  - Learn how to store `user_query` and `context_metadata`.
  - Understand the difference between Text (`str`), Numbers (`int`), and dicts.

- **L02: Lists & Collections (Warehouse Theory)**
  - Store multiple items in order (critical for search results, conversation history).
  - Work with lists of dictionaries (metadata storage).

- **L03: Logic Gates (Railroad Switch Theory)**
  - Route an agent's mind based on `intent` or `confidence`.
  - `if/elif/else` for condition checks. `match/case` (Python 3.10+) for routing by name/type.
  - Master the "Indentation Rule" — the law of whitespace ownership.

- **L04: Loops & Iteration (Assembly Line Theory)**
  - Process each item in a collection using `for` loops.
  - Use `while` loops, `break`, `continue`, and `enumerate()`.

- **L05: Functions as Tools (Juicer Theory)**
  - Build reusable "Tools" that take input, process logic, and deliver output.
  - Understand the power of the `return` statement.

- **L06: Classes as Blueprints (Toolbox vs. Tool Theory)**
  - Create "Modules" — reusable blueprints for agents that can remember their own state (`self`).
  - Three styles: standard `class`, `@dataclass` (for config), Pydantic `BaseModel` (for validation).

- **L07: Reading Real AI Code (The Rosetta Stone)**
  - Decode LangChain, CrewAI, and DSPy code using your L01–L06 knowledge.
  - Recognize that 80% of professional AI code is just list manipulation.

---

## Phase 1(B) — Pattern Recognition & Architecture (L08–L24)

- **L08: Import Patterns** — How imports work; packages, modules, aliases
- **L09: Error Reading** — Read tracebacks, diagnose errors, find the fix
- **L10: Import Pattern Deep Dive** — Virtual environments, requirements.txt, sys.path
- **L11: Async Recognition** — async/await, asyncio.gather, parallel API calls
- **L12: Advanced Debugging** — Silent failures, print audits, token budgets
- **L13: Tool Use Pattern** — JSON schema tools, ReAct loop, function calling
- **L14: Memory Stack Architecture** — Context windows, sliding window, vector memory
- **L15: ReAct Reasoning Pattern** — Thought/Action/Observation loop, agent scratchpad
- **L16: DSPy Signature Paradigm** — Input→output signatures, declarative AI, optimizers
- **L17: Multi-Agent Patterns** — Orchestrator/worker, pipeline, fan-out, CrewAI
- **L18: Persistence & Databases**, **L19: Network Requests & APIs**, **L20: Serving Interfaces** (Streamlit) — with cheatsheets and templates
- **L21: Vibe Coding** — Directing AI to write code; system-prompt template
- **L22: PydanticAI Framework**, **L23: Structured Outputs**, **L24: Evaluation Metrics** — shorter reading lessons

---

## Your Learning Path

### Phase 0 — OOP Fundamentals:

| # | File | Path |
|:--|:-----|:-----|
| — | README | [../00-Phase00_OOP_Introduction/README.md](../00-Phase00_OOP_Introduction/README.md) |
| — | Main Lesson | [../00-Phase00_OOP_Introduction/OOP_FUNDAMENTALS.md](../00-Phase00_OOP_Introduction/OOP_FUNDAMENTALS.md) |
| — | Cheatsheet | [../00-Phase00_OOP_Introduction/CHEATSHEET_OOP.py](../00-Phase00_OOP_Introduction/CHEATSHEET_OOP.py) |
| — | Anatomy Template | [../00-Phase00_OOP_Introduction/template_ai_agent_anatomy.py](../00-Phase00_OOP_Introduction/template_ai_agent_anatomy.py) |

### Phase 1(A) Lessons — click to open:

| # | Lesson | Path |
|:--|:-------|:-----|
| L00 | Setup & First Steps | [Lesson0_Setup_and_First_Steps.md](Lesson0_Setup_and_First_Steps.md) |
| L01 | Labels & Types | [Phase1(A)/L01_Labels_and_Types/L01_Labels_and_Types.md](Phase1(A)/L01_Labels_and_Types/L01_Labels_and_Types.md) |
| L02 | Lists & Collections | [Phase1(A)/L02_Lists_and_Collections/L02_Lists_and_Collections.md](Phase1(A)/L02_Lists_and_Collections/L02_Lists_and_Collections.md) |
| L03 | Logic Gates | [Phase1(A)/L03_Logic_Gates/L03_Logic_Gates.md](Phase1(A)/L03_Logic_Gates/L03_Logic_Gates.md) |
| L04 | Loops & Iteration | [Phase1(A)/L04_Loops_and_Iteration/L04_Loops_and_Iteration.md](Phase1(A)/L04_Loops_and_Iteration/L04_Loops_and_Iteration.md) |
| L05 | Functions as Tools | [Phase1(A)/L05_Functions_as_Tools/L05_Functions_as_Tools.md](Phase1(A)/L05_Functions_as_Tools/L05_Functions_as_Tools.md) |
| L06 | Classes as Blueprints | [Phase1(A)/L06_Classes_as_Blueprints/L06_Classes_as_Blueprints.md](Phase1(A)/L06_Classes_as_Blueprints/L06_Classes_as_Blueprints.md) |
| L07 | Reading Real AI Code | [Phase1(A)/L07_Reading_Real_AI_Code/L07_Reading_Real_AI_Code.md](Phase1(A)/L07_Reading_Real_AI_Code/L07_Reading_Real_AI_Code.md) |

### Phase 1(B) Lessons — click to open:

| # | Lesson | Path |
|:--|:-------|:-----|
| L08 | Import Patterns | [Phase1(B)/L08_Import_Patterns/L08_Import_Patterns.md](Phase1(B)/L08_Import_Patterns/L08_Import_Patterns.md) |
| L09 | Error Reading | [Phase1(B)/L09_Error_Reading/L09_Error_Reading.md](Phase1(B)/L09_Error_Reading/L09_Error_Reading.md) |
| L10 | Import Pattern Deep Dive | [Phase1(B)/L10_Import_Pattern_Deep_Dive/README.md](Phase1(B)/L10_Import_Pattern_Deep_Dive/README.md) |
| L11 | Async Recognition | [Phase1(B)/L11_Async_Recognition/README.md](Phase1(B)/L11_Async_Recognition/README.md) |
| L12 | Advanced Debugging | [Phase1(B)/L12_Advanced_Debugging/README.md](Phase1(B)/L12_Advanced_Debugging/README.md) |
| L13 | Tool Use Pattern | [Phase1(B)/L13_Tool_Use_Pattern/README.md](Phase1(B)/L13_Tool_Use_Pattern/README.md) |
| L14 | Memory Stack Architecture | [Phase1(B)/L14_Memory_Stack_Architecture/README.md](Phase1(B)/L14_Memory_Stack_Architecture/README.md) |
| L15 | ReAct Reasoning Pattern | [Phase1(B)/L15_ReAct_Reasoning_Pattern/README.md](Phase1(B)/L15_ReAct_Reasoning_Pattern/README.md) |
| L16 | DSPy Signature Paradigm | [Phase1(B)/L16_DSPy_Signature_Paradigm/README.md](Phase1(B)/L16_DSPy_Signature_Paradigm/README.md) |
| L17 | Multi-Agent Patterns | [Phase1(B)/L17_Multi-Agent_Patterns/README.md](Phase1(B)/L17_Multi-Agent_Patterns/README.md) |
| L18 | Persistence & Databases | [Phase1(B)/L18_Persistence_and_Databases/L18_Persistence_and_Databases.md](Phase1(B)/L18_Persistence_and_Databases/L18_Persistence_and_Databases.md) |
| L19 | Network Requests & APIs | [Phase1(B)/L19_Network_Requests_and_APIs/L19_Network_Requests_and_APIs.md](Phase1(B)/L19_Network_Requests_and_APIs/L19_Network_Requests_and_APIs.md) |
| L20 | Serving Interfaces | [Phase1(B)/L20_Serving_Interfaces/L20_Serving_Interfaces.md](Phase1(B)/L20_Serving_Interfaces/L20_Serving_Interfaces.md) |
| L21 | Vibe Coding | [Phase1(B)/L21_Vibe_Coding/L21_Vibe_Coding.md](Phase1(B)/L21_Vibe_Coding/L21_Vibe_Coding.md) |
| L22 | PydanticAI Framework | [Phase1(B)/L22_PydanticAI_Framework/README.md](Phase1(B)/L22_PydanticAI_Framework/README.md) |
| L23 | Structured Outputs | [Phase1(B)/L23_Structured_Outputs/README.md](Phase1(B)/L23_Structured_Outputs/README.md) |
| L24 | Evaluation Metrics | [Phase1(B)/L24_Evaluation_Metrics/README.md](Phase1(B)/L24_Evaluation_Metrics/README.md) |

---

> [!IMPORTANT]
> A Senior Architect learns by **recognizing patterns** and using **templates**. Reference, don't memorize.
