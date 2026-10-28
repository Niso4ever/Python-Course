# L05 — Pass 1: RECOGNITION
## Learn to SEE Subagent Pipeline Patterns

**Goal:** When you see multi-agent code, instantly recognize which pattern it is — sequential, conditional, or spawn — without writing a single line.

> **2026 Note:** The two most common mistakes in multi-agent design: (1) using two agents when one is enough, (2) using one agent when two are needed. Recognition skill: spot which agents are present, what each is responsible for, and where the handoff happens.

---

## The Three Shapes of Subagent Pipelines

### Shape 1: Sequential Handoff (Output → Input)
```python
research = await run_agent("Research: " + topic, options=researcher_opts)
summary  = await run_agent("Summarize: " + research, options=writer_opts)
```
**Recognize:** Two `await run_agent()` calls in sequence. Output of the first (`research`) becomes part of the input to the second. No explicit orchestrator — just Python sequencing.

### Shape 2: The Agent Tool Permission
```python
options = ClaudeAgentOptions(
    allowed_tools=["Agent"],
    system_prompt="Delegate research tasks using the Agent tool."
)
```
**Recognize:** `"Agent"` in `allowed_tools` = this agent can spawn subagents. It's the orchestrator role. The spawned subagent runs its own complete loop and reports back.

### Shape 3: Different Models per Role
```python
orchestrator_opts = ClaudeAgentOptions(model="claude-opus-5-5", ...)
specialist_opts   = ClaudeAgentOptions(model="claude-haiku-5-5", ...)
```
**Recognize:** Intentionally different models. Expensive model for decisions (orchestrator), cheap model for execution (specialist). A design signal, not a mistake.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: The Simplest Two-Agent Pipeline
```python
async def research_and_write(topic: str) -> str:
    research = await run_agent(f"Research {topic} thoroughly", options=researcher_opts)
    summary  = await run_agent(f"Summarize:\n{research}", options=writer_opts)
    return summary
```
**Recognize:** Two `await run_agent()` calls. No routing logic. Pure sequential: research first, write second. The entire pipeline is 3 lines.

---

### Example 2: Conditional Router (3 Specialists)
```python
async def route_and_run(query: str) -> str:
    intent = await classify(query)   # returns "research" | "calculate" | "analyze"
    if intent == "research":
        return await researcher_agent(query)
    elif intent == "calculate":
        return await calculator_agent(query)
    else:
        return await analyst_agent(query)
```
**Recognize:** One classification call → `if/elif` routing → one specialist runs. The router doesn't do the work — it only decides who does. This is the "conditional dispatch" pattern from Phase 4 L05.

---

### Example 3: Orchestrator With Agent Tool
```python
orchestrator_opts = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    system_prompt=(
        "You are an orchestrator. Break complex tasks into subtasks. "
        "Use the Agent tool to delegate each subtask to a specialist."
    ),
    allowed_tools=["Agent"],
)

async for msg in query(prompt="Research quantum computing and write a brief", options=orchestrator_opts):
    if isinstance(msg, ResultMessage):
        print(msg.result)
```
**Recognize:** The orchestrator never directly researches or writes — it delegates via `"Agent"` tool. The system prompt tells it WHAT to delegate. The LLM decides WHEN.

---

### Example 4: Result Type from Researcher
```python
class ResearchResult(BaseModel):
    topic: str = Field(description="What was researched")
    findings: str = Field(description="Key facts")
    sources: list[str] = Field(description="Source references")

async def run_researcher(topic: str) -> ResearchResult:
    response = await run_agent(f"Research: {topic}", options=researcher_opts)
    return ResearchResult(topic=topic, findings=response, sources=[])
```
**Recognize:** Researcher returns a Pydantic model, not a raw string. Structured handoff between agents = less ambiguity about what the orchestrator receives.

---

### Example 5: Model Cost Optimization
```python
# Expensive model for strategic decisions
orchestrator = ClaudeAgentOptions(
    model="claude-opus-5-5",
    system_prompt="You are a strategic orchestrator. Decompose tasks carefully."
)

# Cheap model for execution work
researcher = ClaudeAgentOptions(
    model="claude-haiku-5-5",
    system_prompt="You are a research specialist. Find facts quickly."
)
```
**Recognize:** `claude-opus-5-5` for the brain, `claude-haiku-5-5` for the hands. The orchestrator does 20% of tokens but 80% of the "thinking." The subagent does the bulk of retrieval work cheaply.

---

### Example 6: Three-Stage Pipeline
```python
async def full_pipeline(topic: str) -> str:
    raw      = await run_researcher(topic)          # Stage 1: gather
    verified = await run_fact_checker(raw)          # Stage 2: validate
    report   = await run_writer(topic, verified)    # Stage 3: write
    return report
```
**Recognize:** Three sequential stages. Each stage takes the previous output as input. Spot this by counting `await run_*()` calls — each is a stage in the pipeline.

---

### Example 7: Pipeline With Logging
```python
async def pipeline(topic: str) -> str:
    print(f"[1/3] Researcher starting...")
    research = await run_researcher(topic)
    print(f"[2/3] Fact-checker reviewing ({len(research)} chars)...")
    verified = await run_fact_checker(research)
    print(f"[3/3] Writer synthesizing...")
    return await run_writer(topic, verified)
```
**Recognize:** The print statements between `await` calls are pipeline progress indicators. A tell-tale sign of sequential multi-agent code in a project.

---

### Example 8: Pipeline vs. Single Agent (SPOT THE DIFFERENCE)
```python
# Single agent — one system prompt, does everything
single_opts = ClaudeAgentOptions(
    system_prompt="You are a researcher AND a writer. Research topics and write summaries."
)

# Two-agent pipeline — each has a focused role
research_opts = ClaudeAgentOptions(system_prompt="You are a research specialist.")
writer_opts   = ClaudeAgentOptions(system_prompt="You are a technical writer.")
research = await run_agent(topic, options=research_opts)
report   = await run_agent(f"Write from this:\n{research}", options=writer_opts)
```
**Recognize:** The "AND" in a system prompt is a design smell. "Researcher AND writer" means the agent is context-switching. Two agents = cleaner identity, better outputs.
