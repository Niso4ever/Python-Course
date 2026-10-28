# Vibe Coding: The Research Synthesizer

This architecture uses the **Anthropic Agent SDK**. We decompose the problem into Tools -> Subagents -> Orchestrator.

## Prompt 1: The Tools (tools.py)
**Mode: Specification (Level 3)**

```text
CONSTRAINTS: Python 3.12 (the course venv). Async functions.
REQUEST: Create two mock tools: `search_web(query)` and `fetch_article(url)`. Then, define their JSON schemas manually in a list called `TOOLS`, and create a mapping dictionary called `TOOL_REGISTRY` mapping the tool names to the functions.
VALIDATION: The schema must strictly follow the Anthropic tool JSON format. The mock functions should use `asyncio.sleep(0.5)` to simulate network calls.
```

## Prompt 2: The Subagents (agents.py)
**Mode: Integration (Level 5)**

```text
CONSTRAINTS: Use a DEMO_MODE flag to mock the LLM calls so I can run this without API keys. Define a Pydantic schema `ResearchFindings(topic, key_points, sources)`.
REQUEST: Create two agent functions: `run_researcher(topic)` and `run_synthesizer(findings: list[ResearchFindings])`. 
The researcher should simulate using the tools to return a typed `ResearchFindings` object.
The synthesizer should accept a list of those objects, format them into a prompt string, and return a final Markdown report.
VALIDATION: The handoff must be clean: the output of Agent 1 must exactly match the input type of Agent 2. Include comments showing how this would be written using `claude_agent_sdk`.
```

## Prompt 3: The Orchestrator (main.py)
**Mode: Integration (Level 5)**

```text
CONSTRAINTS: `asyncio`. Import the agents.
REQUEST: Write `orchestrate_research(topics: list[str])`. It must use `asyncio.gather` to launch a `run_researcher` agent for EVERY topic simultaneously. Wait for all to finish, collect the list of `ResearchFindings`, and pass them to the `run_synthesizer`. Print the final output.
VALIDATION: The researcher agents MUST run in parallel, not sequentially.
```
