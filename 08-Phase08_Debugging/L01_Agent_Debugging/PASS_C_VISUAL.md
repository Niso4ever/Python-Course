# L01 — Pass C: VISUAL
## Agent Failure Modes — Visualized

---

## Diagram 1: Context Window Overflow (The Truncation Bug)

```
Tokens
4000 │ ┌──────────────────────────────────────┐  ← Context Limit
     │ │                                      │
3000 │ │  Recent Conversation                 │
     │ │                                      │
2000 │ ├──────────────────────────────────────┤
     │ │                                      │
1000 │ │  Tool Results                        │
     │ │                                      │
 500 │ ├──────────────────────────────────────┤  ← TRUNCATION LINE
     │ │  System Prompt / Core Instructions   │  ← DELETED!
   0 │ └──────────────────────────────────────┘

Result: The agent continues chatting but suddenly "forgets" the rules,
its persona, or the format it was supposed to output.
```

---

## Diagram 2: The Infinite Tool Loop (Hallucination Trap)

```
┌─────────┐
│  Agent  │──► [Tool: read_file("config.json")]
└────▲────┘
     │         ┌──────────┐
     └─────────│ File Not │
               │  Found   │
               └──────────┘
                  (Try again...)
┌─────────┐
│  Agent  │──► [Tool: read_file("config.json")]
└────▲────┘
     │         ┌──────────┐
     └─────────│ File Not │
               │  Found   │
               └──────────┘
                 (Try again...)
                    ...

Result: Agent burns through tokens doing the exact same failing action.
Fix: Hard limit on tool calls (e.g., max_steps=5).
```

---

## Diagram 3: State Corruption (Race Condition)

```
Time ──────────────────────────────────────────────────►

File Content:   "[]"                  (empty list)

Agent A reads:  "[]"
Agent B reads:  "[]"

Agent A adds 1: "[1]"
Agent A writes: "[1]"

File Content:   "[1]"

Agent B adds 2: "[2]"                 (B never saw A's update!)
Agent B writes: "[2]"

File Content:   "[2]"                 (A's data is OVERWRITTEN/LOST)

Fix: Use an asyncio.Lock() around read-modify-write blocks.
```

---

## Diagram 4: Trace Logging vs Standard Output

```
Standard Output (What the user sees):
"I found the error on line 42."

Trace Log (What the AI Architect sees):
1. [INPUT] user: "Debug this file"
2. [THINK] "I should read the file first."
3. [TOOL_CALL] read_file("app.py")
4. [TOOL_RES] "...line 41: x = 5\nline 42: print(y)..."
5. [THINK] "Ah, y is undefined on line 42."
6. [OUTPUT] "I found the error on line 42."

Why traces matter: If the output is wrong, the trace shows WHERE the
logic derailed (e.g., did it read the wrong file, or misinterpret the text?).
```

---

## Diagram 5: The Repair Loop

```
┌─────────┐
│  Agent  │──► "{'action': fold}"  (Invalid JSON - missing quotes)
└────▲────┘
     │         ┌───────────────────────┐
     │         │ JSON Parse Error      │
     └─────────│ (Injected as new msg) │
               └───────────────────────┘
┌─────────┐
│  Agent  │──► '{"action": "fold"}' (Agent sees error and fixes it)
└─────────┘

Metrics to track:
- total_repairs_attempted
- successful_repairs
- failed_repairs (crashed anyway)
```

---

## Decision Flowchart: How to Debug an Agent

```
Did the agent crash with a Python exception?
├── YES → Normal debugging (check stack trace, types, API keys)
└── NO  → Did it produce the wrong output or get stuck?
          ├── YES → Did it loop on tool calls?
          │         ├── YES → Bad tool description or missing fallback
          │         └── NO  → Is it a long conversation?
          │                   ├── YES → Check if truncation happened (Diagram 1)
          │                   └── NO  → Check the reasoning trace (Diagram 4)
          │
          └── NO  → Is data missing from memory/files?
                    └── Check for concurrency race conditions (Diagram 3)
```
