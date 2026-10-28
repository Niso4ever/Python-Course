# Phase 8 — Code Review & Debugging (Ph8-L01, 1 template)

Tier 3 of the landscape: dealing with failure modes specific to agents (hallucinations, context overflow, bad schema). These prompts focus heavily on **Mode 4 (Debugging)** and **Mode 5 (Integration)** to ensure failures are caught and logged, rather than silently ignored.

---

## 55. `template_trace_debugger.py` — Ph8-L01 Trace Logger & Repair Loop
**Level 4 (Test Cases) · Mode 4 (Debugging)** — Flight recorders and self-correction.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: A simulated buggy agent outputs invalid JSON on its first attempt. Catch Pydantic ValidationErrors to trigger a repair prompt. Use a TraceLogger class to append all events to a .jsonl trace file.
REQUEST: Build a robust execution loop that catches schema errors, asks the agent to repair its output with the specific error message, and logs the entire reasoning trace (input, think, raw_output, validation_error, success).
VALIDATION: The agent succeeds on the second try. The .jsonl file contains a complete step-by-step history of the failure and recovery.
```
#### 💻 PRODUCES (essence)
```python
try:
    return OutputSchema.model_validate_json(raw_output)
except ValidationError as e:
    repair_prompt = f"Your previous output failed: {e}. Fix this JSON: {raw_output}"
    raw_output = await agent.chat(repair_prompt)
```
