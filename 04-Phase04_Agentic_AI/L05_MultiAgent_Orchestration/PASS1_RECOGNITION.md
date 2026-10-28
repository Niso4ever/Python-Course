# Lesson 21 — Pass 1: RECOGNITION
## Learn to SEE Multi-Agent Patterns

**Goal:** Recognize orchestrator-specialist patterns, handoff flows, and parallel agent calls — in raw API code, without CrewAI or LangGraph.

> **2026 Note:** A "multi-agent system" is just multiple `run_agent()` calls coordinated by logic. CrewAI wraps this in Crew/Agent/Task classes. LangGraph wraps it in nodes and edges. Underneath: one function calling another. Read this and you'll read both frameworks instantly.

---

## The Three Shapes of Multi-Agent Systems

### Shape 1: The Orchestrator (router)
```python
def orchestrate(request: str) -> str:
    intent = classify_intent(request)       # ← decide who handles it
    if intent == "research":
        return research_agent(request)
    elif intent == "write":
        return writer_agent(request)
```
**Recognize:** A function that classifies → routes → calls another agent function.

---

### Shape 2: The Specialist (focused agent)
```python
def research_agent(task: str) -> str:
    return run_agent(
        question=task,
        tools=RESEARCH_TOOLS,               # ← specialized tools
        system=RESEARCH_SYSTEM_PROMPT       # ← specialized persona
    )
```
**Recognize:** `run_agent()` with a specific tool set and system prompt. Same loop — different config.

---

### Shape 3: The Handoff (output becomes input)
```python
def pipeline(request: str) -> str:
    research = research_agent(request)      # Step 1
    draft    = writer_agent(research)       # Step 2: uses research output
    review   = editor_agent(draft)          # Step 3: uses draft output
    return review
```
**Recognize:** Sequential calls where each agent's output feeds the next as input.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Simple Orchestrator with Route Function

> **Note (2026-10-28):** forced `tool_choice={"type": "tool", ...}` routing like the example below returns a 400 on
> claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1. On those models get the routing decision with
> `client.messages.parse(..., output_format=RoutingModel)` instead (see L04).
> Source: platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use

```python
import anthropic
from pydantic import BaseModel
from typing import Literal

client = anthropic.Anthropic()

# Step 1: Classify the request using structured output
class RoutingDecision(BaseModel):
    agent: Literal["research", "writer", "analyst", "fallback"]
    reason: str

route_tool = {
    "name": "RoutingDecision",
    "description": "Decide which specialist agent should handle this request.",
    "input_schema": RoutingDecision.model_json_schema()
}

def classify_request(user_input: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=256,
        tools=[route_tool],
        tool_choice={"type": "tool", "name": "RoutingDecision"},
        messages=[{"role": "user", "content": f"Route this request: {user_input}"}]
    )
    decision = RoutingDecision(**response.content[0].input)
    return decision.agent

# Step 2: Orchestrate
def orchestrate(user_input: str) -> str:
    route = classify_request(user_input)
    print(f"[Orchestrator] Routing to: {route}")

    if route == "research":
        return research_agent(user_input)
    elif route == "writer":
        return writer_agent(user_input)
    elif route == "analyst":
        return analyst_agent(user_input)
    else:
        return fallback_agent(user_input)

# Example call:
answer = orchestrate("Research the latest AI models released in 2026.")
# [Orchestrator] Routing to: research
# → research_agent handles the question
print(answer)   # detailed research output

answer = orchestrate("Write a blog post about agentic AI.")
# [Orchestrator] Routing to: writer
print(answer)   # formatted blog post
```

**RECOGNIZE THIS:**
- `classify_request(...)` uses structured output (L04) to get a typed routing decision
- `if route == "research":` ← the actual routing
- Each branch calls a different agent function

**What it does:** "Use LLM to classify the request → route to the right specialist."

---

### Example 2: Specialist Agents (all use the same run_agent loop)

```python
# System prompts define each specialist's persona
RESEARCH_PROMPT = """You are a thorough research specialist. Your job is to find accurate,
up-to-date information. Always cite sources. Be comprehensive and objective."""

WRITER_PROMPT = """You are a skilled content writer. Transform information into clear,
engaging prose. Use headers, examples, and a professional tone."""

ANALYST_PROMPT = """You are a data analyst. Extract insights, identify patterns,
and present findings with supporting evidence. Be precise and data-driven."""

# Tool sets define each specialist's capabilities
RESEARCH_TOOLS = [search_tool, arxiv_tool, news_tool]
WRITING_TOOLS  = [format_tool, outline_tool]
ANALYST_TOOLS  = [calculate_tool, chart_tool, statistics_tool]

# Specialist factory (note: each is just run_agent with different config)
def research_agent(task: str) -> str:
    return run_agent(task, tools=RESEARCH_TOOLS, system=RESEARCH_PROMPT)

def writer_agent(task: str) -> str:
    return run_agent(task, tools=WRITING_TOOLS, system=WRITER_PROMPT)

def analyst_agent(task: str) -> str:
    return run_agent(task, tools=ANALYST_TOOLS, system=ANALYST_PROMPT)

# Example calls:
research_result = research_agent("What are the top 5 LLMs in 2026?")
print(research_result)  # comprehensive research with citations

writer_result = writer_agent("Write a blog intro about the agent loop pattern.")
print(writer_result)    # formatted prose, ready to publish

analyst_result = analyst_agent("Compare GPT-5, Claude 5, and Gemini Ultra performance.")
print(analyst_result)   # structured comparison with numbers
```

**RECOGNIZE THIS:**
- All three specialists are `run_agent(...)` with different arguments
- System prompt = the specialist's persona
- Tools = the specialist's capabilities
- Naming convention: `_agent` suffix

**What it does:** "Three specialists — one loop, different configuration. This is all a 'specialist' is."

---

### Example 3: Sequential Pipeline (Handoff Chain)

```python
def research_then_write(topic: str) -> dict:
    """3-agent pipeline: research → write → review."""

    print(f"\n[Step 1] Research agent: researching '{topic}'")
    research = research_agent(f"Research {topic}. Return facts, examples, key points.")

    print(f"\n[Step 2] Writer agent: writing from research...")
    draft = writer_agent(f"Write a 300-word article using this research:\n\n{research}")

    print(f"\n[Step 3] Editor agent: reviewing draft...")
    review = editor_agent(f"Review and improve this draft:\n\n{draft}")

    return {
        "topic": topic,
        "research": research,
        "draft": draft,
        "final": review
    }

# Example call:
result = research_then_write("The impact of MCP on AI development in 2026")
print(result["final"])  # polished article ready for publication
# Shows the handoff:
# research → (feeds into) → draft → (feeds into) → review → final output
```

**RECOGNIZE THIS:**
- Three sequential calls — output of each is the input to the next
- `research` → `draft` → `review` ← the variable names show the pipeline
- Returns a dict with all intermediate results (useful for debugging)

**What it does:** "Assembly line: each agent takes the previous agent's output as input."

---

### Example 4: Parallel Agents (asyncio)

```python
import asyncio
import anthropic

client = anthropic.AsyncAnthropic()

async def research_agent_async(task: str) -> str:
    return await run_agent_async(task, tools=RESEARCH_TOOLS, system=RESEARCH_PROMPT)

async def parallel_research(topics: list[str]) -> list[str]:
    """Research multiple topics simultaneously."""
    tasks = [research_agent_async(topic) for topic in topics]
    results = await asyncio.gather(*tasks)     # ← run all in parallel
    return list(results)

# Example call:
topics = [
    "Claude Opus 4 capabilities",
    "GPT-5 benchmark results",
    "Gemini Ultra 2 features"
]
results = asyncio.run(parallel_research(topics))
print(f"Researched {len(results)} topics in parallel")
print(results[0][:100])  # Claude Opus 4 research
print(results[1][:100])  # GPT-5 research
print(results[2][:100])  # Gemini research
# All 3 ran simultaneously instead of 3x sequential wait time
```

**RECOGNIZE THIS:**
- `async def` + `await` ← async agents (L02 Example 8 pattern)
- `asyncio.gather(*tasks)` ← run all tasks in parallel
- Result is a list — one item per topic
- No dependency between topics → perfect for parallel execution

**What it does:** "Run multiple specialist agents simultaneously — 3× faster than sequential."

---

### Example 5: The Swarm Pattern (Agents Spawning Agents)

```python
def research_swarm(main_topic: str, depth: int = 2) -> dict:
    """
    Orchestrator discovers sub-topics, spawns a specialist per sub-topic.
    depth=1: just the main topic
    depth=2: main topic + sub-topics
    """
    # Step 1: Orchestrator identifies sub-topics
    sub_topics_response = client.messages.create(
        model="claude-opus-4-6", max_tokens=512,
        messages=[{
            "role": "user",
            "content": f"List 3 key sub-topics of '{main_topic}' as a JSON array."
        }]
    )
    import json
    sub_topics = json.loads(sub_topics_response.content[0].text)[:3]

    # Step 2: Spawn one specialist agent per sub-topic
    results = {}
    for sub_topic in sub_topics:
        print(f"  [Spawning agent] → {sub_topic}")
        results[sub_topic] = research_agent(sub_topic)

    # Step 3: Synthesize all results
    synthesis = writer_agent(
        f"Synthesize these research results on '{main_topic}':\n"
        + "\n".join(f"## {k}\n{v}" for k, v in results.items())
    )
    return {"topic": main_topic, "sub_research": results, "synthesis": synthesis}

# Example call:
report = research_swarm("Agentic AI in enterprise 2026")
print(f"Sub-topics researched: {list(report['sub_research'].keys())}")
# ["Multi-agent orchestration", "MCP adoption", "Agent security"]
print(report["synthesis"][:200])   # synthesized report
```

**RECOGNIZE THIS:**
- Orchestrator runs first to discover what needs to be done
- `for sub_topic in sub_topics:` ← spawning agents in a loop
- Results collected in a dict → fed to a synthesizer agent
- This is what CrewAI's "hierarchical process" does under the hood

**What it does:** "Dynamic agent spawning — orchestrator decides how many specialists to create."

---

### Example 6: Reading CrewAI as Multi-Agent (Framework Translation)

```python
# CrewAI code (2024 style):
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Research Analyst",
    goal="Find accurate information",
    tools=[search_tool]
)

writer = Agent(
    role="Content Writer",
    goal="Write clear articles",
    tools=[format_tool]
)

research_task = Task(description="Research AI trends", agent=researcher)
write_task    = Task(description="Write article", agent=writer, context=[research_task])

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()

# DIRECT API EQUIVALENT (2026 style):
def research_agent(task):
    return run_agent(task, tools=[search_tool], system="You are a Research Analyst. Find accurate information.")

def writer_agent(task):
    return run_agent(task, tools=[format_tool], system="You are a Content Writer. Write clear articles.")

research_result = research_agent("Research AI trends")
write_result    = writer_agent(f"Write article based on: {research_result}")
```

**RECOGNIZE THIS:**
- `Agent(role=..., goal=..., tools=...)` → `run_agent(system="...", tools=[...])`
- `Task(context=[research_task])` → `writer_agent(f"Use this: {research_result}")`
- `crew.kickoff()` → calling both functions sequentially
- Same behavior, 80% less code, no dependency

**What it does:** "CrewAI is just orchestration logic wrapped in classes. This shows the naked version."

---

### Example 7: Agent-as-Tool (Meta Pattern)

```python
# Register a specialist agent AS A TOOL for the orchestrator LLM
research_as_tool = {
    "name": "call_research_agent",
    "description": "Ask the research specialist to investigate a topic. Returns detailed findings.",
    "input_schema": {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Topic to research"}
        },
        "required": ["topic"]
    }
}

write_as_tool = {
    "name": "call_writer_agent",
    "description": "Ask the writer specialist to create content. Pass the research as context.",
    "input_schema": {
        "type": "object",
        "properties": {
            "task": {"type": "string", "description": "Writing task + context"},
        },
        "required": ["task"]
    }
}

# Dispatcher maps tool names to agent calls
AGENT_MAP = {
    "call_research_agent": lambda topic: research_agent(topic),
    "call_writer_agent":   lambda task:  writer_agent(task),
}

# The orchestrator LLM now has agents as its tools
def run_orchestrator(user_request: str) -> str:
    return run_agent(
        question=user_request,
        tools=[research_as_tool, write_as_tool],  # ← agents are tools
        system="You are an orchestrator. Use specialist agents to complete tasks."
    )

# Example call:
result = run_orchestrator("Research MCP and then write a blog post about it.")
# LLM calls: call_research_agent("MCP") → result →
#            call_writer_agent("Write about MCP: " + result) → final article
print(result)  # polished blog post about MCP
```

**RECOGNIZE THIS:**
- Tool schemas point to agent functions, not data functions
- Dispatcher calls `research_agent(topic)` or `writer_agent(task)` — not `search_web()`
- The orchestrator LLM decides WHEN and HOW to call each specialist

**What it does:** "Agents as tools — the orchestrator's agent loop calls specialist agents. Meta pattern."

---

### Example 8: Full Production Multi-Agent System

```python
class AgentSystem:
    def __init__(self, model: str = "claude-opus-4-6"):
        self.client = anthropic.Anthropic()
        self.model = model
        self._specialists = {}

    def register(self, name: str, system_prompt: str, tools: list):
        """Register a specialist agent by name."""
        self._specialists[name] = {"system": system_prompt, "tools": tools}

    def call(self, name: str, task: str) -> str:
        """Call a registered specialist."""
        spec = self._specialists.get(name)
        if not spec:
            raise ValueError(f"Unknown specialist: {name}")
        return run_agent(task, tools=spec["tools"], system=spec["system"])

    def route(self, user_request: str) -> str:
        """Classify and route to the right specialist."""
        route = classify_request(user_request)
        return self.call(route, user_request)

# Example call:
system = AgentSystem()
system.register("research", RESEARCH_PROMPT, RESEARCH_TOOLS)
system.register("write",    WRITER_PROMPT,   WRITING_TOOLS)
system.register("analyse",  ANALYST_PROMPT,  ANALYST_TOOLS)

# Single call — system routes automatically
answer = system.route("Analyse the performance gap between Claude 4 and GPT-5.")
print(answer)  # analyst output with structured comparison
```

**RECOGNIZE THIS:**
- `register(name, system, tools)` ← specialist registration
- `call(name, task)` ← generic specialist invocation
- `route(user_request)` ← full orchestration in one call
- Clean API — adding a new specialist = one `.register()` call

**What it does:** "Production multi-agent system — clean class interface, no framework."

---

## Multi-Agent Pattern Reference

| Pattern | Shape | Use when |
|:--------|:------|:---------|
| Router | `classify → if/elif → specialist` | Different tasks need different tools |
| Sequential (handoff) | `A(input) → B(A's output) → C(B's output)` | Each step depends on the previous |
| Parallel | `asyncio.gather(A, B, C)` | Independent tasks, want speed |
| Swarm | `for topic in topics: specialist(topic)` | Unknown number of sub-tasks |
| Agent-as-tool | Agent registered as a tool schema | Orchestrator LLM picks which agent |
| Class-based | `system.register()` + `system.route()` | Production with many specialists |

---

## You've Completed Pass 1!

You can now:
✓ **Read** orchestrator routing patterns (classify → route → call)
✓ **Recognize** specialists as `run_agent()` with different config
✓ **Spot** sequential handoff chains (output → next input)
✓ **See** parallel patterns (`asyncio.gather`)
✓ **Translate** CrewAI crew/agent/task code to direct API calls
✓ **Identify** agent-as-tool (meta-pattern)

**Next:**
- **Pass C (Visual):** See orchestration flows and handoff diagrams
- **Pass 3 (Templates):** Copy production-ready orchestration patterns
