# PASS C: Visual ReAct Patterns

---

## Diagram 1: The ReAct Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                        ReAct Agent Loop                         │
│                                                                 │
│  User Question ────────────────────────────────────────┐       │
│                                                        │       │
│  ┌──────────────────────────────────────────────────┐  │       │
│  │                  THOUGHT                         │  │       │
│  │  LLM reasons:                                    │  │       │
│  │  • What do I already know?                       │  │       │
│  │  • What do I still need?                         │  │       │
│  │  • Which tool gets it?                           │  │       │
│  └─────────────────┬────────────────────────────────┘  │       │
│                    │                                    │       │
│         ┌──────────▼──────────┐                        │       │
│         │   "Need more info"  │                        │       │
│         │   → picks a tool    │   "I have enough"      │       │
│         └──────────┬──────────┘         │              │       │
│                    │                    ▼              │       │
│  ┌─────────────────▼────────────┐   ┌───────────┐     │       │
│  │           ACTION             │   │  FINAL    │     │       │
│  │  call web_search("...")       │   │  ANSWER   │     │       │
│  │  call calculator("...")       │   └───────────┘     │       │
│  └─────────────────┬────────────┘                      │       │
│                    │                                    │       │
│  ┌─────────────────▼────────────┐                      │       │
│  │         OBSERVATION          │                      │       │
│  │  Tool returns result         │                      │       │
│  │  → fed back to LLM           │                      │       │
│  └─────────────────┬────────────┘                      │       │
│                    │                                    │       │
│                    └──────────────── loop ──────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagram 2: Thought/Action/Observation Text Format

```
Question: What is 15% of 8,432 and who invented Python?

┌─────────────────────────────────────────────────────────┐
│ THOUGHT #1                                              │
│ "I need a calculation for 15% of 8432.                 │
│  I know Python was created by Guido van Rossum.        │
│  Let me do the math first."                            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ ACTION #1                                               │
│ Tool: calculator                                        │
│ Input: 8432 * 0.15                                      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ OBSERVATION #1                                          │
│ 1264.8                                                  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ THOUGHT #2                                              │
│ "I have both answers. Calculator gave 1264.8.          │
│  I already knew the Python inventor. Done."            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ FINAL ANSWER                                            │
│ "15% of 8,432 is 1,264.80. Python was invented by      │
│  Guido van Rossum."                                    │
└─────────────────────────────────────────────────────────┘
```

---

## Diagram 3: ReAct vs Chain of Thought

```
CHAIN OF THOUGHT (reasoning only, no tools)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User: "A store has 500 items, sold 30%, got 80 more. Total?"
      "Let's think step by step."
         ↓
  LLM internally reasons:
  Step 1: 500 × 0.30 = 150 sold
  Step 2: 500 - 150 = 350 remaining
  Step 3: 350 + 80 = 430 total
         ↓
  Final Answer: 430 items

  ✓ No external tools needed
  ✓ Works for: math, logic, known facts
  ✗ Fails for: current events, live data, large files

REACT (reasoning + external tools)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User: "What is the current Bitcoin price?"
         ↓
  Thought: "I don't know current prices. Search."
  Action: web_search("Bitcoin price today")
  Observe: "$94,230"
         ↓
  Thought: "I have the answer."
  Final Answer: "Current Bitcoin price: $94,230"

  ✓ Gets current, real-world information
  ✓ Works for: live data, files, databases
  ✗ Slower: each tool call = API round-trip
```

---

## Diagram 4: LangChain ReAct Setup

```
CREATE THE PIECES:
────────────────────────────────────────────────────────
@tool                              ← define tools
def calculator(expr): ...          ← (L11 pattern)
def web_search(query): ...

llm = ChatAnthropic(model=...)     ← the LLM brain

prompt = hub.pull("hwchase17/react")  ← ReAct prompt template
                                       (enforces T/A/O format)

ASSEMBLE:
────────────────────────────────────────────────────────
agent = create_react_agent(         ← builds the agent
    llm=llm,
    tools=tools,
    prompt=prompt
)

executor = AgentExecutor(           ← adds the loop + safety
    agent=agent,
    tools=tools,
    verbose=True,         ← print each T/A/O step
    max_iterations=5,     ← stop after 5 loops
    handle_parsing_errors=True  ← recover from bad format
)

RUN:
────────────────────────────────────────────────────────
result = executor.invoke({"input": "Your question"})
print(result["output"])            ← final answer
print(result["intermediate_steps"])  ← full T/A/O history
```

---

## Diagram 5: `max_iterations` Safety Net

```
Without max_iterations:
  Turn 1: Thought → Action → Observe
  Turn 2: Thought → Action → Observe
  Turn 3: Thought → Action → Observe
  Turn 4: Thought → Action → Observe
  Turn ∞: [agent loops forever, costs money]

With max_iterations=5:
  Turn 1: Thought → Action → Observe
  Turn 2: Thought → Action → Observe
  Turn 3: Thought → Action → Observe
  Turn 4: Thought → Action → Observe
  Turn 5: Thought → Action → Observe
  STOP → returns best answer so far

Good defaults:
  max_iterations=5   → general purpose
  max_iterations=10  → complex research tasks
  max_iterations=3   → fast/cheap tasks
```

---

## Diagram 6: `verbose=True` Output (What You See)

```
$ python agent.py

> Entering new AgentExecutor chain...
│
├─ Thought: I need to find the current population of Tokyo.
│           I should use web_search for current data.
│
├─ Action: web_search
├─ Action Input: Tokyo population 2025
│
├─ Observation: Tokyo's population is approximately 13.96 million (city proper)
│               and 37.4 million in the greater metropolitan area.
│
├─ Thought: I have the information. Tokyo city proper has 13.96 million people.
│
└─ Final Answer: Tokyo's population is approximately 13.96 million in the
                 city proper, and 37.4 million in the greater metro area.

> Finished chain.
```

---

## Diagram 7: ReAct Decision Tree (What Triggers a Tool?)

```
LLM receives question
        │
        ▼
Is the answer in training data with high confidence?
  YES → no tool needed → reason directly → Final Answer
  NO  →
        │
        ▼
What kind of information is missing?
  ├── Current/live data  → web_search
  ├── Calculation         → calculator
  ├── Local file          → read_document
  ├── Company knowledge   → search_knowledge_base
  └── Code execution      → run_python
        │
        ▼
Call tool → get Observation
        │
        ▼
Do I have everything now?
  YES → Final Answer
  NO  → Thought → Action → Observation (loop again)
```

---

## Diagram 8: CoT vs ReAct vs Tool-Use Only

```
Question: "What is 17% of the GDP of France?"

APPROACH 1: Tool-Use Only (no reasoning)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  web_search("GDP of France")   → $2.78 trillion
  calculator(2.78e12 * 0.17)    → 472.6 billion
  Answer: $472.6 billion
  Problem: Blind tool calling. May call wrong tools.

APPROACH 2: Chain of Thought (reasoning only, no tools)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  "France GDP is approximately $2.8 trillion"
  "17% of 2.8 trillion = 476 billion"
  Answer: ~$476 billion
  Problem: LLM may have outdated GDP figure. Math may be wrong.

APPROACH 3: ReAct (reason → right tool → accurate result)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Thought: "Need current GDP → web_search. Then accurate math → calculator."
  web_search → current GDP figure
  calculator → exact percentage
  Answer: Accurate and current
  Best for: Problems needing both current data and accuracy
```
