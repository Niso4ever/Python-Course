# PASS 1: Multi-Agent Pattern Recognition

**Rule:** Read each example. Identify the pattern: sequential, hierarchical, parallel, or critic-actor.

---

## Example 1: Sequential Pipeline

```python
# Pattern signal: output of one agent = input of next
def run_content_pipeline(topic: str) -> str:
    # Stage 1: Research
    research = research_agent.run(
        f"Find key facts and statistics about: {topic}"
    )

    # Stage 2: Outline (uses research output)
    outline = outline_agent.run(
        f"Create a structured outline based on:\n{research}"
    )

    # Stage 3: Write (uses outline)
    draft = writer_agent.run(
        f"Write a 500-word article based on this outline:\n{outline}"
    )

    # Stage 4: Edit (uses draft)
    final = editor_agent.run(
        f"Polish and improve this draft:\n{draft}"
    )

    return final   # linear chain complete
```

**Pattern:** Sequential Pipeline
**Signal:** Each `.run()` uses the previous result as input
**When to use:** Research → write → review workflows

---

## Example 2: Hierarchical (Supervisor Routes to Workers)

```python
# Pattern signal: supervisor decides WHICH worker to call
SUPERVISOR_SYSTEM = """You are a task supervisor with access to specialized workers:
- researcher: Find information and facts on any topic
- writer: Draft and write content
- fact_checker: Verify claims for accuracy and truth

Analyze the task and call the right worker(s) in the right order.
When all work is complete, compile the final answer."""

def supervisor_agent(task: str) -> str:
    messages = [{"role": "user", "content": task}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-5-5",
            system=SUPERVISOR_SYSTEM,
            tools=WORKER_TOOLS,      # ← workers defined as tool calls
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text   # supervisor's final answer

        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    # supervisor calls a worker
                    result = workers[block.name](block.input)
                    # result fed back to supervisor
```

**Pattern:** Hierarchical (Supervisor/Worker)
**Signal:** `SUPERVISOR_SYSTEM` + workers defined as tools
**When to use:** Complex tasks with variable subtasks; supervisor adapts

---

## Example 3: Parallel Fan-Out (Speed)

```python
import asyncio

async def parallel_research(topic: str, aspects: list[str]) -> str:
    """Research multiple aspects simultaneously."""

    async def research_one(aspect: str) -> str:
        response = await async_client.messages.create(
            model="claude-sonnet-5-5",
            messages=[{"role": "user", "content": f"Research {aspect} of {topic}"}]
        )
        return response.content[0].text

    # All aspects researched AT THE SAME TIME ← this is the fan-out
    results = await asyncio.gather(*[       # ← parallel execution
        research_one(aspect)
        for aspect in aspects
    ])

    # Merge back in ← fan-in
    return "\n\n".join(f"## {a}\n{r}" for a, r in zip(aspects, results))

# Time: 4 aspects × 5s = 5s (not 20s)
```

**Pattern:** Parallel Fan-Out
**Signal:** `asyncio.gather(*[agent(x) for x in list])`
**When to use:** Same task applied to many inputs; large docs split into sections

---

## Example 4: Critic-Actor (Self-Improvement Loop)

```python
def critic_actor_pipeline(task: str, max_rounds: int = 3) -> str:
    """Actor drafts. Critic reviews. Repeat until good."""

    # Round 0: Initial draft
    draft = actor_agent.run(task)
    print(f"Initial draft: {draft[:80]}...")

    for round_num in range(max_rounds):
        # Critic evaluates the draft
        critique = critic_agent.run(
            f"Review this draft critically. List specific improvements needed:\n\n{draft}"
        )

        # Check if critic approves
        if any(word in critique.lower() for word in ["approved", "looks good", "no issues"]):
            print(f"Critic approved after {round_num + 1} rounds.")
            break

        print(f"Round {round_num + 1} critique: {critique[:60]}...")

        # Actor revises based on feedback
        draft = actor_agent.run(
            f"Revise this draft based on the following critique:\n\n"
            f"Current draft:\n{draft}\n\n"
            f"Critique:\n{critique}"
        )

    return draft
```

**Pattern:** Critic-Actor
**Signal:** `for round in range(max_rounds): draft → critique → revise`
**When to use:** High-stakes output; legal, medical, financial content

---

## Example 5: CrewAI (Framework)

```python
from crewai import Agent, Task, Crew, Process

# Define agents with roles and goals
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find accurate, comprehensive information on any topic",
    backstory="Expert at synthesizing information from multiple sources",
    verbose=True,
    tools=[search_tool]   # ← agents can have tools (L11 pattern!)
)

writer = Agent(
    role="Content Writer",
    goal="Write clear, engaging content from research",
    backstory="Experienced at turning complex information into readable content"
)

# Define tasks assigned to specific agents
research_task = Task(
    description="Research {topic} thoroughly. Include key statistics and recent developments.",
    agent=researcher,
    expected_output="Detailed research notes with key facts and data"
)

writing_task = Task(
    description="Write a 500-word article using the research provided.",
    agent=writer,
    expected_output="Well-structured article draft"
)

# Assemble crew (sequential)
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,   # ← sequential pipeline pattern
    verbose=True
)

result = crew.kickoff(inputs={"topic": "quantum computing"})
```

**Pattern:** Sequential Pipeline (via CrewAI)
**Signal:** `Agent + Task + Crew + crew.kickoff()`
**Key insight:** CrewAI wraps the sequential pipeline pattern in a clean framework

---

## Example 6: CrewAI Hierarchical Process

```python
from crewai import Agent, Task, Crew, Process

manager = Agent(
    role="Project Manager",
    goal="Coordinate team to produce the best possible output",
    backstory="Expert project manager who delegates effectively"
)

researcher = Agent(role="Researcher", goal="Find accurate information", ...)
writer     = Agent(role="Writer",     goal="Write clear content", ...)
reviewer   = Agent(role="Reviewer",   goal="Ensure quality standards", ...)

crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[...],
    process=Process.hierarchical,   # ← supervisor/worker pattern
    manager_agent=manager,          # ← explicit manager agent
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI trends"})
# Manager decides which agent handles what, in what order
```

**Pattern:** Hierarchical (via CrewAI)
**Signal:** `Process.hierarchical` + `manager_agent=...`
**Difference from sequential:** Manager dynamically assigns tasks; order is flexible

---

## Example 7: Shared State (Agent Communication)

```python
# Pattern: all agents read/write the same state dictionary
class MultiAgentPipeline:
    def __init__(self):
        self.state = {     # ← SHARED STATE
            "research":   "",
            "outline":    "",
            "draft":      "",
            "critiques":  [],
            "final":      ""
        }

    def research(self, topic: str):
        result = researcher_llm.run(f"Research: {topic}")
        self.state["research"] = result    # ← WRITES to shared state

    def write(self):
        # READS research, WRITES draft
        result = writer_llm.run(f"Write based on:\n{self.state['research']}")
        self.state["draft"] = result

    def critique(self):
        # READS draft, WRITES critique
        result = critic_llm.run(f"Review:\n{self.state['draft']}")
        self.state["critiques"].append(result)

    def run_pipeline(self, topic: str) -> str:
        self.research(topic)
        self.write()
        self.critique()
        return self.state["draft"]
```

**Pattern:** Sequential Pipeline with Shared State
**Signal:** `self.state = {}` + each method reads previous stage output
**Advantage:** Complete audit trail — you can inspect state at any stage

---

## Example 8: `intermediate_steps` Inspection (Multi-Agent Debug)

```python
# When a LangChain multi-agent pipeline runs:
result = crew.kickoff(inputs={"topic": "AI news"})

# Inspect what each agent did:
for task_output in result.tasks_output:
    print(f"Agent: {task_output.agent}")
    print(f"Task: {task_output.description[:60]}")
    print(f"Output: {task_output.raw[:100]}")
    print("---")

# Output:
# Agent: Senior Research Analyst
# Task: Research AI news thoroughly...
# Output: Key developments: 1) Claude 4 released...
# ---
# Agent: Content Writer
# Task: Write a 500-word article...
# Output: Artificial Intelligence continues to advance...
```

**When to use:** Debugging — see exactly what each agent produced
**Connects to L10:** Same "print audit" debugging principle from the debugging lesson

---

## Pattern Summary Table

| Code signal | Multi-agent pattern |
|:-----------|:--------------------|
| `agent2.run(agent1.run(...))` | Sequential pipeline |
| `supervisor + tools=WORKER_TOOLS` | Hierarchical (supervisor/worker) |
| `asyncio.gather(*[agent(x) for x in ...])` | Parallel fan-out |
| `for round in range(N): draft → critique → revise` | Critic-actor |
| `Agent + Task + Crew + crew.kickoff()` | CrewAI framework |
| `Process.sequential` | Sequential (CrewAI) |
| `Process.hierarchical + manager_agent=...` | Hierarchical (CrewAI) |
| `self.state = {}` shared across methods | Shared state communication |
| `tasks_output` / `intermediate_steps` | Full agent trace (for debugging) |
