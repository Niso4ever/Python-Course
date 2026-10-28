# Lesson 17: Multi-Agent Patterns

**Estimated time: 1 hour**

---

## The Orchestra Theory

One LLM asked to do everything is like asking a single musician to play every instrument simultaneously. It can sort of do it — but not well.

An **orchestra** assigns each instrument to a specialist:
- **Violins** handle melody (Researcher agent)
- **Percussion** provides rhythm (Planner agent)
- **Bass** gives foundation (Critic agent)
- **Conductor** coordinates everything (Orchestrator agent)

Each musician plays their part perfectly. The conductor ensures they play at the right time in the right order. Together, they create something no solo musician could.

Multi-agent systems work the same way.

---

## Why Multi-Agent Instead of One Big Prompt?

One LLM trying to research + plan + write + review simultaneously suffers from:

1. **Attention dilution** — too many concerns → mediocre at each
2. **No specialization** — can't be expert researcher AND expert critic simultaneously
3. **Context overflow** — one agent doing 5 tasks fills context fast
4. **No parallelism** — one agent is sequential; 5 agents can run at once

Multi-agent solves this by decomposition: each agent is an expert at one thing.

---

## The Four Main Patterns

### Pattern 1: Sequential Pipeline (Assembly Line)

Each agent passes work to the next. Output of agent N is input of agent N+1.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Researcher│ →  │ Analyzer │ →  │  Writer  │ →  │  Editor  │
│  (finds   │    │ (extracts│    │ (drafts  │    │ (polishes│
│   facts)  │    │  insights│    │  content)│    │  output) │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

```python
# Sequential pipeline — each step builds on the last
def run_pipeline(topic: str) -> str:
    # Agent 1: Research
    research = researcher_agent.run(f"Find key facts about: {topic}")

    # Agent 2: Analysis (uses research output)
    analysis = analyzer_agent.run(f"Analyze these facts:\n{research}")

    # Agent 3: Writing (uses analysis output)
    draft = writer_agent.run(f"Write an article based on:\n{analysis}")

    # Agent 4: Editing (uses draft)
    final = editor_agent.run(f"Polish this draft:\n{draft}")

    return final
```

**When to use:** Tasks with clear sequential stages. Research → write → review.
**Weakness:** If one agent fails, the whole pipeline stalls.

---

### Pattern 2: Hierarchical (Supervisor/Worker)

A supervisor agent breaks work into tasks and assigns them to worker agents. Workers report results back.

```
              ┌─────────────────┐
              │   SUPERVISOR    │
              │ (plans + routes)│
              └────────┬────────┘
                       │ assigns tasks
          ┌────────────┼────────────┐
          │            │            │
   ┌──────▼──┐  ┌──────▼──┐  ┌──────▼──┐
   │ Worker 1│  │ Worker 2│  │ Worker 3│
   │(research│  │(write   │  │(check   │
   │ agent)  │  │ agent)  │  │ facts)  │
   └──────┬──┘  └──────┬──┘  └──────┬──┘
          │            │            │
          └────────────┴────────────┘
                       │ reports results
              ┌────────▼────────┐
              │   SUPERVISOR    │
              │ (combines +     │
              │  final answer)  │
              └─────────────────┘
```

```python
# Supervisor pattern — LLM decides which agent to call
SUPERVISOR_PROMPT = """You are a supervisor. You have these worker agents:
- researcher: Find information and facts
- writer: Draft documents and content
- fact_checker: Verify claims for accuracy

Given the task, call the right agent(s) in the right order.
When all work is done, compile the final answer."""

def supervisor_run(task: str):
    messages = [{"role": "user", "content": task}]

    while True:
        # Supervisor decides next action
        response = client.messages.create(
            model="claude-sonnet-5-5",
            system=SUPERVISOR_PROMPT,
            tools=WORKER_TOOLS,   # workers defined as tools!
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text   # supervisor's final answer

        if response.stop_reason == "tool_use":
            # Supervisor called a worker agent
            for block in response.content:
                if block.type == "tool_use":
                    worker_result = run_worker(block.name, block.input)
                    # Feed worker result back to supervisor
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": [{"type": "tool_result",
                                     "tool_use_id": block.id,
                                     "content": worker_result}]
                    })
```

**When to use:** Complex tasks with variable subtasks. The supervisor adapts dynamically.
**Strength:** Flexible — supervisor routes based on what each task actually needs.

---

### Pattern 3: Parallel Fan-Out (Speed)

Multiple agents work simultaneously on different parts of the same problem. Results are combined.

```
               ┌─────────────────┐
               │   ORCHESTRATOR  │
               │  "split & merge"│
               └───────┬─────────┘
                       │ splits work
         ┌─────────────┼─────────────┐
         │             │             │
  ┌──────▼──┐   ┌──────▼──┐  ┌──────▼──┐
  │ Agent A │   │ Agent B │  │ Agent C │
  │(section │   │(section │  │(section │
  │  1 of 3)│   │  2 of 3)│  │  3 of 3)│
  └──────┬──┘   └──────┬──┘  └──────┬──┘
         │             │             │
         └─────────────┴─────────────┘
                       │ gather results
               ┌───────▼─────────┐
               │   ORCHESTRATOR  │
               │  "combine into  │
               │  final answer"  │
               └─────────────────┘
```

```python
import asyncio

async def parallel_agent(prompt: str, section: str) -> str:
    """One agent handling one section in parallel."""
    response = await async_client.messages.create(
        model="claude-sonnet-5-5",
        messages=[{"role": "user", "content": f"{prompt}\n\nFocus on: {section}"}]
    )
    return response.content[0].text

async def fan_out_run(topic: str) -> str:
    """Run multiple agents in parallel, combine results."""
    sections = ["introduction", "main analysis", "conclusion", "recommendations"]

    # All 4 agents run at the same time ← this is the fan-out
    results = await asyncio.gather(*[
        parallel_agent(f"Write about {topic}", section)
        for section in sections
    ])

    # Combine results (merge back in)
    full_document = "\n\n".join(results)
    return full_document
    # Time: 4 agents × 5s = 5s (not 20s) ← parallel speedup
```

**When to use:** Large tasks that can be split (long documents, parallel research, batch processing).
**Strength:** Speed — N tasks take same time as 1 task when fully parallel.

---

### Pattern 4: Debate / Critic-Actor (Quality)

One agent proposes. Another critiques. They iterate until quality is met.

```
   ┌──────────┐  draft   ┌──────────┐
   │  ACTOR   │ ──────→  │  CRITIC  │
   │(generates│          │(reviews, │
   │  answer) │ ←──────  │ finds    │
   └──────────┘  revised │ flaws)   │
         ↑        draft  └──────────┘
         │                     │
         │   [loop until good] │
         └─────────────────────┘
```

```python
def critic_actor_run(task: str, max_rounds=3) -> str:
    draft = actor_agent.run(task)   # First draft

    for round in range(max_rounds):
        # Critic reviews the draft
        critique = critic_agent.run(
            f"Review this draft for quality and accuracy:\n{draft}\n"
            f"List specific improvements needed."
        )

        # Check if critic is satisfied
        if "looks good" in critique.lower() or "approved" in critique.lower():
            break   # Critic is happy → exit loop

        # Actor revises based on critique
        draft = actor_agent.run(
            f"Improve this draft based on this critique:\n\n"
            f"Draft: {draft}\n\nCritique: {critique}"
        )

    return draft   # Return best version after N rounds
```

**When to use:** High-stakes output (legal docs, medical advice, code review).
**Strength:** Self-improvement — the system catches its own errors before they reach users.

---

## CrewAI: The Framework for Multi-Agent Systems

CrewAI is the most popular Python library for multi-agent systems:

```python
from crewai import Agent, Task, Crew, Process

# Define specialized agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find accurate, current information on any topic",
    backstory="Expert at finding and synthesizing information from multiple sources",
    verbose=True,
    tools=[search_tool, web_scraper_tool]
)

writer = Agent(
    role="Content Writer",
    goal="Write clear, engaging content from research",
    backstory="Experienced writer who turns complex info into readable content",
    verbose=True
)

editor = Agent(
    role="Senior Editor",
    goal="Ensure content quality, accuracy, and readability",
    backstory="Meticulous editor who catches errors and improves clarity",
    verbose=True
)

# Define tasks (what each agent does)
research_task = Task(
    description="Research the latest developments in {topic}. Include key facts and data.",
    agent=researcher,
    expected_output="Detailed research notes with citations"
)

writing_task = Task(
    description="Write a 500-word article based on the research provided.",
    agent=writer,
    expected_output="Well-structured article draft"
)

editing_task = Task(
    description="Edit and polish the article for publication.",
    agent=editor,
    expected_output="Publication-ready article"
)

# Assemble the crew (sequential pipeline)
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,   # ← runs tasks in order
    verbose=True
)

# Run the crew
result = crew.kickoff(inputs={"topic": "quantum computing"})
print(result)
```

---

## Agent Communication Patterns

Agents communicate through four main channels:

```python
# METHOD 1: Direct output passing (most common)
result1 = agent1.run(task)
result2 = agent2.run(result1)   # output of 1 is input of 2

# METHOD 2: Shared state dict (all agents read/write one dict)
shared_state = {"research": "", "draft": "", "feedback": ""}
researcher.run(state=shared_state)   # writes to shared_state["research"]
writer.run(state=shared_state)       # reads research, writes draft

# METHOD 3: Message queue (async, decoupled)
import queue
message_queue = queue.Queue()
agent1.put(message_queue, result)    # agent1 produces
agent2.get(message_queue)            # agent2 consumes

# METHOD 4: Database (persistent, scalable)
import sqlite3
agent1_result = "research findings"
db.execute("INSERT INTO agent_outputs VALUES (?, ?)", ("researcher", agent1_result))
agent2_input = db.execute("SELECT output FROM agent_outputs WHERE agent='researcher'").fetchone()
```

---

## Reading Multi-Agent Code in the Wild

```
You see this                              You understand
────────────────────────────────────────  ────────────────────────────────────
Agent(role=..., goal=..., tools=[...])    CrewAI agent definition
Task(description=..., agent=...)          Task assigned to specific agent
Crew(agents=[], tasks=[], process=...)    Multi-agent crew definition
Process.sequential / Process.hierarchical Pipeline vs supervisor pattern
crew.kickoff(inputs={...})                Run the entire crew
asyncio.gather(*[agent(x) for x in ...]) Parallel fan-out
supervisor_agent + tools=WORKER_TOOLS     Supervisor pattern (workers as tools)
critic.run() + actor.run()                Critic-actor pattern
shared_state / message_queue              Agent communication channel
max_iter in AgentExecutor                 Safety limit on agent loops
```

---

## When to Use Which Pattern?

```
Task type                                 Best pattern
───────────────────────────────────────   ─────────────────
Fixed stages (research → write → edit)   Sequential Pipeline
Unknown number of steps                  Hierarchical (Supervisor)
Same task, many inputs                   Parallel Fan-Out
High-stakes output (must be correct)     Critic-Actor (Debate)
Complex project combining all            Hierarchical + Fan-Out hybrid
```

---

## The Key Insight: Decomposition Is Architecture

The question "Should I use one agent or many?" is really: "Can I decompose this problem into independent, specialized subtasks?"

If yes → multi-agent is better
If no → one agent is simpler

```
One big agent:
  ✓ Simple to build
  ✓ No coordination overhead
  ✗ Jack of all trades, master of none
  ✗ Context fills up fast
  ✗ Sequential, slow

Multi-agent:
  ✓ Each agent excels at its specialty
  ✓ Parallel execution possible
  ✓ Context distributed across agents
  ✗ More code to write
  ✗ Coordination can fail
  ✗ Harder to debug
```

Start with one agent. When it hits quality ceilings, decompose.

---

## Pattern Recognition Summary

| Pattern | Signal in code |
|:--------|:---------------|
| Sequential pipeline | `result = agent2.run(agent1.run(...))` |
| Hierarchical | `supervisor + workers_as_tools` |
| Parallel fan-out | `asyncio.gather(*[agent(x) for x in ...])` |
| Critic-actor | `for round in max_rounds: draft → critique → revise` |
| CrewAI | `Agent + Task + Crew + crew.kickoff()` |
| Shared state | `state = {}` passed to all agents |
| Worker as tool | `worker defined in TOOLS list, called by supervisor` |

**Congratulations — Phase 1B complete!**

You can now read production AI systems and understand:
- How memory is managed (L12)
- How agents reason step-by-step (L13)
- How DSPy replaces hand-written prompts (L14)
- How multiple agents coordinate as a system (L15)

**Next: Phase 2 — Build Real Systems**
Time to build: RAG Pipeline, Single Agent, Multi-Agent CrewAI, DSPy Pipeline.
