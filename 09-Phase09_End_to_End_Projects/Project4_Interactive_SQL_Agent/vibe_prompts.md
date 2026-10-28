# Vibe Coding: The Interactive SQL Agent

This architecture introduces **Human-in-the-Loop (HITL)**. We use exceptions to break the agent loop when a destructive action is requested, shifting control back to the human orchestrator.

## Prompt 1: The HITL Tools (tools.py)
**Mode: Specification (Level 3)**

```text
CONSTRAINTS: Python 3.12 (the course venv). Async tool functions.
REQUEST: Create a custom exception `HumanApprovalRequired(action, details)`. Create two mock database tools: `execute_select_query` and `execute_destructive_query`. The destructive query MUST take an optional `confirmation_token`. If the token is missing or invalid, it must raise the `HumanApprovalRequired` exception. Provide the JSON schema array `TOOLS` for both functions.
VALIDATION: The destructive tool explicitly fails fast and raises the exception instead of executing.
```

## Prompt 2: The Resumable Agent (agents.py)
**Mode: Guardrails & Integration (Level 4)**

```text
CONSTRAINTS: Mock the LLM call (`DEMO_MODE`). Import the tools and exception.
REQUEST: Create a `DBAgent` class with a `run(prompt, injected_context=None)` method. The agent should attempt to call the destructive query tool. If it hits the `HumanApprovalRequired` exception, it must not catch it—allow it to bubble up to the caller. If `injected_context` is provided (meaning it was resumed), it should execute the tool *with* the required confirmation token.
VALIDATION: The agent handles normal execution, but correctly suspends (via unhandled exception) when human approval is needed, and resumes correctly when context is injected.
```

## Prompt 3: The Orchestrator (main.py)
**Mode: Integration (Level 5)**

```text
CONSTRAINTS: `asyncio`. Use `input()` to get CLI feedback from the user.
REQUEST: Write `orchestrate()` to run the `DBAgent`. Wrap the agent run in a try/except block catching `HumanApprovalRequired`. When caught, print a loud warning to the console, print the SQL query the agent wants to run, and use `input(yes/no)` to ask the human for approval. If yes, resume the agent by calling `run()` again, injecting a system message containing the approval token.
VALIDATION: The script successfully pauses, waits for standard input, and accurately controls whether the agent is allowed to proceed based on human feedback.
```
