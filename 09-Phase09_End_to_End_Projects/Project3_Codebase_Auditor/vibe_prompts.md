# Vibe Coding: The Autonomous Auditor

This architecture uses a **Custom Agent Loop** with trace logging and safe memory operations, modeled after the CLBench architecture.

## Prompt 1: The Core Infrastructure (memory_ops.py & trace_logger.py)
**Mode: Specification (Level 3)**

```text
CONSTRAINTS: Python 3.12 (the course venv). `asyncio`. Use `pathlib`.
REQUEST: First, create `trace_logger.py` with a `TraceLogger` class that appends JSON event dicts to a `.jsonl` file. 
Second, create `memory_ops.py`. Define an `asyncio.Lock()`. Write two functions: `read_memory()` and `write_finding(file_path, issue)` that safely read/write to a JSON file named `audit_memory.json` using the lock to prevent race conditions.
VALIDATION: The logger must clear the file on init and append one JSON object per line. The memory ops MUST use `async with lock` around file I/O.
```

## Prompt 2: The Agent Loop (eval_loop.py)
**Mode: Guardrails & Integration (Level 4)**

```text
CONSTRAINTS: Define a Pydantic `AuditResult(is_safe, vulnerability_description, recommended_fix)`. Import the `TraceLogger`.
REQUEST: Write `run_audit_loop(code_snippet, logger, max_retries)`. Mock the LLM call so it intentionally returns invalid JSON on attempt 1.
The loop must catch `ValidationError`, log it via the TraceLogger, construct a dialectic repair prompt embedding the error message and the raw output, and retry.
VALIDATION: The logger must capture `input`, `think`, `raw_output`, `validation_error`, and `success` events. The loop must successfully repair the JSON on the second try.
```

## Prompt 3: The Orchestrator (main.py)
**Mode: Integration (Level 5)**

```text
CONSTRAINTS: `asyncio.gather`. Import from `eval_loop` and `memory_ops`.
REQUEST: Write an orchestrator that concurrently audits a dictionary of simulated code files. If a file is unsafe, write the finding to memory using `write_finding()`. After all audits complete, use `read_memory()` to print the final vulnerability report.
VALIDATION: The script runs without API keys. The final output accurately reflects the state stored in the locked JSON file.
```
