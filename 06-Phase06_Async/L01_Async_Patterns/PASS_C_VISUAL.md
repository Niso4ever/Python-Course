# L01 — Pass C: VISUAL
## Sequential vs Concurrent — See the Difference

---

## Diagram 1: Sequential Agent Execution (Slow)

```
Time ──────────────────────────────────────────────────►

Agent 1: ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                      │
Agent 2: ░░░░░░░░░░░░░██████████████░░░░░░░░░░░░░░░░░░
                                    │
Agent 3: ░░░░░░░░░░░░░░░░░░░░░░░░░░██████████████░░░░░
                                                  │
Done ─────────────────────────────────────────────►

Total: 9 seconds (3 + 3 + 3)
```

```python
# This code produces the timeline above
result1 = await agent_research(query)   # blocks 3 sec
result2 = await agent_write(query)      # blocks 3 sec (starts AFTER research)
result3 = await agent_review(query)     # blocks 3 sec (starts AFTER write)
```

---

## Diagram 2: Concurrent Agent Execution (Fast)

```
Time ──────────────────────────────────────────────────►

Agent 1: ██████████████│
Agent 2: ██████████████│  ← all 3 finish around the same time
Agent 3: ██████████████│
                       │
Done ──────────────────►

Total: 3 seconds (longest agent wins)
```

```python
# This code produces the timeline above
result1, result2, result3 = await asyncio.gather(
    agent_research(query),   # starts immediately
    agent_write(query),      # starts immediately
    agent_review(query),     # starts immediately
)
```

---

## Diagram 3: Rate-Limited Concurrency (Semaphore)

10 tasks, but only 3 can run at a time:

```
Time ──────────────────────────────────────────────────►

Slot 1: [Task 1]  [Task 4]  [Task 7]  [Task 10]
Slot 2: [Task 2]  [Task 5]  [Task 8]
Slot 3: [Task 3]  [Task 6]  [Task 9]

         ← batch 1 →← batch 2 →← batch 3 →← b4 →
```

```python
semaphore = asyncio.Semaphore(3)  # only 3 slots

async def limited_agent(task):
    async with semaphore:         # waits for a free slot
        return await run_agent(task)

await asyncio.gather(*[limited_agent(t) for t in tasks])
```

---

## Diagram 4: Producer-Consumer Queue Pipeline

```
 ┌─────────────┐     ┌─────────┐     ┌─────────────┐
 │  Researcher  │────►│  Queue  │────►│   Writer    │
 │  (produces)  │     │ (buffer)│     │  (consumes) │
 └─────────────┘     └─────────┘     └─────────────┘

Timeline:
Researcher: [fetch1] [fetch2] [fetch3] [done]
Queue:       ░░░░░░█░░░░░░██░░░░░░███░░░░░empty
Writer:      ░░░░░░░[write1]░[write2]░░[write3]

Both run simultaneously. Writer processes items as they arrive.
```

---

## Diagram 5: The Full Multi-Agent Pipeline

Real-world pattern combining multiple async concepts:

```
                    ┌─────────────────────────────────┐
                    │         Orchestrator             │
                    │     asyncio.run(main())          │
                    └──────────┬──────────────────────┘
                               │
                    ┌──────────▼──────────────────────┐
                    │     asyncio.gather(              │
                    │       process(doc1),             │
                    │       process(doc2),             │
                    │       process(doc3),             │
                    │     )                            │
                    └──┬──────────┬──────────┬────────┘
                       │          │          │
              ┌────────▼┐  ┌─────▼────┐  ┌──▼───────┐
              │ process  │  │ process  │  │ process  │
              │ (doc1)   │  │ (doc2)   │  │ (doc3)   │
              └────┬─────┘  └────┬─────┘  └────┬─────┘
                   │             │             │
            ┌──────▼──────┐     ...           ...
            │ Semaphore(3)│
            │ ┌─────────┐ │
            │ │summarize│ │  ← sequential within each doc
            │ └────┬────┘ │
            │ ┌────▼────┐ │
            │ │ extract  │ │
            │ └─────────┘ │
            └─────────────┘

Key insight:
- BETWEEN documents → concurrent (gather)
- WITHIN each document → sequential (await, await)
- ACROSS all documents → rate-limited (semaphore)
```

---

## Decision Flowchart: Which Async Pattern?

```
Do you have multiple independent tasks?
├── YES → Do they share an API with rate limits?
│         ├── YES → Semaphore + gather
│         └── NO  → Just gather
└── NO  → Does one task feed another?
          ├── YES → Queue (producer/consumer)
          └── NO  → Just await (sequential is fine)
```
