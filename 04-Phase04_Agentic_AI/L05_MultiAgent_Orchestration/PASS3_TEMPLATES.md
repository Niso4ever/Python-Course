# Lesson 21 — Pass 3: TEMPLATES
## Your Multi-Agent Orchestration Copy-Paste Library

---

## Template 1: Simple Router Orchestrator
**Use when:** Different types of requests need different specialists

> **Note (2026-10-28):** forced `tool_choice={"type": "tool", ...}` routing like the example below returns a 400 on
> claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1. On those models get the routing decision with
> `client.messages.parse(..., output_format=RoutingModel)` instead (see L04).
> Source: platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use

```python
import anthropic
from pydantic import BaseModel
from typing import Literal

client = anthropic.Anthropic()

class Route(BaseModel):
    agent: Literal["research", "write", "analyse", "fallback"]
    reason: str

route_tool = {
    "name": "Route",
    "description": "Decide which specialist handles this request.",
    "input_schema": Route.model_json_schema()
}

def classify(request: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=256,
        tools=[route_tool],
        tool_choice={"type": "tool", "name": "Route"},
        messages=[{"role": "user", "content": f"Route: {request}"}]
    )
    return Route(**response.content[0].input).agent

def orchestrate(user_request: str) -> str:
    route = classify(user_request)
    print(f"[Router] → {route}")
    agents = {
        "research": research_agent,
        "write":    writer_agent,
        "analyse":  analyst_agent,
        "fallback": fallback_agent,
    }
    return agents.get(route, fallback_agent)(user_request)
```

**Example calls:**
```python
answer = orchestrate("Research the latest advances in quantum computing.")
# [Router] → research

answer = orchestrate("Write a LinkedIn post about AI agents.")
# [Router] → write

answer = orchestrate("Compare GPT-5 and Claude 4 performance benchmarks.")
# [Router] → analyse
```

---

## Template 2: Sequential Pipeline
**Use when:** Task requires multiple ordered steps, each depends on the last

```python
def run_pipeline(topic: str) -> dict:
    """
    Research → Write → Review pipeline.
    Returns all intermediate results plus final output.
    """
    results = {"topic": topic}

    # Step 1
    print("[Step 1] Research...")
    results["research"] = research_agent(
        f"Research '{topic}'. Return facts, examples, key points."
    )

    # Step 2 — uses Step 1's output
    print("[Step 2] Write...")
    results["draft"] = writer_agent(
        f"Write a 400-word article using this research:\n\n{results['research']}"
    )

    # Step 3 — uses Step 2's output
    print("[Step 3] Review...")
    results["final"] = editor_agent(
        f"Improve this draft (fix grammar, clarity, flow):\n\n{results['draft']}"
    )

    return results
```

**Example call:**
```python
output = run_pipeline("How MCP is changing AI tool integration in 2026")
print(output["final"])       # polished article
print(len(output["research"]))  # can inspect any intermediate step
```

---

## Template 3: Parallel Execution
**Use when:** Multiple independent tasks — want speed, not sequential wait

```python
import asyncio
import anthropic

async_client = anthropic.AsyncAnthropic()

async def research_async(topic: str) -> tuple[str, str]:
    result = await run_agent_async(topic, tools=RESEARCH_TOOLS, system=RESEARCH_PROMPT)
    return topic, result

async def parallel_research(topics: list[str]) -> dict[str, str]:
    """Research all topics in parallel. Returns {topic: result} dict."""
    tasks = [research_async(t) for t in topics]
    results = await asyncio.gather(*tasks)
    return dict(results)

async def research_and_synthesize(topics: list[str]) -> str:
    """Parallel research → single synthesis."""
    research_results = await parallel_research(topics)

    synthesis_input = "\n\n".join(
        f"## {topic}\n{result}"
        for topic, result in research_results.items()
    )
    return writer_agent(f"Synthesize these research findings:\n\n{synthesis_input}")
```

**Example call:**
```python
topics = ["Claude Opus 4 capabilities", "GPT-5 launch details", "Gemini Ultra 2 benchmarks"]
summary = asyncio.run(research_and_synthesize(topics))
print(summary)   # comparative summary of all three models
# Time: ~same as researching 1 topic (all 3 ran in parallel)
```

---

## Template 4: Specialist Builder (Factory Pattern)
**Use when:** Need to define and call specialists cleanly

```python
import anthropic

client = anthropic.Anthropic()

class SpecialistSystem:
    def __init__(self, model: str = "claude-opus-4-6"):
        self.model = model
        self._specialists: dict = {}

    def add(self, name: str, system_prompt: str, tools: list = None):
        """Register a new specialist."""
        self._specialists[name] = {
            "system": system_prompt,
            "tools":  tools or []
        }
        return self   # ← allows chaining: system.add(...).add(...)

    def run(self, name: str, task: str) -> str:
        """Run a named specialist on a task."""
        spec = self._specialists.get(name)
        if not spec:
            raise ValueError(f"Unknown specialist: {name}. Available: {list(self._specialists)}")
        return run_agent(task, tools=spec["tools"], system=spec["system"])

    def route(self, user_request: str) -> str:
        """Auto-route: classify then call the right specialist."""
        agent_names = list(self._specialists.keys())
        route = classify_with_options(user_request, agent_names)
        return self.run(route, user_request)
```

**Example call:**
```python
system = (
    SpecialistSystem()
    .add("researcher", "You are a thorough research analyst.", tools=[search_tool])
    .add("writer",     "You are a clear, engaging content writer.", tools=[format_tool])
    .add("coder",      "You are an expert Python developer.", tools=[code_tool])
)

# Direct call
result = system.run("researcher", "Latest MCP adoption statistics in 2026")
print(result)

# Auto-routed call
result = system.route("Write a blog post about AI agents.")
# classifies as "writer" → runs writer specialist
print(result)
```

---

## Template 5: Agent-as-Tool
**Use when:** Orchestrator LLM should decide when to invoke specialists

```python
def build_agent_tool(name: str, description: str, param_name: str = "task") -> dict:
    """Create a tool schema that wraps a specialist agent."""
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": {
                param_name: {
                    "type": "string",
                    "description": f"The task for the {name} specialist"
                }
            },
            "required": [param_name]
        }
    }

# Register specialists as tools
AGENT_TOOLS = [
    build_agent_tool("research_specialist", "Research any topic. Returns detailed findings."),
    build_agent_tool("write_specialist",    "Write content from provided context or brief."),
    build_agent_tool("analyse_specialist",  "Analyse data, compare options, find patterns."),
]

# Map tool names to agent functions
AGENT_DISPATCH = {
    "research_specialist": research_agent,
    "write_specialist":    writer_agent,
    "analyse_specialist":  analyst_agent,
}

def run_meta_orchestrator(user_request: str) -> str:
    """Orchestrator whose tools ARE other agents."""
    def dispatch_agent(block):
        fn = AGENT_DISPATCH.get(block.name)
        return fn(block.input["task"]) if fn else "Unknown agent"

    messages = [{"role": "user", "content": user_request}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6", max_tokens=4096,
            system="You are an orchestrator. Use specialist agents to complete complex tasks.",
            tools=AGENT_TOOLS,
            messages=messages
        )
        if response.stop_reason == "end_turn":
            return response.content[0].text

        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                result = dispatch_agent(block)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
        messages.append({"role": "user", "content": results})
```

**Example call:**
```python
article = run_meta_orchestrator("Research the history of the agent loop concept, then write a concise explainer.")
# Orchestrator decides: call research_specialist first, then write_specialist
# No if/elif needed — LLM figures out the order
print(article)  # complete explainer article
```

---

## Quick Selection Guide

| Need | Template |
|:-----|:---------|
| Route by request type | Template 1: Simple Router |
| Multi-step dependent tasks | Template 2: Sequential Pipeline |
| Independent tasks, speed needed | Template 3: Parallel |
| Clean specialist management | Template 4: Specialist Builder |
| LLM decides which agent to call | Template 5: Agent-as-Tool |

---

## Specialist Configuration Pattern

```python
# Every specialist is just these 3 things:
SPECIALIST = {
    "system": "You are a [role]. Your job is to [specific goal].",
    "tools":  [tool1, tool2],           # domain-specific tools
    "model":  "claude-opus-4-6"         # can use different models per specialist
}

# Call pattern (always the same):
result = run_agent(task, tools=SPECIALIST["tools"], system=SPECIALIST["system"])
```
