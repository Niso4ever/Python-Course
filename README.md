# Python Course for AI Architects

A course in reading and directing AI-written Python, aimed at building AI agents. It assumes no coding background. You learn to recognise the patterns in AI code, check them, and tell an AI assistant exactly what to build; you are not expected to write everything from scratch.

## Start here

**Read [`Python_Course_Road_Map.md`](Python_Course_Road_Map.md) first.** It explains what to learn deeply, what only to recognise, and the week-by-week order.

Then begin at Phase 1 with [`01-Phase01_Foundation/Lesson0_Setup_and_First_Steps.md`](01-Phase01_Foundation/Lesson0_Setup_and_First_Steps.md).

## The phases

| Phase | Folder | What it covers |
|---|---|---|
| 1 | [`01-Phase01_Foundation`](01-Phase01_Foundation/) | Python basics through AI patterns. 1A (L01–L07): types, lists, logic, loops, functions, classes, reading real code. 1B (L08–L24): imports, errors, async, debugging, tool use, memory, ReAct, DSPy, multi-agent, databases, APIs, serving, vibe coding, PydanticAI, structured outputs, evaluation |
| 2 | [`02-Phase02_Real_Systems`](02-Phase02_Real_Systems/) | Four runnable projects: RAG pipeline, agent with tools, CrewAI multi-agent, DSPy pipeline |
| 3 | [`03-Phase03_Tool_Use`](03-Phase03_Tool_Use/) | Type hints, Pydantic, function calling, tool schemas |
| 4 | [`04-Phase04_Agentic_AI`](04-Phase04_Agentic_AI/) | Agents on the raw Anthropic API: agent loop, tool use, structured output, multi-agent, MCP, system design, OpenAI Agents SDK |
| 5 | [`05-Phase05_Agent_SDK`](05-Phase05_Agent_SDK/) | Claude Agent SDK and Managed Agents |
| 6 | [`06-Phase06_Async`](06-Phase06_Async/) | Running agents in parallel |
| 7 | [`07-Phase07_Evals`](07-Phase07_Evals/) | Testing and evaluating agents |
| 8 | [`08-Phase08_Debugging`](08-Phase08_Debugging/) | Debugging agents from their traces |
| 9 | [`09-Phase09_End_to_End_Projects`](09-Phase09_End_to_End_Projects/) | Four capstone projects |
| — | [`99-Vibe_Coding_Companion`](99-Vibe_Coding_Companion/) | For every template, the prompt you would give an AI to produce it |

## How each lesson works

Most lessons have the same files, read in this order:

1. `PASS1_RECOGNITION.md`: examples to read and recognise, with no writing.
2. `PASS_C_VISUAL.md`: the same ideas as diagrams.
3. `PASS3_TEMPLATES.md` and the `template_*.py` files: working code to copy and adapt.
4. `CHEATSHEET_*.py`: a quick reference to keep open. Some cheatsheets contain deliberate mistakes for you to spot, so they are not meant to run.

## Running the code

You need Python 3.10 or newer.

```bash
pip install anthropic pydantic python-dotenv
cd 04-Phase04_Agentic_AI/L02_Agent_Loop
python template_agent_loop.py
```

Templates run in demo mode with no API key and print simulated output. To make real calls, create a `.env` file containing `ANTHROPIC_API_KEY=...`. Never commit that file. The projects in Phases 2 and 5 list their extra packages in their own `requirements.txt`.

## Currency

Model names, prices and API patterns were checked against Anthropic's documentation on 28 October 2026. The current models are `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5` and `claude-fable-5-1`. These details change, so check [platform.claude.com/docs](https://platform.claude.com/docs) before relying on them.
