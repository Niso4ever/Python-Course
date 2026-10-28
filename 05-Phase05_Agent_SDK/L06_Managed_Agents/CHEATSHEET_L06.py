"""
CHEATSHEET L06 — Managed Agents (First Look)
The 3-step pattern: agent + environment + session.
"""
import anthropic
client = anthropic.Anthropic()

# ── 1. STEP 1: CREATE AGENT (do once, save ID) ───────────────────────────────
# The SDK adds the "managed-agents-2026-04-01" beta header for you.
agent = client.beta.agents.create(
    name="Research Assistant",
    model="claude-sonnet-5-5",
    system="You are a helpful research assistant.",
    tools=[{"type": "agent_toolset_20260401"}],   # built-in bash / file / web tools
)
# → agent.id = "agent_..."  ← save this, reuse forever

# ── 2. STEP 2: CREATE ENVIRONMENT (sandbox config, once per deployment) ──────
# An environment is NOT tied to one agent — it says where sessions run.
env = client.beta.environments.create(
    name="research-env",
    config={"type": "cloud", "networking": {"type": "limited", "allow_package_managers": True}},
)
# → env.id = "env_..."  ← save this, reuse per context

# ── 3. STEP 3: START A SESSION, SEND A MESSAGE, STREAM EVENTS ────────────────
session = client.beta.sessions.create(agent=agent.id, environment_id=env.id)
with client.beta.sessions.events.stream(session.id) as stream:      # open stream first
    client.beta.sessions.events.send(session.id, events=[
        {"type": "user.message",
         "content": [{"type": "text", "text": "Research quantum computing trends"}]},
    ])
    for event in stream:
        if event.type == "agent.message":            # text from the agent
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="")
        elif event.type == "agent.tool_use":         # agent used a built-in tool
            print(f"\n[tool: {event.name}]")
        elif event.type == "session.status_idle":    # agent has nothing more to do
            break

# ── 4. REUSE PATTERN (production) ────────────────────────────────────────────
# Day 1:  create agent + env → save agent_id, env_id
# Day N:  sessions.create(agent=saved_agent_id, environment_id=saved_env_id)
#         → No re-creation. Just new sessions.

# ── 5. TIER DECISION ─────────────────────────────────────────────────────────
# Agent SDK (L01-L05): you control loop, portable, cost visibility per iteration
# Managed Agents (L06): Anthropic runs loop + sandbox, memory stores, zero infra (beta as of 2026-10-28)
# Raw API (Phase 4):    full control, debugging, learning how agents work
