# Lesson 21 — Pass C: VISUAL PATTERNS
## See the Orchestration Flow as a Diagram

---

## Visual 1: Router Pattern

```
User Request
      │
      ▼
┌─────────────────┐
│   ORCHESTRATOR  │ ← classifies intent (structured output)
│   (classifier)  │
└─────────────────┘
      │
  intent?
      │
  ┌───┼────────┐
  │   │        │
"re- "wr-   "an-
search" ite"  alyse"
  │   │        │
  ▼   ▼        ▼
┌───┐┌────┐┌──────┐
│ R ││ W  ││  A   │   R = Research Agent
│ e ││ r  ││  n   │   W = Writer Agent
│ s ││ i  ││  a   │   A = Analyst Agent
│ e ││ t  ││  l   │
│ a ││ e  ││  y   │
│ r ││ r  ││  s   │
└───┘└────┘└──────┘
  │    │        │
  └────┼────────┘
       ▼
   Answer returned to user
```

**Example calls:**
```python
answer = orchestrate("Research quantum computing advances.")
# → classify → "research" → research_agent() → detailed findings

answer = orchestrate("Write a blog about AI agents.")
# → classify → "write" → writer_agent() → formatted prose
```

---

## Visual 2: Sequential Handoff Pipeline

```
User Input
    │
    ▼
┌─────────────┐
│  RESEARCH   │  tools: search, arxiv
│   AGENT     │  prompt: "Be thorough and cite sources"
└─────────────┘
    │
    │  research output
    ▼
┌─────────────┐
│   WRITER    │  tools: format, outline
│   AGENT     │  input: research output above
└─────────────┘
    │
    │  draft article
    ▼
┌─────────────┐
│   EDITOR    │  tools: grammar, style
│   AGENT     │  input: draft above
└─────────────┘
    │
    ▼
 Final Article
```

**Example call:**
```python
result = pipeline("Impact of MCP on AI development")
# Step 1: research_agent("Impact of MCP...") → raw_research
# Step 2: writer_agent("Write from: " + raw_research) → draft
# Step 3: editor_agent("Improve: " + draft) → polished article
print(result["final"])   # ready-to-publish article
```

**Pattern:** Each arrow = output of one agent becomes input of the next.

---

## Visual 3: Parallel Research (asyncio)

```
Main Request: "Compare top 3 LLMs"
        │
        ▼ asyncio.gather(...)
  ┌─────┴─────┬─────────────┐
  │           │             │
  ▼           ▼             ▼
[Claude 4]  [GPT-5]   [Gemini Ultra]
research    research    research
agent       agent       agent
  │           │             │
  └─────┬─────┴─────────────┘
        ▼ all 3 complete together
  Synthesizer Agent
  ("Here are the 3 results, write a comparison")
        │
        ▼
  Comparison Report
```

**Example call:**
```python
results = asyncio.run(parallel_research(["Claude 4", "GPT-5", "Gemini Ultra"]))
print(f"Time: ~same as 1 call (parallel)")  # vs 3x time sequential
synthesis = writer_agent("Compare these: " + "\n".join(results))
```

**Pattern:** Independent tasks → run simultaneously → collect → synthesize.

---

## Visual 4: Swarm (Dynamic Spawning)

```
User: "Research agentic AI comprehensively"
           │
           ▼
    ┌──────────────┐
    │ ORCHESTRATOR │  "Identify sub-topics"
    └──────────────┘
           │
    discovers 3 sub-topics
           │
   ┌───────┼────────┐
   ▼       ▼        ▼
 Agent   Agent    Agent
"loop"  "tools"  "memory"
   │       │        │
   └───────┼────────┘
           ▼
    ┌──────────────┐
    │  SYNTHESIZER │  "Combine all research"
    └──────────────┘
           │
           ▼
     Final Report
```

**Example call:**
```python
report = research_swarm("Agentic AI in 2026")
# Orchestrator found 3 sub-topics automatically
# Spawned 3 specialist agents
# Synthesizer combined results
print(list(report["sub_research"].keys()))  # ["Agent Loop", "Tool Use", "MCP"]
```

**Pattern:** Orchestrator discovers → dynamically spawns → collects → synthesizes.

---

## Visual 5: Agent-as-Tool (Meta Pattern)

```
ORCHESTRATOR AGENT
  │
  │  has these "tools":
  │  ┌────────────────────────────────────────┐
  │  │ tool: "call_research_agent"             │
  │  │ tool: "call_writer_agent"               │
  │  │ tool: "call_analyst_agent"              │
  │  └────────────────────────────────────────┘
  │
  ▼ runs agent loop (L02)
  │
  ├── calls "call_research_agent"
  │       │
  │       └──► research_agent(task)  ← this IS an agent loop
  │                   │
  │               returns research
  │
  ├── calls "call_writer_agent" with research as context
  │       │
  │       └──► writer_agent(research)  ← another agent loop
  │                   │
  │               returns article
  │
  └── stop_reason = "end_turn" → returns article to user
```

**Example call:**
```python
result = run_orchestrator("Research Claude 4 and write a blog about it.")
# Orchestrator LOOP:
# Iteration 1: calls call_research_agent("Claude 4")
#   → sub-agent runs its own loop (3 iterations)
#   → returns research findings
# Iteration 2: calls call_writer_agent("Write about Claude 4: " + research)
#   → sub-agent runs its own loop (2 iterations)
#   → returns blog post
# Iteration 3: stop_reason=end_turn → final blog post returned
```

**Pattern:** Agents inside agents. Each level is its own loop.

---

## Visual 6: Framework Translation Map

```
CREWAI:                     DIRECT API EQUIVALENT:
─────────────────────────────────────────────────────
Agent(role="Researcher")  → run_agent(system=RESEARCHER_PROMPT, tools=RESEARCH_TOOLS)
Agent(role="Writer")      → run_agent(system=WRITER_PROMPT,     tools=WRITING_TOOLS)
Task(description="...",   → researcher_output = research_agent(task)
     context=[task1])         writer_input = f"Based on: {researcher_output}\n{task}"
crew.kickoff()            → research_result = research_agent(request)
                              write_result   = writer_agent(research_result)

LANGGRAPH:                  DIRECT API EQUIVALENT:
─────────────────────────────────────────────────────
@node("research")          → def research_agent(task): return run_agent(...)
@node("write")             → def writer_agent(task):   return run_agent(...)
graph.add_edge(A → B)      → writer_output = writer_agent(research_agent(input))
graph.invoke(state)        → orchestrate(user_input)
```

---

## Visual 7: When to Use Each Pattern

```
ONE question, one answer:
  → Single agent (L02)

Different tasks need different tools:
  → Router orchestrator

Each step depends on the last:
  → Sequential pipeline

Tasks are independent, speed matters:
  → Parallel with asyncio.gather()

Don't know how many tasks ahead of time:
  → Swarm (discover → spawn → synthesize)

Orchestrator needs to decide WHEN to call each agent:
  → Agent-as-tool (orchestrator has agents as tools)
```

---

## You've Completed Pass C!

You can now:
✓ **Visualize** the router pattern — classify → route → specialist
✓ **See** handoff chains as assembly lines
✓ **Map** parallel patterns to asyncio.gather
✓ **Understand** swarm spawning (discover → dynamic spawn)
✓ **See** agent-as-tool as nested loops
✓ **Translate** CrewAI/LangGraph to direct API calls visually

**Next:** Pass 3 — Copy production-ready orchestration templates.
