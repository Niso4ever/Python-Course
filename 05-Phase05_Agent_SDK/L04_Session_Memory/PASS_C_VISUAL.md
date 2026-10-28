# L04 — Visual: Session Memory Flow

## Stateless vs. Stateful Calls

```
STATELESS (no session_id)               STATEFUL (with session_id)
─────────────────────────────           ──────────────────────────────────────
Call 1:  query(prompt="My name is Ahmed")      Call 1:  query(prompt="My name is Ahmed")
         ↓                                       ↓
         [new context]                           [new context] → session_id = "ses_abc"
         Result: "Hello Ahmed!"                  Result: "Hello Ahmed!"
                                                           │
                                                    saves session_id
                                                           │
Call 2:  query(prompt="What is my name?")      Call 2:  query(prompt="What is my name?",
         ↓                                             resume="ses_abc")   
         [new context — forgets]                 ↓
         Result: "I don't know."                 [loads ses_abc history]
                                                 Result: "Your name is Ahmed."
```

---

## Session State Across Calls

```
CALL 1                          CALL 2                          CALL 3
──────────────────────          ──────────────────────          ──────────────────────
query(prompt="My name is Ahmed")  ──►  query(prompt="I am 35 years old", ──►  query(prompt="Summarize what
                                      resume=s_id)                  you know about me",
                                                                     resume=s_id)    
        │                               │                               │
        ▼                               ▼                               ▼
 session_id = "ses_abc"       SDK loads context:              SDK loads context:
 [history: turn 1]            [history: turns 1+2]            [history: turns 1+2+3]
                              result: "Noted."                result: "You are Ahmed,
                                                               35 years old..."
```

---

## Capturing the session_id

```python
session_id = None

async for msg in query(prompt="first message", options=ClaudeAgentOptions()):
    │
    ├── SystemMessage  ← session start (Python: ID is nested in msg.data)
    │
    └── ResultMessage  ← final answer + session_id
          session_id = msg.session_id

# Store session_id for next call
# Next call: ClaudeAgentOptions(resume=session_id)
```

---

## When Context Grows: The Sliding Window Problem

```
Turn 1:   [msg1]                           → 200 tokens
Turn 5:   [msg1][msg2][msg3][msg4][msg5]   → 2,000 tokens
Turn 20:  [all 20 messages]                → 8,000 tokens
Turn 50:  [all 50 messages]                → context limit hit!

SOLUTION: Session summarization
  After N turns, summarize old turns into one message:
  [summary_of_turns_1-40][msg41][msg42]...[msg50]
  → Context stays manageable
  → Key information preserved
```

---

## Session vs. Memory Store

```
session_id (L04)                        memory_stores (L06, Managed Agents)
──────────────────────────────          ────────────────────────────────────
Conversation history only               Structured facts persist forever
Lives for duration of session           Survives session end
Managed by SDK automatically            You write/read explicitly
Turn-by-turn messages                   Key-value or document store
Use for: conversation continuity        Use for: user preferences, facts
```
