# L01_Labels_and_Types Template Reference

This file lists each L01_Labels_and_Types template and what it does.

> **2026 update:** All function templates now include type hints (`name: str = value`, `def fn(x: str) -> dict:`).
> Classic style and 2026 style are both shown. CHEATSHEET_L01.py Section 1B has the full type hint guide.

| Template | What It Does |
| --- | --- |
| `CHEATSHEET_L01.py` | Quick reference for Python variables, dictionaries, nested dictionaries, safe `.get()` access, type hints (Section 1B), and common syntax/type mistakes. |
| `template_llm_metadata.py` | Template for logging LLM API call metadata (model, tokens, latency, cost, success/error, timestamp). |
| `template_document_metadata.py` | Template for storing RAG/vector-search document metadata, including relevance, verification, and filtering patterns. |
| `template_agent_config.py` | Template for agent configuration and runtime state (RAG settings, tool configs, step history, token budget). |
| `template_structured_output.py` | Template for prompting LLMs to return structured JSON outputs (simple, multi-section, nested, and custom formats). |
| `example_structured_output_demo.py` | Runnable demo showing a structured-output prompt, example JSON response, `json.loads` parsing, and reusable prompt generation. |

