# PASS C: Visual Multi-Agent Patterns

---

## Diagram 1: The Four Patterns at a Glance

```
PATTERN 1: SEQUENTIAL PIPELINE
────────────────────────────────────────────────────────
Agent1 → Agent2 → Agent3 → Agent4 → Final Answer
(research) (outline) (write) (edit)

Each agent sees only the previous agent's output.
Like an assembly line — each worker passes the part forward.

PATTERN 2: HIERARCHICAL (Supervisor/Worker)
────────────────────────────────────────────────────────
         SUPERVISOR
        /     |     \
   Agent1  Agent2  Agent3
        \     |     /
         SUPERVISOR → Final Answer

Supervisor decides who does what. Workers report back.
Like a manager delegating to specialists.

PATTERN 3: PARALLEL FAN-OUT
────────────────────────────────────────────────────────
           ORCHESTRATOR
          / | | | | | \
      A1 A2 A3 A4 A5 A6   ← all run at same time
          \ | | | | | /
           ORCHESTRATOR → Final Answer

All agents work simultaneously. Time = 1 agent's time.
Like parallel processing instead of serial.

PATTERN 4: CRITIC-ACTOR
────────────────────────────────────────────────────────
ACTOR → draft → CRITIC → critique → ACTOR → revised draft → ...
                    ↑_________loop until "approved"_____|

Actor produces, critic improves. Self-correcting system.
Like code review or editorial review.
```

---

## Diagram 2: Sequential Pipeline Time vs Parallel

```
SEQUENTIAL (one at a time):
  Research:  [====5s====]
  Write:               [====5s====]
  Edit:                          [====5s====]
  Total: 15 seconds

PARALLEL (fan-out):
  Research:  [====5s====]
  Write:     [====5s====]  ← runs at same time!
  Edit:      [====5s====]  ← runs at same time!
  Total: 5 seconds (3× faster)

Code difference:
  Sequential: result = agent3(agent2(agent1(topic)))
  Parallel:   results = await asyncio.gather(agent1(x), agent2(x), agent3(x))
```

---

## Diagram 3: CrewAI Anatomy

```
┌─────────────────────────────────────────────────────────────┐
│  AGENT                                                       │
│  ─────────────────────────────────────────────────────────  │
│  role      = "Senior Research Analyst"  ← the job title    │
│  goal      = "Find accurate info..."   ← the objective     │
│  backstory = "Expert at..."            ← context for LLM   │
│  tools     = [search_tool, ...]        ← capabilities (L11)│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  TASK                                                        │
│  ─────────────────────────────────────────────────────────  │
│  description     = "Research {topic}..."  ← what to do     │
│  agent           = researcher             ← who does it    │
│  expected_output = "Detailed notes..."    ← what to produce│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CREW                                                        │
│  ─────────────────────────────────────────────────────────  │
│  agents  = [researcher, writer, editor]  ← team members    │
│  tasks   = [task1, task2, task3]         ← work to do      │
│  process = Process.sequential            ← how to run it   │
│  verbose = True                          ← print progress  │
└─────────────────────────────────────────────────────────────┘

crew.kickoff(inputs={"topic": "AI"})  ← START THE CREW
result.raw                             ← final output
result.tasks_output                    ← each agent's work
```

---

## Diagram 4: Hierarchical — Supervisor Pattern

```
USER INPUT
    │
    ▼
┌──────────────────────────────────────────┐
│  SUPERVISOR (LLM with worker tools)      │
│  "I need research → call researcher"     │
│  "Now write → call writer"               │
│  "Check facts → call fact_checker"       │
└──────────┬──────────┬──────────┬─────────┘
           │          │          │
    ┌──────▼──┐  ┌────▼───┐  ┌──▼──────────┐
    │RESEARCHER│  │WRITER  │  │FACT CHECKER │
    │Runs      │  │Drafts  │  │Verifies     │
    │searches  │  │content │  │claims       │
    └──────┬──┘  └────┬───┘  └──┬──────────┘
           │          │          │
           └──────────┴──────────┘
                      │ results
    ┌─────────────────▼────────────────────┐
    │  SUPERVISOR (combines results)        │
    │  Writes final answer                 │
    └──────────────────────────────────────┘

Signal in code:
  supervisor uses tools → WORKER_TOOLS
  each worker is a function = a tool
  supervisor loop = L11 tool use loop
```

---

## Diagram 5: Critic-Actor Loop

```
ROUND 1:
  ACTOR: "Here's my first draft: ..."     (rough but fast)
  CRITIC: "Issues: 1) vague intro 2) no data 3) awkward ending"

ROUND 2:
  ACTOR: "Revised draft with sharper intro, added data, fixed ending"
  CRITIC: "Better. 1) data needs citation 2) ending still weak"

ROUND 3:
  ACTOR: "Final revision with citations and stronger conclusion"
  CRITIC: "Approved — this meets quality standards"

Loop exits → best draft returned

Control:
  max_rounds=3  → at most 3 iterations (cost control)
  if "approved" in critique → exit early (quality gate)

Use cases:
  ✓ Legal document drafting
  ✓ Medical advice synthesis
  ✓ Code review automation
  ✓ Marketing copy
```

---

## Diagram 6: Agent Communication Methods

```
METHOD 1: Direct Output Chain (Sequential)
  output1 = agent1(input)
  output2 = agent2(output1)    ← output of 1 is input of 2
  Best: simple pipelines, clear data flow

METHOD 2: Shared State Dict
  state = {"research":"", "draft":""}
  agent1 writes to state["research"]
  agent2 reads state["research"], writes to state["draft"]
  Best: when multiple agents need the same information

METHOD 3: CrewAI Task Context
  Task(context=[previous_task])  ← task sees previous task's output
  CrewAI handles the passing automatically
  Best: when using CrewAI framework

METHOD 4: Message Queue (Advanced)
  import queue
  q = queue.Queue()
  agent1: q.put(result)    ← producer
  agent2: data = q.get()   ← consumer
  Best: async, decoupled, producer-consumer patterns

METHOD 5: Database (Persistent)
  agent1: db.save("research_output", result)
  agent2: data = db.load("research_output")
  Best: long-running tasks, multi-session pipelines
```

---

## Diagram 7: When to Use Each Pattern

```
Task has clear sequential stages?
  YES → Sequential Pipeline
    Example: Research → Outline → Write → Edit

Task has unknown/variable steps?
  YES → Hierarchical (Supervisor decides dynamically)
    Example: Complex analysis with unknown data needs

Same task applied to many independent inputs?
  YES → Parallel Fan-Out
    Example: Translate 10 articles, analyze 5 products

Output quality must be very high?
  YES → Critic-Actor (iterate to quality)
    Example: Legal brief, medical report, financial analysis

Working with Python framework?
  YES → CrewAI (wraps any of the above)
    Use Process.sequential or Process.hierarchical
```

---

## Diagram 8: Multi-Agent Debugging (10 Seconds)

```
Step 1: Find how many agents exist
  class Agent1, class Agent2 → 2 agents
  Agent(role="Researcher"), Agent(role="Writer") → CrewAI 2-agent system

Step 2: Find the pattern
  agent2.run(agent1.run(...)) → sequential
  asyncio.gather(...)         → parallel
  while True: supervisor...  → hierarchical
  for round: draft/critique  → critic-actor

Step 3: Find the communication method
  direct param passing    → simple chain
  self.state = {}         → shared state
  Task(context=[...])     → CrewAI context
  queue.Queue()           → message queue

Step 4: Find safety limits
  max_rounds=3            → critic-actor iteration limit
  max_iterations=5        → supervisor/react loop limit
  timeout=30              → per-agent time limit
```
