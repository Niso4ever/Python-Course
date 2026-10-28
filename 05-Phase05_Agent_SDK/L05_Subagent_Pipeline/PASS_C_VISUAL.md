# L05 — Visual: Two-Agent Pipeline (Subagents)

## Single Agent vs. Two-Agent Pipeline

```
SINGLE AGENT                            TWO-AGENT PIPELINE
──────────────────────                  ────────────────────────────────────────
User: "Research quantum computing       User: "Research quantum computing
       and write a summary"                    and write a summary"
         │                                       │
         ▼                                       ▼
  ┌─────────────┐                        ┌─────────────────┐
  │   AGENT     │                        │  ORCHESTRATOR   │
  │ system:     │                        │  system: "Break │
  │ "Research   │                        │  tasks down and │
  │  AND write" │                        │  delegate"      │
  │ (confused   │                        └────────┬────────┘
  │  identity)  │                                 │ spawns
  └─────────────┘                                 ▼
                                         ┌─────────────────┐
                                         │   RESEARCHER    │
                                         │  system: "You   │
                                         │  are a research │
                                         │  specialist"    │
                                         └────────┬────────┘
                                                  │ research result
                                                  ▼
                                         ┌─────────────────┐
                                         │ ORCHESTRATOR    │
                                         │ assembles final │
                                         │ summary         │
                                         └─────────────────┘
```

---

## Subagent Spawn Flow

```
ORCHESTRATOR LOOP
├── Turn 1: User asks complex question
│       │
│       ▼ LLM decides: "I need a specialist"
│       │
│       ├── Calls Agent tool: {"task": "research quantum computing", "model": "..."}
│       │                           │
│       │             ┌─────────────┘
│       │             │
│       │    SUBAGENT LOOP (runs independently)
│       │    ├── subagent gets its task
│       │    ├── runs tools (search, lookup, etc.)
│       │    ├── iterates until done
│       │    └── returns: ResultMessage("here is the research...")
│       │             │
│       │             └─────────────┐
│       │                           │
│       ▼ tool_result received: research findings
│
├── Turn 2: Orchestrator has the research
│       │
│       ▼ LLM writes summary using the research
│       └── stop_reason: "end_turn"
│
└── ResultMessage(final_summary)
```

---

## Four Multi-Agent Patterns (From Simple to Complex)

```
PATTERN 1: SEQUENTIAL (this lesson)
  Orchestrator → Researcher → Writer → Result
  Output of each = input of next

PATTERN 2: PARALLEL (future)
  Orchestrator → Researcher ─┐
               → Analyst    ├─→ Synthesizer → Result
               → Fact-check ─┘

PATTERN 3: CONDITIONAL ROUTING (Ph4-L05 from Phase 4)
  Router classifies intent
  ├── "research" → Research agent
  ├── "write"    → Writer agent
  └── "analyze"  → Analyst agent

PATTERN 4: HIERARCHICAL (enterprise, deferred)
  Manager → Team Lead → Worker
                      → Worker
                      → Worker
```

---

## Cost Consideration

```
EXPENSIVE: Use a powerful model for the orchestrator (it makes decisions)
CHEAPER:   Use a faster/cheaper model for the specialist (it does execution)

Orchestrator: claude-opus-5-5    (strategic thinking)
Subagent:     claude-haiku-5-5   (research retrieval, data processing)

Savings: subagent does 80% of the token work at fraction of the cost
```
