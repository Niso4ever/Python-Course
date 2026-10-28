# Lesson 03: Logic Gates & Routing
## The Railroad Switch Theory

> **2026 Note:** Two routing tools in modern AI code:
> - `if/elif/else` — condition checks (scores, thresholds, True/False)
> - `match/case` — routing by name/type/status (Python 3.10+, now standard)
> Both are used daily. Neither replaced the other. They serve different jobs.

Architect, you now know how to store data (L01 labels, L02 lists). Now you need to **route** based on that data.

In AI systems, different inputs need different handling:
- High confidence score → Return answer directly
- Low confidence score → Ask for human review
- Toxic content → Block immediately
- Valid query → Process normally

This is where **Logic Gates** come in — `if/else` and `match/case` are the railroad switches that route your data.

---

## 1. The Basic Switch (if/else)

Think of your code as train tracks. Logic gates flip the tracks based on conditions.

```python
confidence_score = 0.92

if confidence_score > 0.90:
    print("High confidence - safe to return")
else:
    print("Low confidence - flag for review")

# Output: High confidence - safe to return
```

| Symbol | Role |
|:-------|:-----|
| `if` | "Check this condition" |
| `>` | Greater than (comparison operator) |
| `:` | "Everything indented below belongs to this branch" |
| `else:` | "If condition is False, do this instead" |

---

## 2. The Critical Rule: Indentation

**Python uses whitespace (indentation) to show ownership.**

```python
# CORRECT ✓
if score > 0.8:
    print("Pass")      # Indented - belongs to if
    print("Approved")  # Indented - belongs to if
print("Done")          # Not indented - always runs

# WRONG ✗
if score > 0.8:
print("Pass")  # No indent - Python error!
```

**Rule:** Use **4 spaces** (or 1 Tab) to indent. Everything indented under `if` only runs when condition is True.

---

## 3. Multiple Branches (if/elif/else)

Route to different destinations based on multiple conditions:

```python
intent = "search"

if intent == "greeting":
    print("Welcome, Architect!")
elif intent == "search":
    print("Searching knowledge base...")
elif intent == "calculate":
    print("Running calculation...")
else:
    print("Unknown intent - defaulting to search")

# Output: Searching knowledge base...
```

**Pattern Recognition:**
- `if` - First check
- `elif` - "Else if" - additional checks
- `else` - Fallback if nothing matched

---

## 4. Comparison Operators (The Switches)

```python
score = 0.85

# Equal to
if score == 0.85:
    print("Exact match")

# Greater than
if score > 0.80:
    print("Above threshold")

# Less than
if score < 0.90:
    print("Below threshold")

# Greater than or equal
if score >= 0.85:
    print("At or above threshold")

# Not equal
if score != 1.0:
    print("Not perfect")
```

| Operator | Meaning |
|:---------|:--------|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

---

## 5. Real-World AI Examples

### Example 1: Confidence Threshold
```python
# RAG system - decide if answer is good enough
confidence = 0.87
THRESHOLD = 0.90

if confidence >= THRESHOLD:
    return_to_user = True
    print("High confidence - returning answer")
else:
    return_to_user = False
    print("Low confidence - escalating to human")
```

### Example 2: Toxicity Guard
```python
# Content moderation
toxicity_score = 0.15  # 0 = safe, 1 = toxic
MAX_TOXICITY = 0.20

if toxicity_score > MAX_TOXICITY:
    print("BLOCKED - Toxic content detected")
    response = "I cannot respond to that request."
else:
    print("SAFE - Processing request")
    response = process_query(user_input)
```

### Example 3: Intent Routing
```python
# Route to different agent tools
user_intent = "weather_query"

if user_intent == "greeting":
    response = "Hello! How can I help?"
elif user_intent == "weather_query":
    response = get_weather(location)
elif user_intent == "calculation":
    response = calculate(expression)
elif user_intent == "search":
    response = search_database(query)
else:
    response = "I don't understand. Can you rephrase?"
```

### Example 4: Source Validation
```python
# RAG - check if sources are trusted
source = "internal_kb"

if source == "internal_kb":
    trust_level = "high"
    print("Trusted source - using directly")
elif source == "wikipedia":
    trust_level = "medium"
    print("Public source - adding disclaimer")
else:
    trust_level = "low"
    print("Unknown source - requiring verification")
```

---

## 6. Combining Conditions (and/or)

```python
# Multiple conditions
score = 0.92
source = "internal_kb"

# AND - both must be true
if score > 0.90 and source == "internal_kb":
    print("High confidence AND trusted source")

# OR - at least one must be true
if score > 0.95 or source == "internal_kb":
    print("Either very confident OR from trusted source")

# Complex logic
if score > 0.90 and (source == "internal_kb" or source == "verified_api"):
    print("High confidence with trusted source")
```

| Operator | Meaning |
|:---------|:--------|
| `and` | Both conditions must be True |
| `or` | At least one condition must be True |
| `not` | Reverse the condition |

---

## 7. Pattern Recognition Guide

**When you see:**
```python
if condition:
    # indented code
```
**Translation:** "If condition is True, run the indented code. Otherwise, skip it."

**When you see:**
```python
if condition:
    # branch A
else:
    # branch B
```
**Translation:** "Choose branch A if True, branch B if False. Exactly one runs."

**When you see:**
```python
if condition1:
    # branch A
elif condition2:
    # branch B
else:
    # branch C
```
**Translation:** "Check conditions in order. Run first matching branch. Else runs if none match."

**When you see (2026 pattern):**
```python
match variable:
    case "value_A":
        # branch A
    case "value_B":
        # branch B
    case _:
        # default (catch-all, same as else)
```
**Translation:** "Route by the exact value of `variable`. Jump directly to the matching case."
**Use when:** routing by name, type, or status — NOT for score/threshold comparisons.

---

## 8. Common AI Routing Patterns

### Pattern 1: Quality Gate (use if/elif — it's a score check)
```python
if quality_score > threshold:
    proceed = True
else:
    proceed = False
```

### Pattern 2: Fallback Chain (use if/elif — checking availability)
```python
if primary_source_available:
    data = fetch_from_primary()
elif backup_source_available:
    data = fetch_from_backup()
else:
    data = use_default()
```

### Pattern 3: Intent Routing — if/elif style (classic)
```python
if intent == "search":
    search_tool()
elif intent == "calculate":
    calculator_tool()
else:
    default_llm()
```

### Pattern 3B: Intent Routing — match/case style (2026 preferred for routing by name)
```python
match intent:
    case "search":
        search_tool()
    case "calculate":
        calculator_tool()
    case _:
        default_llm()
```

### Pattern 4: Stop Reason Routing (use match/case — real Anthropic API pattern)
```python
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

### Pattern 5: Safety Check (use if/elif — threshold and boolean checks)
```python
if content_is_safe and user_is_authorized and rate_limit_ok:
    process_request()
else:
    reject_request()
```

---

## 9. The Nested Switch (if inside if)

```python
# RAG system with multiple checks
if source_is_trusted:
    if confidence > 0.90:
        return answer_directly
    else:
        return answer_with_disclaimer
else:
    return "Cannot verify this information"
```

**Indentation shows ownership:**
- Outer `if` - first level indent
- Inner `if` - second level indent
- Inner `else` - second level indent

---

## 10. Templates You Can Use

See this lesson folder ([./](./)) for ready-to-use routing patterns: `template_confidence_threshold.py`, `template_fallback_chains.py`, `template_intent_routing.py`, `template_safety_guards.py`, `template_source_validation.py`.

**Your workflow:**
1. Identify your routing need (confidence check, intent routing, safety guard)
2. Copy the matching template
3. Modify the conditions and actions
4. Use in your AI system

---

## 11. Key Takeaways

✓ **Logic gates route data** based on conditions
✓ **Indentation shows ownership** — 4 spaces = 1 level
✓ **Comparison operators** create conditions (`==`, `>`, `<`, etc.)
✓ **if/elif/else** — for condition/threshold checks (scores, True/False)
✓ **match/case** — for routing by name/type/status (Python 3.10+, 2026 standard)
✓ **and/or** combine multiple conditions

**Decision rule:**
- Score or threshold check → `if/elif/else`
- Routing by a specific name or type → `match/case`

**Most common AI use:**
- Confidence thresholds → `if/elif/else`
- Intent routing → `match/case` (or `if/elif`)
- Stop reason routing → `match/case`
- Safety guards → `if/elif/else`
- Source validation → `match/case` (routing by name)

---

## 12. Next Steps

**Immediate:**
1. Check the `template_*.py` files in this lesson folder ([./](./))
2. Recognize `if/else` in real AI code
3. Understand: It's just routing based on data

**Coming up:**
- **L04:** Loops — Process entire collections
- **L05:** Functions — Package logic into reusable tools

---

**Remember:** You're not memorizing syntax. You're recognizing: "Oh, this is routing based on confidence score" or "This is intent classification." The template handles the rest.
