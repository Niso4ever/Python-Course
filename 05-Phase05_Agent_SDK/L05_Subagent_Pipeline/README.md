# L05 — Two-Agent Pipeline (Subagents)

> **Metaphor:** A project manager who can't do everything alone delegates to a specialist.
> The orchestrator agent is the PM. The subagent is the specialist. One task, two minds.

---

## The Shift

Phase 4 (Ph4-L05) built multi-agent orchestration manually — two separate `run_agent()` calls wired together.

The SDK approach: give the orchestrator permission to spawn subagents using the `Agent` tool:

```python
# Orchestrator — can spawn subagents
orchestrator_options = ClaudeAgentOptions(
    system_prompt="You are a research orchestrator. Delegate work using the Agent tool.",
    allowed_tools=["Agent"],   # the key permission
    model="claude-sonnet-5-5"
)

# The orchestrator decides WHEN and WHAT to delegate
# The subagent runs its own full loop and reports back
```

`allowed_tools=["Agent"]` auto-approves the Agent tool; it does not restrict the orchestrator to it.
To give the orchestrator a named specialist (its own prompt, tools and model), define it with
`agents=` and `AgentDefinition` (added 2026-10-28; source: code.claude.com/docs/en/agent-sdk/subagents):

```python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

orchestrator_options = ClaudeAgentOptions(
    allowed_tools=["Agent", "WebSearch"],
    agents={
        "researcher": AgentDefinition(
            description="Research specialist. Use for fact-finding with sources.",  # when to delegate
            prompt="You are a research specialist. Find facts and cite sources.",  # its system prompt
            tools=["WebSearch"],                                                     # what it may use
            model="haiku",                                                           # cheaper model
        ),
    },
)
```

The template in this folder chains two separate `query()` calls by hand instead. Both work: the
hand-chained version is easier to follow; `agents=` lets the orchestrator decide when to delegate.

---

## The Two Roles

| Role | Responsibility |
|------|---------------|
| **Orchestrator** | Understands the overall goal, breaks it into tasks, delegates, assembles results |
| **Subagent** | Focused specialist — only sees its assigned subtask, does one thing well |

---

## When to Use Two Agents Instead of One

Use one agent when: the task is linear and fits in one context window.
Use two agents when:

1. **Specialization:** The specialist needs a different system prompt / persona
2. **Context isolation:** The subagent shouldn't see the full conversation history
3. **Parallelism:** Multiple independent subtasks can run simultaneously
4. **Cost control:** Use a cheaper model for the specialist's simpler task

---

## The Simplest Pattern: Output → Input

```
Orchestrator:  "Research quantum computing trends"
    │
    ▼ spawns subagent
Subagent:      [runs full loop with research tools]
    │
    ▼ returns result
Orchestrator:  "Now write a summary of: {subagent_result}"
    │
    ▼ final answer
```

Output of agent 1 becomes input of agent 2. That's all a pipeline is.

---

## Architect's Question

> "Is this one agent doing two different things, or two different agents each doing one thing?
> If the system prompt would need to say 'be both a researcher AND a writer', split it."
