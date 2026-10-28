"""
═══════════════════════════════════════════════════════════════════
LESSON 03 CHEATSHEET: Logic Gates & Routing
═══════════════════════════════════════════════════════════════════

Quick reference for if/else AND match/case patterns in AI systems.
Keep this open while reading code!

Python 3.13 / 2026 context:
  if/elif/else  → condition checks (scores, thresholds, True/False)
  match/case    → routing by name/type/status (Python 3.10+)

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. BASIC IF/ELSE (Two options)
# ═══════════════════════════════════════════════════════════

if condition:
    # Runs when True
    action_A
else:
    # Runs when False
    action_B

# Example:
confidence = 0.92
if confidence > 0.90:
    return_answer()
else:
    escalate_to_human()


# ═══════════════════════════════════════════════════════════
# 2. IF/ELIF/ELSE (Multiple options)
# ═══════════════════════════════════════════════════════════

if condition1:
    action_A
elif condition2:
    action_B
elif condition3:
    action_C
else:
    action_default

# Example:
intent = "search"
if intent == "greeting":
    greet_user()
elif intent == "search":
    search_database()
elif intent == "calculate":
    do_math()
else:
    show_help()


# ═══════════════════════════════════════════════════════════
# 3. COMPARISON OPERATORS
# ═══════════════════════════════════════════════════════════

# Equal to
if score == 1.0:
    perfect()

# Not equal to
if status != "error":
    proceed()

# Greater than
if score > 0.90:
    high_quality()

# Less than
if cost < 1.00:
    affordable()

# Greater than or equal
if confidence >= 0.85:
    acceptable()

# Less than or equal
if toxicity <= 0.20:
    safe()


# ═══════════════════════════════════════════════════════════
# 4. AND LOGIC (All must be True)
# ═══════════════════════════════════════════════════════════

if condition1 and condition2:
    # Runs only if BOTH are True
    proceed()

# Example:
if score > 0.90 and source == "trusted":
    approve()
else:
    reject()


# ═══════════════════════════════════════════════════════════
# 5. OR LOGIC (At least one must be True)
# ═══════════════════════════════════════════════════════════

if condition1 or condition2:
    # Runs if EITHER is True
    proceed()

# Example:
if score > 0.95 or source == "trusted":
    approve()
else:
    reject()


# ═══════════════════════════════════════════════════════════
# 6. NOT LOGIC (Reverse the condition)
# ═══════════════════════════════════════════════════════════

if not condition:
    # Runs when condition is False
    handle_false_case()

# Example:
if not user_is_authorized:
    block_access()


# ═══════════════════════════════════════════════════════════
# 7. NESTED LOGIC (If inside if)
# ═══════════════════════════════════════════════════════════

if outer_condition:
    if inner_condition:
        both_true()
    else:
        outer_true_inner_false()
else:
    outer_false()

# Example:
if source_is_trusted:
    if confidence > 0.90:
        return_directly()
    else:
        add_disclaimer()
else:
    reject()


# ═══════════════════════════════════════════════════════════
# 8. MEMBERSHIP CHECK (in operator)
# ═══════════════════════════════════════════════════════════

# Check if item is in list
trusted_sources = ["internal_kb", "verified_api"]
if source in trusted_sources:
    proceed()

# Check if substring in string
if "weather" in user_query:
    call_weather_api()


# ═══════════════════════════════════════════════════════════
# 9. COMMON AI PATTERNS (if/elif/else)
# ═══════════════════════════════════════════════════════════

# Pattern: Confidence Threshold (use if/elif — it's a score check)
if confidence >= THRESHOLD:
    return_to_user()
else:
    escalate_to_human()

# Pattern: Safety Guard (use if/elif — it's a threshold check)
if toxicity_score > MAX_TOXICITY:
    block()
else:
    process()

# Pattern: Fallback Chain (use if/elif — checking availability)
if primary_available:
    use_primary()
elif backup_available:
    use_backup()
else:
    use_default()


# ═══════════════════════════════════════════════════════════
# 9B. MATCH/CASE — 2026 ROUTING PATTERN (Python 3.10+)
# ═══════════════════════════════════════════════════════════

# Pattern: Intent Routing (use match/case — routing by NAME)
match intent:
    case "search":
        search_tool()
    case "calculate":
        calculator_tool()
    case "summarize":
        summarizer_tool()
    case _:              # ← _ is the catch-all (like else)
        default_llm()

# Pattern: Stop Reason Routing (real Anthropic API pattern)
match response.stop_reason:
    case "end_turn":
        return response.content[0].text
    case "tool_use":
        execute_tools(response)
    case "max_tokens":
        handle_truncation()
    case _:
        handle_unexpected()

# Pattern: Source Trust Level (use match/case — routing by NAME)
match source:
    case "internal_kb":
        trust_level = "high"
    case "wikipedia":
        trust_level = "medium"
    case _:
        trust_level = "low"


# ═══════════════════════════════════════════════════════════
# 10. INDENTATION RULES
# ═══════════════════════════════════════════════════════════

# ✓ CORRECT:
if condition:
    action1()  # 4 spaces
    action2()  # 4 spaces
done()         # No indent - always runs

# ✗ WRONG (shown as comments — actual code would raise IndentationError):
# if condition:
# action1()      ← no indent = ERROR

# ✗ WRONG:
# if condition:
#     action1()  ← 4 spaces
#      action2() ← 5 spaces = INCONSISTENT, ERROR


# ═══════════════════════════════════════════════════════════
# 11. SHORTHAND PATTERNS
# ═══════════════════════════════════════════════════════════

# Single-line if (use sparingly)
if condition: action()

# Ternary operator (conditional expression)
result = value_if_true if condition else value_if_false

# Example:
status = "approved" if score > 0.90 else "review"


# ═══════════════════════════════════════════════════════════
# 12. TRUTHINESS (What counts as True/False)
# ═══════════════════════════════════════════════════════════

# False values:
if False: pass          # Boolean False
if None: pass           # None
if 0: pass              # Zero
if "": pass             # Empty string
if []: pass             # Empty list
if {}: pass             # Empty dict

# True values (everything else):
if True: pass           # Boolean True
if 1: pass              # Non-zero numbers
if "text": pass         # Non-empty strings
if [1, 2]: pass         # Non-empty lists


# ═══════════════════════════════════════════════════════════
# 13. QUICK DECISION TREE
# ═══════════════════════════════════════════════════════════

"""
Need to check:
├─ One condition? → Use if/else
├─ Multiple options? → Use if/elif/else
├─ Routing by name/type/status? → Use match/case (2026 standard)
├─ All must be true? → Use 'and'
├─ At least one true? → Use 'or'
└─ Depends on previous check? → Use nested if

match/case rule:
├─ Checking WHAT something IS → match/case
└─ Checking if something PASSES A TEST → if/elif/else
"""


# ═══════════════════════════════════════════════════════════
# 14. COMMON MISTAKES TO AVOID
# ═══════════════════════════════════════════════════════════

# ✗ WRONG: Using = instead of ==  (shown as comment — would raise SyntaxError)
# if score = 0.90:   ← assignment, not comparison!

# ✓ CORRECT:
if score == 0.90:  # Comparison
    pass

# ✗ WRONG: Missing colon  (shown as comment — would raise SyntaxError)
# if condition
#     pass

# ✓ CORRECT:
if condition:
    pass

# ✗ WRONG: Inconsistent indentation  (shown as comment — would raise IndentationError)
# if condition:
#     action1()
#         action2()  ← too much indent, ERROR

# ✓ CORRECT:
if condition:
    action1()
    action2()


# ═══════════════════════════════════════════════════════════
# 15. DEBUGGING TIPS
# ═══════════════════════════════════════════════════════════

# Print to see which branch executes
if confidence > 0.90:
    print("HIGH CONFIDENCE BRANCH")  # Add this
    return_answer()
else:
    print("LOW CONFIDENCE BRANCH")  # And this
    escalate()

# Check your condition value
print(f"Confidence: {confidence}")  # See actual value
if confidence > 0.90:
    pass


# ═══════════════════════════════════════════════════════════
# 16. TEMPLATE QUICK LINKS
# ═══════════════════════════════════════════════════════════

"""
Available templates in this folder:
- template_confidence_threshold.py    → Quality gates
- template_intent_routing.py          → Multi-tool routing
- template_safety_guards.py           → Content moderation
- template_source_validation.py       → Trust levels
- template_fallback_chains.py         → Redundancy logic
"""


# ═══════════════════════════════════════════════════════════
# 17. WHEN TO USE WHAT
# ═══════════════════════════════════════════════════════════

"""
Use if/elif/else when:
✓ Quality checking    → if confidence >= 0.85:
✓ Threshold filtering → if toxicity > MAX:
✓ Boolean check       → if result is None:
✓ Availability check  → if primary_available:
✓ Error handling      → if status == "error":

Use match/case when (Python 3.10+):
✓ Intent routing      → match intent: case "search":
✓ Stop reason routing → match stop_reason: case "tool_use":
✓ Source trust        → match source: case "internal_kb":
✓ Status codes        → match status_code: case 200:
✓ Tool dispatch       → match tool_name: case "calculator":

Don't use either for:
✗ Processing every item in a list → Use loops (L04)
✗ Defining reusable logic         → Use functions (L05)
✗ Complex state management        → Use classes (L06)
"""


# ═══════════════════════════════════════════════════════════
# 18. BEST PRACTICE PATTERNS — What breaks without these
# ═══════════════════════════════════════════════════════════

# ── A. match/case ALWAYS needs case _: ──────────────────────────────────────
# BAD — silently ignores new stop_reason values added in future API updates
match stop_reason:
    case "end_turn":  return response.content[0].text
    case "tool_use":  execute_tools(response)
# ← BUG: if stop_reason = "max_tokens", NOTHING happens — silent failure

# GOOD — case _: surfaces unexpected values immediately
match stop_reason:
    case "end_turn":  return response.content[0].text
    case "tool_use":  execute_tools(response)
    case _:           raise ValueError(f"Unexpected stop_reason: {stop_reason}")


# ── B. Guard clauses over nested if/elif ────────────────────────────────────
# BAD — deep nesting, hard to read
def route(intent: str, query: str) -> str:
    if intent:
        if query:
            if intent == "search":
                return search(query)
        else:
            return "empty query"
    return "no intent"

# GOOD — exit early, keep code flat
def route(intent: str, query: str) -> str:
    if not intent:       return "no intent"
    if not query:        return "empty query"
    if intent == "search": return search(query)
    return "unknown intent"


# ── C. Dual-threshold: accept / low-confidence / reject ─────────────────────
# BAD — only one threshold, no nuance
if confidence >= 0.85:
    return answer   # else: silently returns None

# GOOD — three zones, all paths explicit
if confidence >= 0.85:
    return answer
elif confidence >= 0.60:
    return f"{answer} ⚠ low confidence — please verify"
else:
    return None   # caller handles rejection explicitly


# ═══════════════════════════════════════════════════════════
# END OF CHEATSHEET
# ═══════════════════════════════════════════════════════════

print("Keep this cheatsheet open while coding!")
print("Copy patterns as needed - don't memorize!")
