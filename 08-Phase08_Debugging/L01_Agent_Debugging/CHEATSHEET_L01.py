"""
CHEATSHEET — Agent Debugging & Code Review (L01)
Keep this open while debugging agentic systems.

2026 Note: Debugging an agent is debugging a reasoning process, not a state machine.
"""

# ─── 1. THE 3 FATAL AGENT BUGS ──────────────────────────────
#
# 1. Hallucination/Looping (Reasoning Bug)
#    - Agent calls same tool 5 times with same arguments.
#    - Fix: Add max_steps limit, return explicit errors to agent.
#
# 2. Context Truncation (Amnesia Bug)
#    - Agent suddenly ignores system prompt or formatting rules.
#    - Fix: Monitor token counts, summarize old context before truncating.
#
# 3. State Corruption (Concurrency Bug)
#    - Two agents write to shared memory, data is lost.
#    - Fix: Use asyncio.Lock() around shared state writes.


# ─── 2. TRACE LOGGING (The Flight Recorder) ────────────────
# Always save the agent's internal monologue and tool calls to a file.
import json
from datetime import datetime

def log_trace(file_path: str, event_type: str, data: dict):
    """Save every step to a .jsonl file for post-mortem analysis."""
    with open(file_path, "a") as f:
        event = {"time": datetime.now().isoformat(), "type": event_type, "data": data}
        f.write(json.dumps(event) + "\n")


# ─── 3. THE REPAIR LOOP PATTERN ────────────────────────────
# When an agent outputs bad JSON, don't crash. Ask it to fix it.
from pydantic import BaseModel, ValidationError

class OutputSchema(BaseModel):
    action: str

async def try_parse_or_repair(raw_output: str, agent, max_retries=2):
    # max_retries + 1 checks: the first output, then one per repair.
    # (With range(max_retries) the last repaired output would never be checked.)
    for attempt in range(max_retries + 1):
        try:
            return OutputSchema.model_validate_json(raw_output)
        except ValidationError as e:
            if attempt == max_retries:
                break  # out of repairs
            # Send the exact error back to the agent
            repair_prompt = f"Validation Error: {e}\nFix this JSON: {raw_output}"
            raw_output = await agent.chat(repair_prompt)
    raise ValueError("Agent failed to repair output")

# 2026: on the Claude API you can often PREVENT bad JSON instead of repairing it:
# structured outputs (output_config.format) or strict tool use (strict: true)
# constrain the output to your schema. Keep the repair loop as a fallback for
# models or providers without that feature.


# ─── 4. CONTEXT MONITORING ─────────────────────────────────
# Track tokens before you hit the API limit
def check_context_health(messages: list[dict], max_tokens: int = 4000):
    # Rough approximation: 4 chars = 1 token (offline, free, often wrong).
    # Real count: client.messages.count_tokens(model=..., messages=...) —
    # free but rate-limited, and still an estimate. Newer models use a new
    # tokenizer, so count with the model you will actually call.
    est_tokens = sum(len(str(m.get("content", ""))) // 4 for m in messages)
    
    if est_tokens > max_tokens:
        print(f"⚠️ CONTEXT OVERFLOW DANGER: {est_tokens} > {max_tokens}")
        return True # Needs truncation or summary
    return False


# ─── 5. ASYNC LOCKS (Concurrency Safety) ───────────────────
# Use this when multiple agents share a file or variable
import asyncio

memory_lock = asyncio.Lock()

async def safe_write(filepath: str, data: str):
    async with memory_lock:  # Only one agent enters here at a time
        with open(filepath, "a") as f:
            f.write(data + "\n")


# ═══ QUICK REFERENCE TABLE ═════════════════════════════════
#
# | Symptom                         | Diagnosis                      | Fix                                |
# |---------------------------------|--------------------------------|------------------------------------|
# | Silent failure, wrong format    | Context window truncated       | Summarize history, monitor tokens  |
# | Endless tool calls              | Tool loop hallucination        | Add max_steps, improve tool desc   |
# | JSON Decode Error               | Missing repair loop            | Catch error, prompt agent to fix   |
# |                                 |                                | (or prevent: structured outputs)   |
# | Intermittent missing data       | Race condition on write        | Add asyncio.Lock()                 |
# | "I cannot perform this task"    | Safety filter / Bad prompt     | Check trace log for exact trigger  |
