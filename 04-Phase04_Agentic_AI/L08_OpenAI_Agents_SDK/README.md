# Lesson 24: OpenAI Agents SDK
## The Light Framework — Same Patterns, Less Code

> **Why this lesson exists:** After mastering the raw Anthropic API (L02–L07), you can now read any agentic code. This lesson shows you the OpenAI Agents SDK — the lightest official framework — so you can recognize it, direct AI to use it, and know when to choose it over raw API calls.

## What the OpenAI Agents SDK Is

The OpenAI Agents SDK is Anthropic's equivalent built by OpenAI — a thin, official wrapper around the same THINK → ACT → OBSERVE loop you already know. It hides the while loop inside `Runner.run_sync()` and turns tool schemas into Python decorators.

```
RAW API (L02–L06):                     OPENAI AGENTS SDK (L08):
══════════════════════════════════════════════════════════════
You write: while True: ...         →   Runner.run_sync(agent, msg)
You write: {"name": ...,           →   @function_tool
            "input_schema": {...}}      def tool_name(param: type) -> str:
You write: run_specialist(task)    →   Agent(handoffs=[specialist])
You write: if not validate(input)  →   @input_guardrail
```

**Same patterns. Different syntax. Much less code.**

## When to Use the SDK vs. Raw API

| Situation | Use |
|:----------|:----|
| Simple to medium agent | OpenAI Agents SDK |
| Multi-agent with handoffs | OpenAI Agents SDK |
| Need full control over the loop | Raw Anthropic/OpenAI API |
| Complex swarm or dynamic spawning | Raw API |
| Using Anthropic's Claude models | Raw Anthropic API |
| Using OpenAI's GPT models | OpenAI Agents SDK |
| Learning / prototyping fast | OpenAI Agents SDK |

## Learning Materials

1. **PASS1_RECOGNITION.md** — 8 examples of SDK code to read (START HERE)
2. **PASS_C_VISUAL.md** — Architecture diagrams and translation maps
3. **PASS3_TEMPLATES.md** — 6 copy-paste templates for real use
4. **CHEATSHEET_L08.py** — Quick reference (keep open while building)
5. **template_openai_agent.py** — Full runnable demo with 4 scenarios

## The 5 Concepts That Cover 90% of SDK Usage

```
1. Agent(name, instructions, tools, handoffs)   → define the agent
2. @function_tool                                → create a tool from a function
3. Runner.run_sync(agent, message)              → run the agent (sync)
4. result.final_output                           → get the answer
5. Agent(handoffs=[specialist])                  → route to another agent
```

That's it. Everything else is variations on these five.

## How to Run the Demo

```bash
# Demo mode (no API key needed):
python template_openai_agent.py

# Real mode:
pip install openai-agents
export OPENAI_API_KEY=your_key_here
# Set DEMO_MODE = False in the file, then:
python template_openai_agent.py
```
