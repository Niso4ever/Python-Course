# L01 — Pass 1: RECOGNITION
## How to Spot Debugging Patterns in Agent Code

**Goal:** After this pass, you can look at any agent system and identify how it logs its thinking, where its state is stored, and how it handles errors.

---

## Pattern 1: The Event Stream (Trace Logging)

When you looked at the `continual-learning-bench` Claude system, you saw `_parse_events(stdout)`. This is the core of agent debugging.

```python
# SHAPE: appending structured events to a trace log
class Agent:
    def __init__(self):
        self._trace_log = []   # ← The "black box" flight recorder

    async def run(self, prompt):
        self._trace_log.append({"type": "input", "data": prompt})

        # Tool calls get logged
        tool_call = await decide_tool(prompt)
        self._trace_log.append({"type": "tool_call", "name": tool_call.name})

        # Responses get logged
        result = await execute(tool_call)
        self._trace_log.append({"type": "tool_result", "data": result})

# Later, when debugging:
with open("trace.jsonl", "w") as f:
    for event in agent._trace_log:
        f.write(json.dumps(event) + "\n")
```

**What to recognize:**
- A list/array (like `_trace_log` or `_jsonl_log`) that stores dicts/JSON
- Events appended at every major step (input, think, tool call, output)
- Export to `.jsonl` (JSON Lines) — one event per line
- **Why it matters:** When the agent hallucinates, the stack trace won't help. You need the event stream to see *what it was thinking* right before the mistake.

---

## Pattern 2: Context Window Monitoring

Agents fail silently when their context window overflows (truncation) or when the context gets too noisy (lost in the middle).

```python
# SHAPE: tracking token usage and context size
class ContextTracker:
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self.total_tokens += count_tokens(content)

        # The truncation trigger
        if self.total_tokens > MAX_TOKENS:
            self._truncate_oldest()
            self.truncation_count += 1      # ← Red flag metric
            self.has_truncated = True       # ← Red flag metric

# From CLBench ICL System:
def get_truncation_stats(self):
    return {
        "has_truncated": self.has_truncated_flag,
        "truncation_count": self.truncation_count,
        "current_tokens": self._count_message_tokens(self.messages),
    }
```

**What to recognize:**
- `count_tokens()` or similar functions
- `truncation_count` or `has_truncated` flags
- If `has_truncated` is True and the agent starts failing, you found your bug (it forgot the instructions).

---

## Pattern 3: State Checkpointing (Memory Snapshots)

If an agent has long-term memory (files, databases), you need to know exactly what that memory looked like at Step 5, not just at the end.

```python
# SHAPE: taking snapshots of memory files after every step
class MemoryAgent:
    def _record_memory_snapshot(self):
        # Read all files in the memory directory
        memory_snapshot = self._read_all_memory_files()

        # Save the snapshot to history
        self._memory_history.append({
            "step": self._interaction_count,
            "files": memory_snapshot
        })

# Debugging use case:
# "Why did it fail on step 6?"
# -> Look at memory snapshot from step 5. Oh, it corrupted the JSON file!
```

**What to recognize:**
- `snapshot`, `history`, or `checkpoint` naming
- Saving the *entire state* (like file contents) at regular intervals
- This is exactly what `continual-learning-bench` does to track what the Claude agent wrote to its `MEMORY.md`.

---

## Pattern 4: The Fallback / Repair Loop

Agents will produce invalid JSON. Good agent code expects this and tries to repair it.

```python
# SHAPE: try, catch validation error, prompt agent to fix it
async def run_action_turn(prompt, schema):
    # Try once
    assistant_text = await run_llm(prompt)
    try:
        return parse_json(assistant_text, schema)
    except ValidationError as e:
        # It failed. Don't crash — ask the agent to fix it.
        repair_prompt = f"Validation error: {e}\nFix your JSON: {assistant_text}"
        repair_text = await run_llm(repair_prompt)
        return parse_json(repair_text, schema)
```

**What to recognize:**
- `try/except` around JSON parsing or schema validation
- A specific prompt designed to feed the error *back* to the LLM
- Metrics tracking `repair_attempted` (if this is high, your original prompt is bad)

---

## Pattern 5: Concurrency Safety (Locks)

When two agents try to write to the same memory file at the same time, you get corruption.

```python
# SHAPE: asyncio.Lock protecting shared state
import asyncio

memory_lock = asyncio.Lock()

async def agent_write_memory(content: str):
    async with memory_lock:                # ← Critical section
        current = read_file("memory.txt")
        write_file("memory.txt", current + "\n" + content)
```

**What to recognize:**
- `asyncio.Lock()` (different from a Semaphore)
- `async with lock:` around file I/O or shared variable updates
- **The Bug:** If you see two agents writing to the same file *without* a lock, you've found a race condition.

---

## Recognition Drill: Read This Real Debugging Code

```python
def check_agent_health(metadata: dict) -> list[str]:
    warnings = []

    # Check 1: Did we lose context?
    if metadata.get("has_truncated", False):
        warnings.append(f"Context truncated {metadata['truncation_count']} times")

    # Check 2: Did the agent struggle to format output?
    if metadata.get("repair_attempted", False):
        warnings.append("Agent required a repair prompt to fix its JSON")

    # Check 3: Is it talking too much?
    usage = metadata.get("token_usage", {})
    if usage.get("output_tokens", 0) > 2000:
        warnings.append("High output token usage (possible loop/hallucination)")

    return warnings
```

**What you should spot:**
1. Debugging relies on **metadata**, not just the final string output.
2. Truncation, repairs, and token counts are the key vital signs.
3. This is exactly what an AI Architect looks at when an eval fails.

---

## Quick Reference: Failure Modes & Signatures

| Failure Mode | Signature in Logs |
|--------------|-------------------|
| **Context Overflow** | `has_truncated = True`, or sudden forgetfulness of early instructions |
| **Tool Loop** | `tool_call` → `error` → `tool_call` (same tool) repeating endlessly |
| **Schema Failure** | `repair_attempted = True` or `ValidationError` crashes |
| **Race Condition** | Two agents succeed, but only one agent's data is in the file |
| **Deadlock** | Agents hang forever, `asyncio.TimeoutError` triggers |
