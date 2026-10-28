# Vibe Coding: The Data Pipeline

To build this architecture, you don't ask the AI to "build a pipeline." You ask for it piece by piece, starting with the contract.

## Prompt 1: The Contract (schema.py)
**Mode: Specification (Level 3)**

```text
CONSTRAINTS: Python 3.12 (the course venv). Use Pydantic BaseModel and Field.
REQUEST: Create a schema for a customer purchase record. It must capture the customer name, email (optional), purchase date, a list of items (product_id, quantity, unit_price), the total value of the transaction, and a boolean flag `is_flagged` if the raw text indicates a complaint, return, or fraud.
VALIDATION: Every field must have a clear `description` attribute inside `Field` so an LLM understands exactly what to extract.
```

## Prompt 2: The LLM Logic (extractor.py)
**Mode: Integration (Level 3)**

```text
CONSTRAINTS: Raw Anthropic async API (`AsyncAnthropic`). Import `CustomerRecord` from schema.py.
REQUEST: Write a function `extract_record(raw_text)` that uses `tool_choice` to FORCE the model to return the data matching the `CustomerRecord` schema. (If your target model rejects forced `tool_choice` — the newest Claude models do — ask instead for strict tool use or structured outputs via `output_config.format`.)
VALIDATION: The function must convert the Pydantic schema to an Anthropic tool dictionary, execute the API call, parse the `tool_use` block, validate it with Pydantic, and return the validated `CustomerRecord` object. Catch exceptions and return None on failure.
```

## Prompt 3: The Orchestrator (main.py)
**Mode: Integration (Level 3)**

```text
CONSTRAINTS: `asyncio`. Import `extract_record` from extractor.py. Include a DEMO_MODE toggle that skips the actual API call and returns mock data so I can test the concurrency.
REQUEST: Write a batch pipeline that processes a list of 3 raw text strings. Use `asyncio.Semaphore(2)` to limit concurrent API calls. Launch them all via `asyncio.gather` and print the resulting JSON objects and total execution time.
VALIDATION: The execution must be properly rate-limited and run concurrently, not sequentially.
```
