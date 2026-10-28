# Lesson 03 - Pass 1: RECOGNITION
## Learn to SEE Logic Gates in the Wild

**Goal:** By the end of this pass, you'll instantly recognize routing patterns and understand what they do WITHOUT writing any code.

---

## The Shape Recognition Method

Logic gates have distinctive VISUAL SHAPES. Learn to recognize them by sight.

> **2026 Note:** You will see TWO routing shapes in real AI code.
> Shape 1-3 = `if/elif/else` (condition checks, thresholds)
> Shape 4 = `match/case` (routing by name/type — Python 3.10+)

### Shape 1: The Simple Branch (if/else)

```python
if condition:
    action_A
else:
    action_B
```

**Visual Pattern:**
```
if [something]:
    ← INDENT (4 spaces)
else:
    ← INDENT (4 spaces)
```

**What to recognize:**
- `if` keyword
- Colon `:`
- Indentation (everything indented belongs to that branch)
- `else:` (optional fallback)

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Confidence Gate

```python
# RAG system quality check
confidence = 0.87

if confidence > 0.90:
    print("High confidence - safe to return")
    return_to_user = True
else:
    print("Low confidence - flag for review")
    return_to_user = False
```

**RECOGNIZE THIS:**
- Line 3: `if confidence > 0.90:` ← Check condition
- Lines 4-5: Indented ← Runs when True
- Line 6: `else:` ← Fallback
- Lines 7-8: Indented ← Runs when False

**What it does:** "If score is high, return answer. Otherwise, send to human."

---

### Example 2: Intent Router

```python
# Multi-tool agent
user_intent = "search"

if user_intent == "greeting":
    response = "Hello! How can I help?"
elif user_intent == "search":
    response = search_database(query)
elif user_intent == "calculate":
    response = calculate(expression)
else:
    response = "I don't understand"
```

**RECOGNIZE THIS:**
- `if` ← First check
- `elif` ← "Else if" - additional checks
- `elif` ← Another check
- `else` ← Final fallback if nothing matched

**What it does:** "Check intent in order. Use first match. Fallback if none match."

**Visual Pattern:**
```
if choice == "A":
    do_A
elif choice == "B":
    do_B
elif choice == "C":
    do_C
else:
    do_default
```

---

### Example 3: Toxicity Guard

```python
# Content moderation
toxicity_score = 0.25
MAX_TOXICITY = 0.20

if toxicity_score > MAX_TOXICITY:
    print("BLOCKED - Toxic content")
    response = "I cannot respond to that."
else:
    print("SAFE - Processing")
    response = process_query(user_input)
```

**RECOGNIZE THIS:**
- Compare score to threshold
- Block if over limit
- Process if safe

**What it does:** "Safety check before processing user input."

---

### Example 4: Source Validation

```python
# RAG source trust check
source = "internal_kb"

if source == "internal_kb":
    trust_level = "high"
elif source == "wikipedia":
    trust_level = "medium"
else:
    trust_level = "low"
```

**RECOGNIZE THIS:**
- Multiple levels of trust
- Different actions based on source
- Fallback for unknown sources

**What it does:** "Categorize source by trust level."

---

### Example 5: Multi-Condition Gate (AND logic)

```python
# Combined checks
score = 0.92
source = "internal_kb"

if score > 0.90 and source == "internal_kb":
    print("High confidence AND trusted source")
    proceed = True
else:
    print("Either low confidence OR untrusted source")
    proceed = False
```

**RECOGNIZE THIS:**
- `and` ← BOTH conditions must be True
- Two checks combined with `and`
- Only proceeds if BOTH pass

**What it does:** "Only proceed if confident AND from trusted source."

---

### Example 6: Multi-Condition Gate (OR logic)

```python
# Flexible approval
score = 0.88
source = "internal_kb"

if score > 0.95 or source == "internal_kb":
    print("Either very confident OR from trusted source")
    approved = True
else:
    approved = False
```

**RECOGNIZE THIS:**
- `or` ← At least ONE condition must be True
- Approves if either condition passes

**What it does:** "Approve if EITHER very confident OR trusted source."

---

### Example 7: Nested Logic (Gate Inside Gate)

```python
# Two-level check
if source_is_trusted:
    if confidence > 0.90:
        action = "return_directly"
    else:
        action = "add_disclaimer"
else:
    action = "reject"
```

**RECOGNIZE THIS:**
- Outer `if` ← First level
- Inner `if` ← Second level (only checked if first passes)
- TWO levels of indentation

**Visual Pattern:**
```
if outer_condition:
    ← INDENT LEVEL 1
    if inner_condition:
        ← INDENT LEVEL 2
    else:
        ← INDENT LEVEL 2
else:
    ← INDENT LEVEL 1
```

**What it does:** "First check source. If trusted, then check confidence. If not trusted, reject immediately."

---

## Comparison Operators (The Switches)

RECOGNIZE these symbols:

| Symbol | Meaning | Example |
|:-------|:--------|:--------|
| `==` | Equal to | `if intent == "search"` |
| `!=` | Not equal to | `if status != "error"` |
| `>` | Greater than | `if score > 0.90` |
| `<` | Less than | `if cost < 1.00` |
| `>=` | Greater/equal | `if confidence >= 0.85` |
| `<=` | Less/equal | `if toxicity <= 0.20` |

### Recognition Practice: What do these check?

```python
if confidence == 1.0:        # Exactly 1.0?
if tokens > 1000:            # More than 1000?
if cost < 0.10:              # Less than $0.10?
if source != "unknown":      # Not unknown?
if score >= 0.75:            # 0.75 or higher?
```

---

## The Indentation Rule (CRITICAL!)

**RECOGNIZE ownership by indentation:**

```python
if score > 0.8:
    print("Pass")         # ← Belongs to if (indented)
    print("Approved")     # ← Belongs to if (indented)
print("Done")             # ← NOT indented, always runs
```

**Visual Guide:**
```
if condition:
    ← 4 SPACES = belongs to if
    ← 4 SPACES = belongs to if
← NO INDENT = doesn't belong to if
```

---

## Recognition Exercise: Read These Code Blocks

### Block 1
```python
rating = 4.5

if rating >= 4.0:
    quality = "excellent"
else:
    quality = "needs_improvement"
```

**Questions:**
1. What condition is checked? → `rating >= 4.0`
2. What happens if True? → Sets quality to "excellent"
3. What happens if False? → Sets quality to "needs_improvement"

---

### Block 2
```python
model_type = "claude-opus-5-5"

if model_type == "claude-opus-5-5":
    cost_per_token = 0.015
elif model_type == "claude-sonnet-5-5":
    cost_per_token = 0.003
else:
    cost_per_token = 0.001
```

**Questions:**
1. How many branches? → 3 (if, elif, else)
2. What sets cost to 0.003? → model_type == "claude-sonnet-5-5"
3. What's the fallback cost? → 0.001

---

### Block 3
```python
toxicity = 0.15
confidence = 0.92

if toxicity < 0.20 and confidence > 0.90:
    status = "approved"
else:
    status = "review_needed"
```

**Questions:**
1. How many conditions? → 2 (toxicity AND confidence)
2. What operator combines them? → `and`
3. Both must be True for approval? → Yes

---

## Pattern Recognition Summary

When you see code, ask:

### 1. What shape is it?
- Simple branch (if/else)?
- Multi-branch (if/elif/else)?
- Nested (if inside if)?

### 2. What's being checked?
- Number comparison (`score > 0.90`)?
- Text match (`intent == "search"`)?
- Multiple conditions (`and`/`or`)?

### 3. What's the outcome?
- Route to different tools?
- Quality gate (pass/fail)?
- Safety check (allow/block)?

---

## Common AI Patterns (Recognition Cheat Sheet)

### Pattern: Confidence Threshold
```python
if confidence > threshold:
    proceed()
else:
    review()
```
**Recognize:** Quality gate for AI outputs

---

### Pattern: Intent Router
```python
if intent == "A":
    tool_A()
elif intent == "B":
    tool_B()
else:
    default()
```
**Recognize:** Multi-tool agent routing

---

### Pattern: Safety Guard
```python
if is_safe and is_authorized:
    process()
else:
    reject()
```
**Recognize:** Security/moderation check

---

### Pattern: Fallback Chain
```python
if primary_available:
    use_primary()
elif backup_available:
    use_backup()
else:
    use_default()
```
**Recognize:** Redundancy/failover logic

---

## Final Recognition Test

Look at this real AI code and identify the pattern:

```python
# Mystery code from production RAG system
retrieved_docs = search_vector_db(query)

if len(retrieved_docs) == 0:
    response = "I don't have information on that topic."
elif retrieved_docs[0]["score"] < 0.70:
    response = "I found some information, but I'm not confident. Would you like me to show what I found?"
else:
    context = combine_docs(retrieved_docs)
    response = generate_answer(query, context)
```

**RECOGNIZE:**
1. Shape? → if/elif/else (3 branches)
2. What's checked first? → No documents found
3. What's checked second? → Low confidence score
4. What happens in else? → Normal RAG flow
5. Purpose? → Handle edge cases before normal processing

**This is:** Error handling + Quality gate + Normal flow

---

---

## Shape 4: match/case — The Modern Router (Python 3.10+, 2026 standard)

```python
match subject:
    case "value_A":
        action_A
    case "value_B":
        action_B
    case _:             # ← _ is the catch-all (same job as else)
        action_default
```

**Visual Pattern:**
```
match [variable]:
    case "[option1]":
        ← INDENT (4 spaces)
    case "[option2]":
        ← INDENT (4 spaces)
    case _:
        ← INDENT (4 spaces)
```

**What to recognize:**
- `match` keyword followed by a variable name
- `case` lines (each is one routing option)
- `case _:` at the bottom (the catch-all)
- All case bodies are indented

---

### Example 8: Stop Reason Router (Real Anthropic API Pattern)

```python
# Inside the agent tool loop
match response.stop_reason:
    case "end_turn":
        return response.content[0].text
    case "tool_use":
        execute_tools(response)
    case "max_tokens":
        handle_truncation()
    case _:
        handle_unexpected()
```

**RECOGNIZE THIS:**
- `match response.stop_reason` ← the subject being routed
- Each `case` handles one specific stop reason by NAME
- `case _:` ← catch-all for anything else

**What it does:** "Look at what the LLM decided to do. Route to the right handler."

---

### Example 9: Intent Router (match/case version of Example 2)

```python
# Modern multi-tool agent — same intent as Example 2, different syntax
match user_intent:
    case "greeting":
        response = "Hello! How can I help?"
    case "search":
        response = search_database(query)
    case "calculate":
        response = calculate(expression)
    case _:
        response = "I don't understand"
```

**RECOGNIZE THIS — compare to Example 2:**
- Same routing logic, cleaner visual shape
- No `elif` chains — each option is a `case` line
- `case _:` replaces `else:`

**Side by side:**
```
if/elif (still valid)          match/case (2026 preferred for routing)
──────────────────             ─────────────────────────────────────
if intent == "search":         match intent:
    search()                       case "search":
elif intent == "calc":                 search()
    calculate()                    case "calc":
else:                                  calculate()
    default()                      case _:
                                       default()
```

---

### Pattern Recognition Summary — Updated for 2026

When you see code, ask:

**1. What shape is it?**
- Simple branch (`if/else`) — threshold check
- Multi-branch (`if/elif/else`) — multiple conditions
- Nested (`if` inside `if`) — two-level check
- **Match/case** — routing by name/type/status (2026 pattern)

**2. Which tool is it using?**
- Checking a SCORE or THRESHOLD → `if/elif/else`
- Routing by a SPECIFIC NAME or TYPE → `match/case`

**3. What's the outcome?**
- Route to different tools?
- Quality gate (pass/fail)?
- Safety check (allow/block)?

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** if/else shapes by sight
✓ **Recognize** match/case shapes by sight (2026 addition)
✓ **Identify** what conditions are being checked
✓ **Understand** what different branches do
✓ **Spot** common AI patterns (routing, gates, guards)
✓ **Know when** to expect if/elif vs match/case in real code

**Next:**
- **Pass C (Visual):** See logic gates as flowcharts (including match/case)
- **Pass 3 (Templates):** Copy and modify routing patterns

**Remember:** You're not memorizing. You're training your eyes to SEE patterns.

---

## Pro Tip: The 3-Second Rule

When you see unfamiliar code with `if/else` or `match/case`:
1. **Second 1:** Identify the shape (if/elif? match/case? nested?)
2. **Second 2:** Read what's being compared or routed
3. **Second 3:** Understand the purpose (routing? safety? quality?)

That's it. You don't need to understand every detail. Just recognize the pattern.
