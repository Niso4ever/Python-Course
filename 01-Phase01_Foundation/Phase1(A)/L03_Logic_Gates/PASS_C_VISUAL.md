# Lesson 03 - Pass C: VISUAL PATTERNS
## See Logic Gates as Flowcharts

**Goal:** Understand routing logic through visual diagrams, not just code.

---

## Visual 1: Simple Branch (if/else)

### Code:
```python
if confidence > 0.90:
    return_answer()
else:
    escalate_to_human()
```

### Visual Flowchart:
```
                    START
                      |
                      ↓
            ┌─────────────────┐
            │ Check:          │
            │ confidence > 90?│
            └─────────────────┘
                 /      \
              YES        NO
              /            \
             ↓              ↓
    ┌──────────────┐   ┌──────────────┐
    │ Return Answer│   │  Escalate to │
    │              │   │    Human     │
    └──────────────┘   └──────────────┘
             \              /
              \            /
               ↓          ↓
                   END
```

**Pattern:** Diamond = Decision, Rectangle = Action

---

## Visual 2: Multi-Branch (if/elif/else)

### Code:
```python
if intent == "greeting":
    greet_user()
elif intent == "search":
    search_database()
elif intent == "calculate":
    do_math()
else:
    show_help()
```

### Visual Flowchart:
```
                    START
                      |
                      ↓
            ┌─────────────────┐
            │ intent ==       │
            │ "greeting"?     │
            └─────────────────┘
                 /      \
              YES        NO
              /            \
             ↓              ↓
    ┌──────────────┐  ┌─────────────────┐
    │ Greet User   │  │ intent ==       │
    │              │  │ "search"?       │
    └──────────────┘  └─────────────────┘
             |             /      \
             |          YES        NO
             |          /            \
             |         ↓              ↓
             |  ┌──────────────┐  ┌─────────────────┐
             |  │Search DB     │  │ intent ==       │
             |  │              │  │ "calculate"?    │
             |  └──────────────┘  └─────────────────┘
             |         |             /      \
             |         |          YES        NO
             |         |          /            \
             |         |         ↓              ↓
             |         |  ┌──────────────┐  ┌──────────────┐
             |         |  │ Do Math      │  │ Show Help    │
             |         |  │              │  │ (default)    │
             |         |  └──────────────┘  └──────────────┘
             |         |         |              |
             └─────────┴─────────┴──────────────┘
                              |
                              ↓
                            END
```

**Pattern:** Waterfall of checks, first match wins

---

## Visual 3: AND Logic (Both Must Be True)

### Code:
```python
if score > 0.90 and source == "trusted":
    approve()
else:
    reject()
```

### Visual Flowchart:
```
                    START
                      |
                      ↓
            ┌─────────────────┐
            │  score > 0.90?  │
            └─────────────────┘
                 /      \
              YES        NO ──────┐
              /                   │
             ↓                    │
    ┌─────────────────┐           │
    │ source ==       │           │
    │ "trusted"?      │           │
    └─────────────────┘           │
         /      \                 │
      YES        NO               │
      /            \              │
     ↓              ↓             │
┌──────────┐   ┌────────────────┐│
│ APPROVE  │   │    REJECT      ││
│          │   │                ││
└──────────┘   └────────────────┘│
     |              |             |
     └──────────────┴─────────────┘
                    |
                    ↓
                  END
```

**Key Insight:** With AND, if FIRST check fails, skip second check → reject

---

## Visual 4: OR Logic (At Least One Must Be True)

### Code:
```python
if score > 0.95 or source == "trusted":
    approve()
else:
    reject()
```

### Visual Flowchart:
```
                    START
                      |
                      ↓
            ┌─────────────────┐
            │  score > 0.95?  │
            └─────────────────┘
                 /      \
              YES        NO
              /            \
             ↓              ↓
    ┌──────────────┐   ┌─────────────────┐
    │   APPROVE    │   │ source ==       │
    │              │   │ "trusted"?      │
    └──────────────┘   └─────────────────┘
             |              /      \
             |           YES        NO
             |           /            \
             |          ↓              ↓
             |  ┌──────────────┐  ┌──────────┐
             |  │   APPROVE    │  │  REJECT  │
             |  │              │  │          │
             |  └──────────────┘  └──────────┘
             |          |              |
             └──────────┴──────────────┘
                        |
                        ↓
                      END
```

**Key Insight:** With OR, if FIRST check passes → approve (skip second check)

---

## Visual 5: Nested Logic (Decision Inside Decision)

### Code:
```python
if source_is_trusted:
    if confidence > 0.90:
        return_directly()
    else:
        add_disclaimer()
else:
    reject()
```

### Visual Flowchart:
```
                    START
                      |
                      ↓
            ┌─────────────────┐
            │  Source         │
            │  Trusted?       │
            └─────────────────┘
                 /      \
              YES        NO
              /            \
             ↓              ↓
    ┌─────────────────┐  ┌──────────────┐
    │ Confidence      │  │   REJECT     │
    │ > 0.90?         │  │              │
    └─────────────────┘  └──────────────┘
         /      \              |
      YES        NO             |
      /            \            |
     ↓              ↓           |
┌──────────┐   ┌─────────────┐ |
│ Return   │   │    Add      │ |
│ Directly │   │ Disclaimer  │ |
└──────────┘   └─────────────┘ |
     |              |           |
     └──────────────┴───────────┘
                    |
                    ↓
                  END
```

**Pattern:** Inner decision only happens if outer passes

---

## Visual 6: Real RAG System Flow

### Code:
```python
docs = search(query)

if len(docs) == 0:
    response = "No information found"
elif docs[0]["score"] < 0.70:
    response = "Low confidence warning"
else:
    response = generate_answer(docs)
```

### Visual Flowchart:
```
                    START
                      |
                      ↓
            ┌─────────────────┐
            │  Search Vector  │
            │   Database      │
            └─────────────────┘
                      |
                      ↓
            ┌─────────────────┐
            │  Found any      │
            │  documents?     │
            └─────────────────┘
                 /      \
               NO        YES
              /            \
             ↓              ↓
    ┌──────────────┐   ┌─────────────────┐
    │ "No info     │   │  Top score      │
    │  found"      │   │  >= 0.70?       │
    └──────────────┘   └─────────────────┘
             |              /      \
             |            NO        YES
             |            /            \
             |           ↓              ↓
             |  ┌──────────────┐   ┌──────────────┐
             |  │ "Low conf    │   │  Generate    │
             |  │  warning"    │   │   Answer     │
             |  └──────────────┘   └──────────────┘
             |           |              |
             └───────────┴──────────────┘
                         |
                         ↓
                 Return Response
                         |
                         ↓
                       END
```

**Pattern:** Error handling → Quality gate → Normal flow

---

## Visual 7: Intent Router (Agent Tool Selection)

### Code:
```python
if intent == "search":
    use_search_tool()
elif intent == "weather":
    use_weather_api()
elif intent == "calculate":
    use_calculator()
else:
    use_default_llm()
```

### Visual Shape Recognition:
```
┌─────────────────────────────────────┐
│         INTENT ROUTER               │
│                                     │
│  ┌───────────┐                      │
│  │  User     │                      │
│  │  Intent   │                      │
│  └─────┬─────┘                      │
│        │                            │
│   ┌────┴────┬────────┬────────┐    │
│   │         │        │        │    │
│   ↓         ↓        ↓        ↓    │
│ search   weather  calc    other    │
│   │         │        │        │    │
│   ↓         ↓        ↓        ↓    │
│ Search   Weather  Math    Default  │
│  Tool      API    Tool      LLM    │
└─────────────────────────────────────┘
```

**Visual Pattern:** Railroad switch - one track chosen based on intent

---

## Visual 8: Safety Pipeline

### Code:
```python
if is_toxic:
    block()
elif not is_authorized:
    block()
elif rate_limit_exceeded:
    block()
else:
    process()
```

### Visual Flowchart:
```
        START
          |
          ↓
    ┌──────────┐
    │ Toxic?   │
    └──────────┘
       /    \
     YES     NO
     /         \
    ↓           ↓
 BLOCK    ┌──────────┐
          │Authorized│
          └──────────┘
             /    \
           NO      YES
           /         \
          ↓           ↓
       BLOCK    ┌──────────┐
                │Rate Limit│
                │ OK?      │
                └──────────┘
                   /    \
                 NO      YES
                 /         \
                ↓           ↓
             BLOCK       PROCESS
```

**Pattern:** Security gauntlet - must pass ALL checks

---

## Shape Comparison Chart

### Simple Branch
```
    ◇
   / \
  A   B
```
One decision, two outcomes

---

### Multi-Branch
```
    ◇
   /|\
  A B C
```
Multiple options, one chosen

---

### AND Logic
```
  ◇
  |
  ◇
 / \
A   B
```
Two checks stacked, both required

---

### OR Logic
```
    ◇
   / \
  A   ◇
     / \
    A   B
```
First pass → A, else check second

---

### Nested
```
      ◇
     / \
    ◇   B
   / \
  A   C
```
Decision tree with depth

---

## Visual Recognition Exercise

Look at this code and draw the shape in your mind:

```python
if priority == "urgent":
    route_to_human()
elif priority == "high":
    if expert_available:
        route_to_expert()
    else:
        route_to_standard()
else:
    queue_for_later()
```

**Mental Image:**
```
      Priority?
     /    |    \
 urgent high  normal
    |     |      |
  Human  ◇    Queue
        / \
    Expert Standard
```

---

## Color Coding Method (For Your Practice)

When reading code, mentally color it:

- **🔵 Blue** = Conditions (what's being checked)
- **🟢 Green** = Actions (what happens)
- **🟡 Yellow** = Keywords (if/elif/else)

```python
🟡if 🔵confidence > 0.90:
    🟢return_answer()
🟡else:
    🟢escalate_to_human()
```

---

---

## Visual: match/case — The Switch Board (Python 3.10+, 2026 standard)

### Code:
```python
match response.stop_reason:
    case "end_turn":
        return_answer()
    case "tool_use":
        execute_tools()
    case "max_tokens":
        handle_truncation()
    case _:
        handle_unexpected()
```

### Visual — The Switchboard:
```
                        START
                          │
                   ┌──────▼──────┐
                   │ stop_reason │
                   │   = what?   │
                   └──────┬──────┘
                          │
          ┌───────────────┼───────────────┬───────────────┐
          │               │               │               │
    "end_turn"       "tool_use"      "max_tokens"      anything
          │               │               │               │
          ▼               ▼               ▼               ▼
    return_answer   execute_tools  handle_truncation  handle_unexpected
```

**The Visual Difference from if/elif:**

```
if/elif — tests each condition ONE BY ONE:          match/case — goes DIRECTLY to the match:

  ┌─────────────────┐                                 ┌───────────────┐
  │ is it "end_turn"│──NO──►                          │  stop_reason  │
  └────────┬────────┘        ┌─────────────────┐      └───────┬───────┘
           │YES              │ is it "tool_use"│              │
           ▼                 └────────┬────────┘    Direct jump to the right case
      return_answer                   │YES
                                      ▼
                                 execute_tools
```

**Shape rule:**
- `if/elif` = checking conditions ONE BY ONE (slower to read, more flexible)
- `match/case` = jumping DIRECTLY to the match (faster to read, cleaner for routing)

### Visual — Side by Side Shapes:

```
if/elif shape:          match/case shape:
───────────────         ──────────────────
if x == "A":            match x:
    ...                     case "A":
elif x == "B":                  ...
    ...                     case "B":
elif x == "C":                  ...
    ...                     case "C":
else:                               ...
    ...                     case _:
                                    ...

Looks like: a staircase   Looks like: a clean list
```

---

## You've Completed Pass C!

You can now:
✓ **Visualize** if/else logic gates as flowcharts
✓ **Visualize** match/case as a switchboard (2026 addition)
✓ **See** the shape of routing logic
✓ **Understand** flow without reading every line
✓ **Recognize** patterns by visual structure — if/elif staircase vs match/case list

**Next:**
- **Pass 3 (Templates):** Copy and modify routing patterns for your AI systems

**Remember:** When you see `if/else` — picture a staircase. When you see `match/case` — picture a switchboard going directly to the right connection.

---

## Pro Tip: The Mental Flowchart

Whenever you see complex routing:
1. **Identify decision points** (diamonds in the flow)
2. **Trace one path** through to the end
3. **Understand the shape** (staircase if/elif? or switchboard match/case?)

You don't need to trace every path. Just recognize the pattern.
