# L01 — Pass 3: TEMPLATES
## Your Agent Debugging Copy-Paste Library

**Goal:** Five ready-to-use debugging patterns. Copy, configure, run.

---

## Template 1: The Event Trace Logger

**Use when:** You need to see exactly what the agent was thinking when it failed.

```python
import json
from datetime import datetime

class TraceLogger:
    """A 'flight recorder' for an agent's internal monologue and actions."""
    def __init__(self, log_file: str = "trace.jsonl"):
        self.log_file = log_file
        # Clear previous log
        open(self.log_file, "w").close()

    def log(self, event_type: str, data: dict):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Also print a summary to console for live debugging
        print(f"[{event_type.upper()}] {str(data)[:100]}")

# Usage inside an agent loop:
# logger = TraceLogger()
# logger.log("input", {"prompt": user_input})
# logger.log("think", {"reasoning": llm_internal_monologue})
# logger.log("tool_call", {"name": "search", "args": {"q": "python"}})
# logger.log("tool_result", {"output": search_results})
```

---

## Template 2: Context Window Monitor

**Use when:** Your agent suddenly "forgets" its instructions in long conversations.

```python
class ContextMonitor:
    """Tracks token usage and flags when truncation happens."""
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.truncation_count = 0
        self.has_truncated = False

    def check_size(self, messages: list[dict]):
        # Mock token count: ~4 chars per token. For the real number use
        # client.messages.count_tokens(model=..., messages=...) — free,
        # rate-limited, an estimate; count with the model you will call.
        self.current_tokens = sum(len(str(m.get("content", ""))) // 4 for m in messages)
        
        if self.current_tokens > self.max_tokens:
            self.has_truncated = True
            self.truncation_count += 1
            print(f"⚠️ WARNING: Context limit exceeded ({self.current_tokens} > {self.max_tokens})")
            print("  Agent may lose instructions or prior memory!")
            return True
        return False

# Usage:
# monitor = ContextMonitor(max_tokens=4000)
# if monitor.check_size(messages):
#     messages = truncate_oldest_messages(messages)
```

---

## Template 3: The Repair Loop

**Use when:** Your agent sometimes produces invalid JSON or schema formats.

```python
from pydantic import BaseModel, ValidationError

class OutputSchema(BaseModel):
    action: str
    confidence: float

async def robust_agent_call(prompt: str, max_retries: int = 2) -> OutputSchema:
    """Tries to get a valid response, asks the agent to fix it if it fails."""
    current_prompt = prompt
    
    for attempt in range(max_retries + 1):
        # 1. Get raw output (simulated here)
        raw_output = await run_llm(current_prompt)
        
        # 2. Try to parse it
        try:
            return OutputSchema.model_validate_json(raw_output)
        except ValidationError as e:
            if attempt == max_retries:
                print(f"❌ Failed after {max_retries} repairs. Last error: {e}")
                raise
            
            # 3. Create a repair prompt and try again
            print(f"⚠️ Validation error on attempt {attempt+1}. Asking agent to repair...")
            current_prompt = f"""
            Your previous output failed validation: {e}
            Here is what you output: {raw_output}
            Please fix the errors and return ONLY valid JSON matching the schema.
            """

# Usage:
# result = await robust_agent_call("What action should I take?")
```

---

## Template 4: State Snapshots (Memory Diffs)

**Use when:** You need to see how the agent's memory or files changed step-by-step.

```python
import json
import copy

class StateSnapshotter:
    """Takes snapshots of state dicts to find where things went wrong."""
    def __init__(self):
        self.snapshots = []

    def take_snapshot(self, step_name: str, state: dict):
        # Deepcopy is crucial so later changes don't affect the snapshot
        self.snapshots.append({
            "step": step_name,
            "state": copy.deepcopy(state)
        })

    def print_diff(self, step_a: int, step_b: int):
        state_a = self.snapshots[step_a]["state"]
        state_b = self.snapshots[step_b]["state"]
        
        print(f"Diff from {self.snapshots[step_a]['step']} to {self.snapshots[step_b]['step']}:")
        for key in set(state_a.keys()) | set(state_b.keys()):
            val_a = state_a.get(key)
            val_b = state_b.get(key)
            if val_a != val_b:
                print(f"  {key}: {val_a} -> {val_b}")

# Usage:
# memory = {"known_facts": ["sky is blue"], "goal": "find water"}
# snapshotter.take_snapshot("start", memory)
# memory["known_facts"].append("water is wet")
# snapshotter.take_snapshot("after_search", memory)
# snapshotter.print_diff(0, 1)
```

---

## Template 5: Concurrency Lock

**Use when:** Multiple agents might write to the same file/resource simultaneously.

```python
import asyncio
import json
from pathlib import Path

# The shared lock (must be accessible to all agents)
memory_lock = asyncio.Lock()
MEMORY_FILE = Path("shared_memory.json")

async def safe_memory_update(agent_name: str, new_fact: str):
    """Safely updates a shared file without race conditions."""
    # Critical section: only one agent can be in this block at a time
    async with memory_lock:
        print(f"[{agent_name}] Acquired lock, reading memory...")
        
        # 1. Read current state
        if MEMORY_FILE.exists():
            data = json.loads(MEMORY_FILE.read_text())
        else:
            data = {"facts": []}
            
        # 2. Modify state
        data["facts"].append(new_fact)
        
        # 3. Simulate slow I/O
        await asyncio.sleep(0.5) 
        
        # 4. Write back
        MEMORY_FILE.write_text(json.dumps(data, indent=2))
        print(f"[{agent_name}] Released lock, memory updated.")

# Usage:
# await asyncio.gather(
#     safe_memory_update("Agent1", "fact A"),
#     safe_memory_update("Agent2", "fact B")
# )
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| See what the agent was thinking | Template 1: Trace Logger |
| Agent forgets instructions | Template 2: Context Monitor |
| Agent outputs bad JSON | Template 3: Repair Loop |
| Agent corrupts state/memory | Template 4: State Snapshots |
| Multiple agents break files | Template 5: Concurrency Lock |
