# L06 — Pass 1: RECOGNITION
## Learn to SEE the Managed Agents Pattern

**Goal:** When you see Managed Agents code, instantly recognize the three-step structure and know what each step does — without writing a single line.

> **2026 Note:** Managed Agents launched April 8, 2026 in public beta. The API is at `client.beta.agents`, `client.beta.environments`, `client.beta.sessions`. You'll start seeing this in production codebases and job postings. The three steps are always present — learn to spot them even when the code is split across multiple files. Still in beta as of 2026-10-28 (all endpoints use the `managed-agents-2026-04-01` header, which the SDK sets for you).

> **Correction (2026-10-28):** Where an example below streams with `session.stream(input=...)` and checks
> `session_start` / `text_delta` / `tool_call` / `session_complete` or `event.text`, that event model does not exist.
> The real loop opens `client.beta.sessions.events.stream(session.id)`, sends the task with
> `client.beta.sessions.events.send(session.id, events=[{"type": "user.message", "content": [{"type": "text", "text": task}]}])`,
> and reads `agent.message` (text in `event.content` blocks), `agent.tool_use`, and `session.status_idle` (finished).
> See the code block in `README.md` and `template_managed_agent.py`. Source: platform.claude.com/docs/en/managed-agents/quickstart.

---

## The Three Shapes of Managed Agents

### Shape 1: Agent Creation (Step 1)
```python
agent = client.beta.agents.create(
    name="...",
    model={"id": "claude-sonnet-5-5"},
    system="...",
    betas=["managed-agents-2026-04-01"]
)
```
**Recognize:** `client.beta.agents.create()`. Returns an object with `.id`. This is done ONCE. In production you save `agent.id` to a config file or database — you never recreate it per request.

### Shape 2: Environment Creation (Step 2)
```python
env = client.beta.environments.create(name="research-env")
```
**Recognize:** `client.beta.environments.create()`. Takes a `name` and an optional sandbox `config`; it is not tied to one agent. Returns `.id`. Done once per deployment context. Think: "the sandbox this agent runs in."

### Shape 3: Session Streaming (Step 3)
```python
session = client.beta.sessions.create(agent=..., environment_id=...)
for event in session.stream(input="user task here"):
    ...
```
**Recognize:** `sessions.create()` + `session.stream()`. This pair is the per-conversation pattern. New session for each run.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: The Minimal Three-Step
```python
import anthropic
client = anthropic.Anthropic()

agent = client.beta.agents.create(name="Assistant", model={"id": "claude-sonnet-5-5"}, system="You help.")
env   = client.beta.environments.create(name="research-env")
session = client.beta.sessions.create(agent=agent.id, environment_id=env.id)

for event in session.stream(input="Hello"):
    if hasattr(event, "text"):
        print(event.text, end="")
```
**Recognize:** All three steps in sequence. Agent → Environment → Session. Event loop at the end. This is the complete skeleton.

---

### Example 2: Reuse Pattern (Production)
```python
# config.py — loaded at startup, not recreated per request
AGENT_ID = "agt_abc123"
ENV_ID   = "env_xyz789"

# handler.py — runs per request
def handle_request(user_input: str) -> str:
    session = client.beta.sessions.create(
        agent=AGENT_ID,   
        environment_id=ENV_ID
    )
    result = ""
    for event in session.stream(input=user_input):
        if hasattr(event, "text"):
            result += event.text
    return result
```
**Recognize:** `AGENT_ID` and `ENV_ID` are constants — created once, hardcoded or stored in env vars. Only Step 3 (`sessions.create`) runs per request. This is the production pattern.

---

### Example 3: Beta Header
```python
agent = client.beta.agents.create(
    name="Research Agent",
    model={"id": "claude-opus-5-5"},
    system="You are a research specialist.",
    betas=["managed-agents-2026-04-01"]   # ← required beta header
)
```
**Recognize:** `betas=["managed-agents-2026-04-01"]` is required during public beta. The SDK adds the HTTP header automatically when you pass it here.

---

### Example 4: Event Stream Types
```python
for event in session.stream(input="Research quantum computing"):
    if event.event_type == "session_start":
        print("Agent started...")
    elif event.event_type == "text_delta":
        print(event.text, end="", flush=True)
    elif event.event_type == "tool_call":
        print(f"\n[Tool: {event.tool_name}]")
    elif event.event_type == "session_complete":
        print("\nDone.")
```
**Recognize:** Four event types: `session_start`, `text_delta`, `tool_call`, `session_complete`. Managed Agents have a richer event stream than raw API because the server is doing more work.

---

### Example 5: Agent vs Environment vs Session (Lifecycle Comparison)
```python
# Day 1 setup
agent = client.beta.agents.create(...)  # ← define ONCE: model, system, tools
env   = client.beta.environments.create(name="research-env")  # ← create ONCE per context
# Save: AGENT_ID = agent.id, ENV_ID = env.id

# Day 1 run
s1 = client.beta.sessions.create(agent=AGENT_ID, environment_id=ENV_ID)

# Day 2 run — same agent and env, new session
s2 = client.beta.sessions.create(agent=AGENT_ID, environment_id=ENV_ID)
```
**Recognize:** Agent = months, Environment = weeks/months, Session = minutes. One agent definition serves thousands of sessions.

---

### Example 6: With Memory Store Reference
```python
agent = client.beta.agents.create(
    name="Personal Assistant",
    model={"id": "claude-sonnet-5-5"},
    system="Use the memory store to recall user preferences.",
    memory_store_id=store.id,    # ← persistent memory across sessions
    betas=["managed-agents-2026-04-01"]
)
```
**Recognize:** `memory_store_id=` is the bridge between sessions. Without it, each session starts fresh. With it, the agent remembers facts across runs. This is Tier 3's answer to Phase 4's manual memory patterns.

---

### Example 7: Managed Agents vs Agent SDK
```python
# Agent SDK (L01–L05) — your machine runs the loop
from claude_agent_sdk import query, ClaudeAgentOptions
async for msg in query(prompt="task", options=ClaudeAgentOptions()):
    ...

# Managed Agents (L06) — Anthropic runs the loop
session = client.beta.sessions.create(agent=..., environment_id=...)
for event in session.stream(input="task"):
    ...
```
**Recognize:** SDK = you import and run. Managed = you create a session and receive events. The distinction: who runs the loop.

---

### Example 8: In a Web API Handler
```python
@app.post("/agent/run")
def run_agent_endpoint(request: RunRequest) -> RunResponse:
    session = client.beta.sessions.create(
        agent=settings.AGENT_ID,
        environment_id=settings.ENV_ID
    )
    result = ""
    for event in session.stream(input=request.task):
        if hasattr(event, "text"):
            result += event.text
    return RunResponse(result=result)
```
**Recognize:** The entire web handler is just Step 3. Steps 1 and 2 happen at app startup or deploy time. The request only creates a session and streams the result.
