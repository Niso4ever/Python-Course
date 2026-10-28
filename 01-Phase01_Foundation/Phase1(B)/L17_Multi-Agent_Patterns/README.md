# Lesson 17 Templates: Multi-Agent Patterns

One LLM is a solo musician. Multi-agent is an orchestra — specialized, coordinated, parallel.

## Learning Materials
The lesson file covers all 4 patterns with full code examples, CrewAI syntax, and decision guide.

## Templates
1. **PASS1_RECOGNITION.md** - 8 multi-agent patterns from real production code
2. **PASS_C_VISUAL.md** - Visual diagrams: 4 patterns side-by-side, CrewAI anatomy, agent communication
3. **CHEATSHEET_L17.py** - Quick reference for all multi-agent signals
4. **template_multi_agent.py** - 4 patterns: sequential pipeline, hierarchical, parallel fan-out, critic-actor (all with simulated demos)

## The Four Patterns
```
Sequential:   agent1 → agent2 → agent3 → answer
Hierarchical: supervisor → assigns workers → combines results
Parallel:     asyncio.gather(agent1, agent2, agent3) → merge
Critic-Actor: actor drafts → critic reviews → repeat
```

## The Key Insight
Start with one agent. Add more only when it hits quality ceilings.
Decomposition is the decision: "Can this be split into independent specialized subtasks?"
