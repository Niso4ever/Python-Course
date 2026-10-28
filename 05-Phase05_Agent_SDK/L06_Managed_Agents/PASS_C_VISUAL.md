# L06 — Visual: Managed Agents (Three-Step Pattern)

## The Three Tiers Side by Side

> **Correction (2026-10-28):** Where an example below streams with `session.stream(input=...)` and checks
> `session_start` / `text_delta` / `tool_call` / `session_complete` or `event.text`, that event model does not exist.
> The real loop opens `client.beta.sessions.events.stream(session.id)`, sends the task with
> `client.beta.sessions.events.send(session.id, events=[{"type": "user.message", "content": [{"type": "text", "text": task}]}])`,
> and reads `agent.message` (text in `event.content` blocks), `agent.tool_use`, and `session.status_idle` (finished).
> See the code block in `README.md` and `template_managed_agent.py`. Source: platform.claude.com/docs/en/managed-agents/quickstart.

```
TIER 1 (Phase 4)              TIER 2 (L01–L05)              TIER 3 (this lesson)
─────────────────────         ────────────────────           ─────────────────────────
Your machine runs loop        Your machine runs loop         ANTHROPIC runs loop
                              (SDK hides the code)           (fully server-side)

client.messages.create()  →   query(prompt=task, options) → sessions.events.send/stream
+ manual tool dispatch        SDK dispatches tools            Anthropic dispatches tools
+ manual messages list        SDK manages messages            Anthropic manages context
+ you handle retries          SDK handles retries             Anthropic handles retries
                                                              + memory stores
                                                              + environments (sandbox)
                                                              + vaults (secrets)
```

---

## The Three-Step Pattern

```
STEP 1: Define the Agent (do this ONCE — reuse by ID)
┌────────────────────────────────────────────────────────────┐
│  agent = client.beta.agents.create(                        │
│      name="Research Assistant",                            │
│      model={"id": "claude-sonnet-5-5"},                    │
│      system="You are a helpful research assistant."        │
│  )                                                         │
│  → agent.id = "agt_abc123"                                 │
└────────────────────────────────────────────────────────────┘
                               │
                               ▼ (save agent.id — reuse forever)

STEP 2: Create an Environment (sandbox for execution)
┌────────────────────────────────────────────────────────────┐
│  env = client.beta.environments.create(                    │
│      name="research-env"                                   │
│  )                                                         │
│  → env.id = "env_xyz789"                                   │
└────────────────────────────────────────────────────────────┘
                               │
                               ▼ (save env.id — reuse per deployment)

STEP 3: Start a Session (one conversation/task run)
┌────────────────────────────────────────────────────────────┐
│  session = client.beta.sessions.create(                    │
│      agent=agent.id,                                       │
│      environment_id=env.id                                 │
│  )                                                         │
│  with client.beta.sessions.events.stream(session.id) as s: │
│      client.beta.sessions.events.send(session.id, ...)     │
│      for event in s: ...   # until session.status_idle     │
└────────────────────────────────────────────────────────────┘
```

---

## Session Event Stream

```
session.stream(input="Research quantum computing")
         │
         ▼
session_start          ← session is live
         │
         ▼
[agent_thinking]       ← Anthropic's servers running the loop
         │
         ├── tool_call: search("quantum computing trends")
         │          ▼
         │   tool_result: "..."
         │
         ├── text_delta: "Quantum computing..."
         ├── text_delta: " uses quantum..."
         ├── text_delta: " mechanical..."
         │
         ▼
session_complete       ← final result available
         │
         ▼
    event.result
```

---

## Create Once, Run Many Times

```
Day 1:   agents.create()   → agent.id = "agt_abc"   ← SAVE THIS
         environments.create() → env.id = "env_xyz" ← SAVE THIS

Day 2:   sessions.create(agent="agt_abc", environment_id="env_xyz")
         session.stream("task 1")

Day 3:   sessions.create(agent="agt_abc", environment_id="env_xyz")
         session.stream("task 2")

→ Each session = one fresh conversation using the same agent definition
→ Agent and environment are reused — no re-creation cost
```

---

## Managed Agents vs. Agent SDK Decision

```
Use Agent SDK (L01–L05) when:           Use Managed Agents (L06+) when:
─────────────────────────────           ─────────────────────────────────
You need loop control                   You want zero infrastructure
You need custom message injection       You need built-in memory stores
Cost visibility per iteration           You want Anthropic to handle retries
Portable (any server, any cloud)        You want cloud sandbox execution
Already have agent infrastructure       Starting fresh in 2026
```
