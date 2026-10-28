# L05 — Pass 3: TEMPLATES
## Your Subagent Pipeline Copy-Paste Library

**Goal:** Five multi-agent patterns. Copy, replace the system prompts, run.

> **2026 Note:** Start with Template 1 (sequential) for almost every use case. Only move to more complex patterns when you have a clear reason — specialization, parallelism, or cost. Premature orchestration is a real failure mode.

---

## Template 1: Sequential Two-Agent Pipeline
**Use when:** Task naturally decomposes into two sequential steps

```python
import asyncio
from dataclasses import dataclass
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

@dataclass
class PipelineConfig:
    researcher_model:  str = "claude-haiku-5-5"
    writer_model:      str = "claude-sonnet-5-5"
    researcher_system: str = "You are a research specialist. Find key facts and cite sources."
    writer_system:     str = "You are a technical writer. Synthesize research into clear summaries."

async def run_agent(task: str, model: str, system: str) -> str:
    options = ClaudeAgentOptions(model=model, system_prompt=system)
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

async def research_and_write(topic: str, cfg: PipelineConfig = PipelineConfig()) -> str:
    """Two-stage pipeline: research → write."""
    print(f"  [1/2] Researching '{topic}'...")
    research = await run_agent(f"Research thoroughly: {topic}", cfg.researcher_model, cfg.researcher_system)

    print(f"  [2/2] Writing summary...")
    summary = await run_agent(f"Write a 2-sentence summary of:\n{research}", cfg.writer_model, cfg.writer_system)
    return summary

# Call:
result = asyncio.run(research_and_write("quantum computing trends 2026"))
print(result)
```

---

## Template 2: Conditional Router (3 Specialists)
**Use when:** Tasks arrive with different types and each type needs a different expert

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

ROUTER_SYSTEM = (
    "You are a task classifier. Respond with ONLY one word: "
    "'math', 'research', or 'write'."
)
SPECIALIST_SYSTEMS = {
    "math":     "You are a math tutor. Solve step by step.",
    "research": "You are a researcher. Find facts and cite sources.",
    "write":    "You are a writer. Produce clear, engaging content.",
}

async def run_agent(task: str, system: str) -> str:
    options = ClaudeAgentOptions(model="claude-sonnet-5-5", system_prompt=system)
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

async def routed_agent(task: str) -> str:
    """Classify intent → route to specialist."""
    intent = (await run_agent(task, ROUTER_SYSTEM)).strip().lower()
    system = SPECIALIST_SYSTEMS.get(intent, SPECIALIST_SYSTEMS["research"])
    print(f"  → Routed to: {intent} specialist")
    return await run_agent(task, system)

# Call:
print(asyncio.run(routed_agent("What is 15% of 240?")))         # → math
print(asyncio.run(routed_agent("What is RAG?")))                 # → research
print(asyncio.run(routed_agent("Write a haiku about agents")))   # → write
```

---

## Template 3: Orchestrator With Agent Tool (SDK Subagents)
**Use when:** The orchestrator should decide at runtime what to delegate and to whom

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

ORCHESTRATOR_SYSTEM = (
    "You are a project orchestrator. For complex tasks, use the Agent tool to "
    "delegate focused subtasks to specialists. "
    "Synthesize all results into a final answer."
)

async def orchestrated_pipeline(task: str) -> str:
    """Orchestrator spawns subagents via the Agent tool."""
    options = ClaudeAgentOptions(
        model="claude-sonnet-5-5",
        system_prompt=ORCHESTRATOR_SYSTEM,
        allowed_tools=["Agent"],    # ← permission to spawn subagents
    )
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# Call:
result = asyncio.run(orchestrated_pipeline(
    "Research quantum computing trends and write a 3-bullet executive summary"
))
print(result)
# → Orchestrator spawns researcher → gets findings → writes summary
```

---

## Template 4: Pipeline With Structured Handoff
**Use when:** Agents need to pass structured data (not raw strings) between them

```python
import asyncio
from pydantic import BaseModel, Field
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

class ResearchOutput(BaseModel):
    topic: str = Field(description="Research topic")
    key_findings: list[str] = Field(description="3-5 key facts")
    confidence: str = Field(description="high | medium | low")

async def run_researcher(topic: str) -> ResearchOutput:
    options = ClaudeAgentOptions(
        model="claude-haiku-5-5",
        system_prompt="Research the topic. Return ONLY a JSON object matching this schema: "
                      f"{ResearchOutput.model_json_schema()}"
    )
    async for msg in query(prompt=f"Research: {topic}", options=options):
        if isinstance(msg, ResultMessage):
            import json
            data = json.loads(msg.result)
            return ResearchOutput(**data)
    return ResearchOutput(topic=topic, key_findings=[], confidence="low")

async def run_writer(research: ResearchOutput) -> str:
    findings_text = "\n".join(f"- {f}" for f in research.key_findings)
    options = ClaudeAgentOptions(system_prompt="Write clear, engaging summaries.")
    prompt = f"Write a 2-sentence summary of these findings on {research.topic}:\n{findings_text}"
    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

async def structured_pipeline(topic: str) -> str:
    research = await run_researcher(topic)
    return await run_writer(research)

asyncio.run(structured_pipeline("RAG systems in 2026"))
```

---

## Template 5: Three-Stage Pipeline With Logging
**Use when:** More than 2 stages, with observability for debugging

```python
import asyncio, time
from dataclasses import dataclass, field
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

@dataclass
class PipelineLog:
    stages: list[dict] = field(default_factory=list)

    def record(self, stage: str, result: str, duration_s: float) -> None:
        self.stages.append({"stage": stage, "chars": len(result), "duration_s": round(duration_s, 2)})

    def print_summary(self) -> None:
        print("\nPipeline summary:")
        for s in self.stages:
            print(f"  {s['stage']}: {s['chars']} chars in {s['duration_s']}s")

async def run_stage(name: str, task: str, system: str, log: PipelineLog) -> str:
    print(f"  [{name}] starting...")
    t0 = time.perf_counter()
    options = ClaudeAgentOptions(model="claude-haiku-5-5", system_prompt=system)
    result = ""
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            result = msg.result
    log.record(name, result, time.perf_counter() - t0)
    return result

async def three_stage_pipeline(topic: str) -> str:
    log = PipelineLog()
    raw      = await run_stage("Researcher", f"Research: {topic}",   "Find key facts.", log)
    verified = await run_stage("Validator",  f"Validate:\n{raw}",    "Check accuracy.", log)
    final    = await run_stage("Writer",     f"Summarize:\n{verified}", "Write clearly.", log)
    log.print_summary()
    return final

asyncio.run(three_stage_pipeline("MCP protocol in 2026"))
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| Two sequential steps | Template 1: Sequential |
| Different tasks → different experts | Template 2: Router |
| LLM decides what to delegate | Template 3: Orchestrator + Agent Tool |
| Structured data between agents | Template 4: Structured Handoff |
| 3+ stages with debugging | Template 5: Three-Stage + Logging |

---

## When NOT to Use Two Agents

Use one agent when:
- The task fits in one context window
- The system prompt doesn't need to say "AND" (researcher AND writer)
- You're prototyping — start simple, split only when quality demands it
