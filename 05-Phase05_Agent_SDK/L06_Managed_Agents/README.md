# L06 — Managed Agents (First Look)

> **Metaphor:** Tier 1 (raw API) is owning a car. Tier 2 (Agent SDK) is leasing a car.
> Managed Agents is calling an Uber — you say where you want to go, Anthropic handles
> the driving, the fuel, the maintenance.

---

## The Shift

With the SDK, your code runs the agent loop on your machine:
```
Your machine: SDK loop → tool calls → response → loop again
```

With Managed Agents, Anthropic's servers run the loop:
```
Your code: creates agent + environment + session (3 API calls)
Anthropic: runs the loop, manages context, handles retries
Your code: receives events as they stream back
```

---

## The Three-Step Pattern (public beta since April 8, 2026; still beta on 2026-10-28)

```python
import anthropic
client = anthropic.Anthropic()   # SDK adds the managed-agents-2026-04-01 beta header itself

# Step 1: Define the agent — model, system, tools (create ONCE, reuse by ID)
agent = client.beta.agents.create(
    name="Research Assistant",
    model="claude-sonnet-5-5",
    system="You are a research assistant.",
    tools=[{"type": "agent_toolset_20260401"}],   # built-in bash / file / web tools
)

# Step 2: Create an environment — where sessions run (create once per context)
env = client.beta.environments.create(
    name="research-env",
    config={"type": "cloud", "networking": {"type": "limited", "allow_package_managers": True}},
)

# Step 3: Start a session — one conversation (create for each run)
session = client.beta.sessions.create(agent=agent.id, environment_id=env.id)

# Open the event stream, send the task as a user.message event, read events back
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(session.id, events=[
        {"type": "user.message", "content": [{"type": "text", "text": "Research quantum computing"}]},
    ])
    for event in stream:
        if event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="")
        elif event.type == "session.status_idle":   # agent finished
            break
```

> **Corrected 2026-10-28.** Earlier versions of this lesson showed `environments.create(agent_id=...)`,
> `sessions.create(agent_id=...)` and `session.stream(input=...)` with `session_start` / `text_delta` /
> `session_complete` events. None of those exist. The shapes above follow
> platform.claude.com/docs/en/managed-agents/quickstart. The PASS files still show the old event loop in
> places; read them for the three-step *structure*, and use this block for the actual calls.

---

## Agent vs. Environment vs. Session

| Concept | Analogy | Create how often |
|---------|---------|-----------------|
| **Agent** | The job description | Once — reuse by ID |
| **Environment** | The office/sandbox | Once per deployment context |
| **Session** | One work session | Each conversation / task run |

---

## Why This Matters (2026 Architect Lens)

The Managed Agents API is the arrival of the "declarative intent" paradigm from the course road map (`Python_Course_Road_Map.md`):

```
Old world: You write the loop → the tool call → the tool
New world: You write the agent definition (what it does, what tools it has)
           Anthropic runs everything else
```

Your `agents.create()` call IS your architecture. The description quality determines agent quality.

---

## Architect's Question

> "Am I building an agent I run, or defining an agent Anthropic runs?
> If you need portability, custom loop control, or cost visibility — stay in Tier 2.
> If you want zero infrastructure and built-in memory/tools — move to Tier 3."
