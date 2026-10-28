# Lesson 23 — Pass C: VISUAL PATTERNS
## Decision Trees for Agentic System Design

---

## Visual 1: The "Do I Need an Agent?" Decision Tree

```
Does the task require information the LLM doesn't already know?
        │
    YES │                NO
        ▼                ▼
  Does it require    Can it be done
  current/real-time  in pure Python?
  information?           │
        │             YES│       NO
    YES │                ▼       ▼
        ▼           Use Python  Single
  USE AGENT         function    LLM call
  (with search      (no API!)
   tool)
        │
   Multi-step? Does each step depend on previous?
        │
    YES │                NO
        ▼                ▼
  USE AGENT         Use structured
  (loop needed)     output (messages.parse,
                    no loop)
```

**Examples:**
```
"What is RAG?"              → LLM knows → Single call
"Format this list"          → Pure Python → No API
"Latest AI news today"      → Real-time → Agent + search
"Extract name from text"    → Structured output → No loop
"Research and write report" → Multi-step → Agent loop
```

---

## Visual 2: How Many Agents?

```
START: one task from the user
           │
           ▼
Do all steps need the SAME tools?
           │
       YES │              NO
           ▼              ▼
   Do all steps      ← Split agents
   need the same       one per skill set
   context/persona?
           │
       YES │              NO
           ▼              ▼
   ONE agent        ← Split agents
   handles it         one per role


EXAMPLES:
"Research + summarize"     → Same tools (search) → ONE agent
"Research + write article" → Different tools → TWO agents
"Validate + analyze + format" → Maybe ONE if tools overlap
"Research + code + test"   → THREE very different skill sets → THREE agents
```

**Visual rule:**
```
All same tools + same persona → 1 agent
Different tools OR different persona → N agents
```

---

## Visual 3: Tool Selection Framework

```
For each candidate tool, ask:

1. Does the agent NEED this?
   Could it complete the task without it?
   If YES (can complete without) → REMOVE the tool

2. Is this tool CLEAR enough?
   Would the LLM know when to use this vs. other tools?
   If NO (ambiguous) → REWRITE the description

3. Is this tool SAFE?
   Could the LLM call this at the wrong time and cause damage?
   If YES (risky) → Add explicit constraints to the description

RESULT:
  Start with ALL tools you can think of
  Apply the 3 questions to each
  Keep only what survives
  Target: 3-6 tools per agent

TOO FEW:      Agent can't complete the task → add tools
JUST RIGHT:   Agent picks the right tool every time
TOO MANY:     Agent gets confused, calls wrong tool → remove tools
```

**Example:**
```
TASK: Research AI news and summarize
CANDIDATE TOOLS:          PASS?
  search_recent_news      ✓ YES — directly needed
  search_all_time         ✗ NO — redundant with above
  format_html             ✗ NO — task just needs text
  send_email              ✗ NO — not part of this task
  summarize               ✗ NO — LLM can do this natively

RESULT: 1 tool: search_recent_news
```

---

## Visual 4: Guardrail Placement

```
USER INPUT
     │
     ▼ ← GUARDRAIL 1: Input validation
  Validate:
  - Length OK?
  - Format valid?
  - No injection?
     │
  PASS │          FAIL
     │            └──► return error
     ▼
  AGENT LOOP ← GUARDRAIL 2: Loop cap (max_iterations=N)
     │
  Tool calls...
  Reasoning...
     │
     ▼ ← GUARDRAIL 3: Output quality gate
  Evaluate:
  - Answer relevant?
  - Confidence >= threshold?
  - No hallucinations?
     │
  PASS │     FAIL (retry)    FAIL (escalate)
     │            │                │
     ▼            ▼                ▼
  Return      Re-run agent    Flag for human
  answer      (max 2 retries)  review
```

**Three guardrails — three different risks:**
```
Input guardrail  → protects against: bad input crashing the agent
Loop cap         → protects against: infinite loops / runaway costs
Output gate      → protects against: wrong/low quality answers reaching the user
```

---

## Visual 5: Memory Strategy Decision

```
What memory does this system need?

Is this a one-shot question?
  YES → No memory (stateless) → messages = [{"role": "user", "content": q}]

Is this a multi-turn conversation (same session)?
  YES → Session memory → messages = history + [new_message]

Does the agent need to remember across sessions?
  YES → Persistent memory → Load from DB → inject into system/messages

Does each user need their own memory?
  YES → Per-user storage → key by user_id

MEMORY OVERHEAD grows conversation length:
  Every stored message = tokens used in every future call
  Trim history when it gets long (L05 Template 10: trim_history)
```

**Visual:**
```
STATELESS:
  [User Q] → Agent → Answer
  [User Q] → Agent → Answer  ← each call starts fresh

SESSION:
  [History + User Q1] → Agent → Answer
  [History+A1 + User Q2] → Agent → Answer  ← remembers Q1

PERSISTENT:
  DB.load(user_id) → [Past context + User Q] → Agent → Answer
                       DB.save(answer, user_id)  ← saves for next time
```

---

## Visual 6: The Architect's Checklist

```
BEFORE building any agentic system:

□ Does this need an agent, or is a single LLM call enough?
□ What is the MINIMUM set of tools needed to complete the task?
□ How many agents — can one agent handle all the steps?
□ What is the system prompt? (role + tools + constraints + output format)
□ Where are the guardrails? (input, loop cap, output)
□ What memory strategy? (stateless / session / persistent)
□ How will I know if it's working? (evaluation metric)
□ What's the max cost per call? (token budget, max_iterations)

AFTER the AI writes the code for you:

□ Does the agent have a loop when it doesn't need one?
□ Are there more than 7 tools in one agent?
□ Is the system prompt specific or vague?
□ Is there a loop cap?
□ Is there an output validation step?
□ Are you starting with a blank messages list every call (should you have history)?
```

---

## Visual 7: Scale and Complexity Map

```
COMPLEXITY ↑                        COMPLEXITY ↑

Single LLM call                     [simplest]
    ↓
Single LLM call + structured output
    ↓
One agent + one tool
    ↓
One agent + multiple tools          [most common]
    ↓
Sequential pipeline (2-3 agents)
    ↓
Router + specialists
    ↓
Parallel agents
    ↓
Swarm (dynamic spawning)
    ↓
Agent-as-tool (nested agents)       [most complex]

RULE: Start at the simplest level that solves the problem.
      Move up only when you observe specific failures.
      Each level adds cost, complexity, and debugging surface.
```

---

## You've Completed Pass C!

You can now:
✓ **Apply** the "Do I need an agent?" decision tree
✓ **Use** the tool selection framework (3 questions)
✓ **Place** guardrails at all three correct points
✓ **Choose** the right memory strategy
✓ **Run** the architect's checklist before and after building
✓ **Map** your system to the complexity scale

**Next:** Pass 3 — Thinking frameworks and design checklists you can use with AI when designing your systems.
