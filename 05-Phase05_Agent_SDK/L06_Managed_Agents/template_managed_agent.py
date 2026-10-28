"""
TEMPLATE: Managed Agents — First Look
CURRICULUM PATTERN: Ph5-L06
DESCRIPTION: The 3-step Anthropic Managed Agents pattern (public beta since April 8, 2026;
             still beta as of 2026-10-28). DEMO_MODE mocks the API objects to show
             the pattern without a key. Real-mode call shapes checked against
             platform.claude.com/docs/en/managed-agents/quickstart on 2026-10-28.
Run with: python template_managed_agent.py
"""

import time
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

DEMO_MODE = True
BETA_HEADER = "managed-agents-2026-04-01"

# ──────────────────────────────────────────────
# DEMO MOCK OBJECTS
# ──────────────────────────────────────────────

class MockAgent(BaseModel):
    id: str = Field(description="Agent identifier")
    name: str = Field(description="Agent display name")
    model_id: str = Field(description="Model used by this agent")

class MockEnvironment(BaseModel):
    id: str = Field(description="Environment identifier")
    name: str = Field(description="Environment name (environments are not tied to one agent)")

class MockSession(BaseModel):
    id: str = Field(description="Session identifier")
    agent_id: str = Field(description="Agent running this session")
    environment_id: str = Field(description="Environment for this session")

@dataclass
class MockTextBlock:
    text: str
    type: str = "text"

@dataclass
class MockEvent:
    type: str                                   # real event types: "agent.message", "agent.tool_use", "session.status_idle", ...
    content: list[MockTextBlock] = field(default_factory=list)

DEMO_EVENTS: list[MockEvent] = [
    MockEvent("agent.message", [MockTextBlock("Based on current research, ")]),
    MockEvent("agent.message", [MockTextBlock("quantum computing in 2026 has reached several key milestones: ")]),
    MockEvent("agent.message", [MockTextBlock("larger processors, advances in error correction, ")]),
    MockEvent("agent.message", [MockTextBlock("and growing enterprise adoption.")]),
    MockEvent("session.status_idle"),             # agent has nothing more to do
]


def _demo_agents_create(name: str, model_id: str) -> MockAgent:
    return MockAgent(id="agt_demo_001", name=name, model_id=model_id)

def _demo_environments_create(name: str) -> MockEnvironment:
    return MockEnvironment(id="env_demo_001", name=name)

def _demo_sessions_create(agent_id: str, environment_id: str) -> MockSession:
    return MockSession(id="ses_demo_001", agent_id=agent_id, environment_id=environment_id)

def _demo_session_stream(session: MockSession, input_text: str):
    for event in DEMO_EVENTS:
        time.sleep(0.08)
        yield event


# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────

@dataclass
class ManagedAgentConfig:
    name: str = "Research Assistant"
    model_id: str = "claude-sonnet-5-5"
    system_prompt: str = "You are a helpful research assistant. Be concise and accurate."


# ──────────────────────────────────────────────
# THE THREE-STEP PATTERN
# ──────────────────────────────────────────────

def create_agent(config: ManagedAgentConfig) -> MockAgent | object:
    """Step 1: Define the agent. Do this ONCE and save the ID.

    Args:
        config: Agent configuration (name, model, system prompt).

    Returns:
        Agent object with .id field for reuse.
    """
    print(f"  Creating agent '{config.name}' ({config.model_id})...")

    if DEMO_MODE:
        agent = _demo_agents_create(config.name, config.model_id)
    else:
        import anthropic  # type: ignore
        client = anthropic.Anthropic()
        agent = client.beta.agents.create(       # SDK adds the beta header itself
            name=config.name,
            model=config.model_id,
            system=config.system_prompt,
            tools=[{"type": "agent_toolset_20260401"}],   # built-in bash/file/web tools
        )

    print(f"  ✓ Agent created: {agent.id}")
    return agent


def create_environment(name: str) -> MockEnvironment | object:
    """Step 2: Create a sandbox environment. Do this once per deployment context.

    An environment is not tied to one agent: it describes WHERE sessions run
    (cloud sandbox config, networking). Any agent's session can use it.

    Args:
        name: A label for the environment.

    Returns:
        Environment object with .id field for reuse.
    """
    print(f"  Creating environment '{name}'...")

    if DEMO_MODE:
        env = _demo_environments_create(name)
    else:
        import anthropic  # type: ignore
        client = anthropic.Anthropic()
        env = client.beta.environments.create(
            name=name,
            config={
                "type": "cloud",
                "networking": {"type": "limited", "allow_package_managers": True},
            },
        )

    print(f"  ✓ Environment created: {env.id}")
    return env


def run_session(
    agent_id: str,
    environment_id: str,
    input_text: str,
) -> str:
    """Step 3: Start a session and stream the agent's response.

    Args:
        agent_id: Agent ID from Step 1.
        environment_id: Environment ID from Step 2.
        input_text: The task or question to send to the agent.

    Returns:
        Complete response text after streaming finishes.
    """
    print(f"  Starting session for: '{input_text}'")
    print("  Streaming: ", end="")

    full_text = ""

    def handle(event) -> bool:
        """Print text from agent.message events. Return True when the agent goes idle."""
        nonlocal full_text
        if event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="", flush=True)
                    full_text += block.text
        elif event.type == "session.status_idle":
            return True
        return False

    if DEMO_MODE:
        session = _demo_sessions_create(agent_id, environment_id)
        for event in _demo_session_stream(session, input_text):
            if handle(event):
                break
    else:
        import anthropic  # type: ignore
        client = anthropic.Anthropic()
        session = client.beta.sessions.create(
            agent=agent_id,
            environment_id=environment_id,
        )
        # Open the stream first, then send the user's message as an event.
        with client.beta.sessions.events.stream(session.id) as stream:
            client.beta.sessions.events.send(
                session.id,
                events=[{
                    "type": "user.message",
                    "content": [{"type": "text", "text": input_text}],
                }],
            )
            for event in stream:
                if handle(event):
                    break

    print()
    return full_text


# ──────────────────────────────────────────────
# DEMO
# ──────────────────────────────────────────────

def main() -> None:
    config = ManagedAgentConfig()

    print("Managed Agents — 3-Step Pattern Demo")
    print("=" * 55)
    print()

    # Step 1 — Define agent once
    print("STEP 1: Create agent (do once, save ID)")
    agent = create_agent(config)
    print()

    # Step 2 — Create environment once
    print("STEP 2: Create environment (do once per context)")
    env = create_environment("research-env")
    print()

    # Step 3 — Run sessions (one per conversation)
    tasks = [
        "Research quantum computing trends in 2026",
        "Summarize the key benefits of RAG systems",
    ]

    for i, task in enumerate(tasks, 1):
        print(f"STEP 3 (Session {i}/{len(tasks)}): Run a session")
        result = run_session(agent.id, env.id, task)
        print(f"  ✓ Session complete ({len(result)} chars)\n")

    print("-" * 55)
    print("Pattern recap:")
    print(f"  Agent:       {agent.id}  ← reuse forever")
    print(f"  Environment: {env.id}  ← reuse per context")
    print(f"  Sessions:    {len(tasks)} created  ← new each run")
    print()
    print(f"[{'DEMO' if DEMO_MODE else 'REAL API'} MODE]")
    if DEMO_MODE:
        print(f"[Real API needs: ANTHROPIC_API_KEY + beta header '{BETA_HEADER}']")


if __name__ == "__main__":
    main()
