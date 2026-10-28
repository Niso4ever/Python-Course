# Lesson 03 Templates: Logic Gates & Routing

These templates show common routing patterns in AI systems.

---

## What's Inside

1. **CHEATSHEET_L03.py** - Quick reference for if/else AND match/case patterns
2. **template_confidence_threshold.py** - Quality gates for RAG/LLM responses
3. **template_intent_routing.py** - Route to different tools based on user intent
4. **template_safety_guards.py** - Content moderation and safety checks
5. **template_source_validation.py** - Verify data sources before using
6. **template_fallback_chains.py** - Primary → Backup → Default logic

---

## Two Routing Tools — Know When to Use Each

### `if/elif/else` — Condition Checking (still standard, not replaced)
Use when you are **evaluating a condition** — a score, a threshold, a True/False check.

```python
# Use if/elif/else when checking a VALUE or CONDITION
if confidence >= 0.90:
    return_answer()
elif confidence >= 0.70:
    ask_for_clarification()
else:
    escalate_to_human()
```

### `match/case` — Pattern Routing (Python 3.10+, now standard in AI agents)
Use when you are **routing based on what something IS** — a tool name, an intent, a status code.

```python
# Use match/case when routing based on a SPECIFIC VALUE
match intent:
    case "search":
        use_search_tool()
    case "calculate":
        use_calculator()
    case "summarize":
        use_summarizer()
    case _:
        return_default_response()   # _ is the catch-all (like else)
```

**The rule:**
- Score/threshold check → `if/elif/else`
- Routing by name/type/status → `match/case`

---

## Real AI Agent Example — match/case for Tool Routing (2026 pattern)

```python
# Modern agent tool dispatcher
match tool_name:
    case "web_search":
        result = web_search(query)
    case "calculator":
        result = calculator(expression)
    case "read_document":
        result = read_document(filename)
    case _:
        result = f"Unknown tool: {tool_name}"
```

---

## Common Patterns

### Confidence Threshold (use if/elif)
Use when: LLM response needs quality check
```python
if confidence >= 0.90:
    return_answer()
else:
    escalate_to_human()
```

### Intent Routing (use match/case)
Use when: Different user requests need different tools
```python
match intent:
    case "search": use_search_tool()
    case "calculate": use_calculator()
    case _: use_default()
```

### Safety Guard (use if/elif — it's a threshold check)
Use when: Content needs moderation
```python
if toxicity_score > threshold:
    block_request()
else:
    process_request()
```

### Stop Reason Routing (use match/case — 2026 Anthropic API pattern)
Use when: Handling what the LLM decided to do
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

---

> **Python version note:** `match/case` requires Python 3.10+. Python 3.13 is current as of 2026.
> `if/elif/else` is still used daily — neither replaced the other. They serve different jobs.

**Remember:** You're not writing from scratch. You're recognizing the pattern, copying the template, and modifying values.
