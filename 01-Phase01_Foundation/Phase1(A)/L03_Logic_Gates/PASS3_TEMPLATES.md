# Lesson 03 - Pass 3: TEMPLATES
## Your Copy-Paste Routing Library

**Goal:** Build your reference library of routing patterns. Copy, modify, use.

**Note (checked 2026-10-28):** 5 of the 8 templates on this page are saved as `.py` files in this folder (`template_confidence_threshold.py`, `template_fallback_chains.py`, `template_intent_routing.py`, `template_safety_guards.py`, `template_source_validation.py`). `template_multi_condition_and.py`, `template_multi_condition_or.py` and `template_nested_logic.py` exist only as the code blocks below; copy them from this page.

---

## How to Use These Templates

1. **Identify** your routing need
2. **Find** the matching template below
3. **Copy** the code
4. **Modify** the values/conditions
5. **Use** in your AI system

**You're not writing from scratch. You're customizing proven patterns.**

---

## Template Library

### Template 1: Confidence Threshold (Quality Gate)

**Use when:** LLM/RAG response needs quality check

**File:** `template_confidence_threshold.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Confidence Threshold (Quality Gate)
# Use: Check if AI response is confident enough to return
# ═══════════════════════════════════════════════════════════

# Configuration
CONFIDENCE_THRESHOLD = 0.90  # ← MODIFY: Your threshold

# Your data (from LLM/RAG system)
confidence_score = 0.87  # ← MODIFY: Actual score from your system
response = "RAG combines retrieval with generation..."  # ← Your response

# Routing logic
if confidence_score >= CONFIDENCE_THRESHOLD:
    # High confidence - safe to return
    action = "return_to_user"
    return_response = response
    flag_for_review = False
    print(f"✓ High confidence ({confidence_score}) - Returning answer")

else:
    # Low confidence - needs review
    action = "escalate_to_human"
    return_response = "Let me connect you with a human expert for this question."
    flag_for_review = True
    print(f"⚠ Low confidence ({confidence_score}) - Escalating to human")

# Result
result = {
    "action": action,
    "response": return_response,
    "original_confidence": confidence_score,
    "flagged": flag_for_review
}

print(f"\nAction taken: {result['action']}")
print(f"Response: {result['response']}")
```

**Modification Guide:**
- Change `CONFIDENCE_THRESHOLD` to your required level
- Modify `action` values to match your system
- Adjust low-confidence fallback message

---

### Template 2: Intent Routing (Multi-Tool Agent)

**Use when:** Different user intents need different tools

**File:** `template_intent_routing.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Intent Routing (Multi-Tool Agent)
# Use: Route user requests to appropriate tools
# ═══════════════════════════════════════════════════════════

# User input (from intent classifier)
user_intent = "search"  # ← MODIFY: Your intent classification
user_query = "What is RAG?"  # ← MODIFY: Actual user query

# Intent routing
if user_intent == "greeting":
    # Handle greetings
    tool_used = "greeting_handler"
    response = "Hello! How can I help you today?"

elif user_intent == "search":
    # Search knowledge base
    tool_used = "search_tool"
    # response = search_database(user_query)  # ← MODIFY: Your search function
    response = f"Searching for: {user_query}"

elif user_intent == "calculate":
    # Math/calculation requests
    tool_used = "calculator"
    # response = calculate(user_query)  # ← MODIFY: Your calculator function
    response = "Calculating..."

elif user_intent == "weather":
    # Weather queries
    tool_used = "weather_api"
    # response = get_weather(location)  # ← MODIFY: Your weather function
    response = "Fetching weather data..."

else:
    # Unknown intent - fallback
    tool_used = "default_llm"
    response = "I'm not sure I understand. Could you rephrase that?"
    print(f"⚠ Unknown intent: {user_intent}")

# Result
result = {
    "intent": user_intent,
    "tool_used": tool_used,
    "response": response,
    "query": user_query
}

print(f"\nIntent: {result['intent']}")
print(f"Tool: {result['tool_used']}")
print(f"Response: {result['response']}")
```

**Modification Guide:**
- Add/remove `elif` blocks for your specific intents
- Replace placeholder responses with actual function calls
- Customize default/fallback behavior

---

### Template 3: Safety Guards (Content Moderation)

**Use when:** Need to filter toxic/unsafe content

**File:** `template_safety_guards.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Safety Guards (Content Moderation)
# Use: Block toxic/unsafe content before processing
# ═══════════════════════════════════════════════════════════

# Configuration
MAX_TOXICITY = 0.20  # ← MODIFY: Your toxicity threshold
REQUIRE_AUTH = True   # ← MODIFY: Require authorization?

# Your data (from moderation API)
toxicity_score = 0.15      # ← MODIFY: Score from moderation system
user_is_authorized = True  # ← MODIFY: Auth status
content = "User request text..."  # ← MODIFY: Actual content

# Safety check
if toxicity_score > MAX_TOXICITY:
    # BLOCKED - Toxic content
    status = "blocked_toxic"
    response = "I cannot respond to that request."
    allow_processing = False
    reason = f"Toxicity score {toxicity_score} exceeds limit {MAX_TOXICITY}"
    print(f"🚫 BLOCKED: {reason}")

elif REQUIRE_AUTH and not user_is_authorized:
    # BLOCKED - Not authorized
    status = "blocked_unauthorized"
    response = "You need to be logged in to access this feature."
    allow_processing = False
    reason = "User not authorized"
    print(f"🚫 BLOCKED: {reason}")

else:
    # SAFE - Allow processing
    status = "approved"
    # response = process_request(content)  # ← MODIFY: Your processing function
    response = "Processing your request..."
    allow_processing = True
    reason = "Passed all safety checks"
    print(f"✓ APPROVED: {reason}")

# Result
result = {
    "status": status,
    "response": response,
    "allowed": allow_processing,
    "reason": reason,
    "toxicity_score": toxicity_score
}

print(f"\nStatus: {result['status']}")
print(f"Allowed: {result['allowed']}")
```

**Modification Guide:**
- Adjust `MAX_TOXICITY` threshold
- Add additional safety checks (rate limiting, content policy, etc.)
- Customize block messages

---

### Template 4: Source Validation (Trust Levels)

**Use when:** RAG sources need trust categorization

**File:** `template_source_validation.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Source Validation (Trust Levels)
# Use: Categorize RAG sources by trust level
# ═══════════════════════════════════════════════════════════

# Retrieved document source
source = "internal_kb"  # ← MODIFY: Your document source
document_text = "RAG combines retrieval..."  # ← MODIFY: Document content
confidence_score = 0.88  # ← MODIFY: Retrieval score

# Source validation
if source == "internal_kb":
    # Trusted internal source
    trust_level = "high"
    use_directly = True
    add_disclaimer = False
    citation_format = f"Source: Internal Knowledge Base"
    print(f"✓ High trust: {source}")

elif source == "verified_api":
    # Verified external API
    trust_level = "high"
    use_directly = True
    add_disclaimer = False
    citation_format = f"Source: Verified API"
    print(f"✓ High trust: {source}")

elif source == "wikipedia":
    # Public source - medium trust
    trust_level = "medium"
    use_directly = True
    add_disclaimer = True
    citation_format = f"Source: Wikipedia (public source)"
    print(f"⚠ Medium trust: {source} - Adding disclaimer")

elif source == "web_search":
    # Web search - lower trust
    trust_level = "low"
    use_directly = False
    add_disclaimer = True
    citation_format = f"Source: Web Search (unverified)"
    print(f"⚠ Low trust: {source} - Requiring verification")

else:
    # Unknown source - minimal trust
    trust_level = "unknown"
    use_directly = False
    add_disclaimer = True
    citation_format = f"Source: Unknown - Manual verification required"
    print(f"🚫 Unknown source: {source}")

# Build response based on trust
if use_directly:
    response = document_text
    if add_disclaimer:
        response += f"\n\nNote: {citation_format}"
else:
    response = f"I found information from {source}, but it requires verification."

# Result
result = {
    "source": source,
    "trust_level": trust_level,
    "use_directly": use_directly,
    "response": response,
    "citation": citation_format
}

print(f"\nTrust Level: {result['trust_level']}")
print(f"Citation: {result['citation']}")
```

**Modification Guide:**
- Add your specific sources (databases, APIs, etc.)
- Define trust levels for each source
- Customize citation formats

---

### Template 5: Fallback Chains (Redundancy)

**Use when:** Need primary → backup → default logic

**File:** `template_fallback_chains.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Fallback Chains (Redundancy)
# Use: Try primary, fallback to backup, use default if all fail
# ═══════════════════════════════════════════════════════════

# Configuration
primary_available = False   # ← MODIFY: Check if primary source is up
backup_available = True     # ← MODIFY: Check if backup source is up

# User query
query = "What is RAG?"  # ← MODIFY: Actual query

# Fallback chain
if primary_available:
    # Try primary source first
    source_used = "primary_database"
    # result = query_primary_db(query)  # ← MODIFY: Your primary query function
    result = f"Result from primary database for: {query}"
    latency = "fast"
    print(f"✓ Using primary source")

elif backup_available:
    # Primary failed, try backup
    source_used = "backup_database"
    # result = query_backup_db(query)  # ← MODIFY: Your backup query function
    result = f"Result from backup database for: {query}"
    latency = "medium"
    print(f"⚠ Primary unavailable - Using backup source")

else:
    # Both failed, use default/cached response
    source_used = "default_cache"
    result = "I'm having trouble accessing my knowledge base. Please try again later."
    latency = "instant"
    print(f"🚫 Both sources unavailable - Using default")

# Result
response = {
    "source": source_used,
    "result": result,
    "latency": latency,
    "query": query
}

print(f"\nSource: {response['source']}")
print(f"Result: {response['result']}")
```

**Modification Guide:**
- Add more fallback levels if needed
- Replace availability checks with actual health checks
- Customize default/cached responses

---

### Template 6: Multi-Condition Gates (AND Logic)

**Use when:** Multiple conditions must ALL be true

**File:** `template_multi_condition_and.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Multi-Condition Gates (AND Logic)
# Use: All conditions must pass
# ═══════════════════════════════════════════════════════════

# Configuration
MIN_CONFIDENCE = 0.90
APPROVED_SOURCES = ["internal_kb", "verified_api"]

# Your data
confidence = 0.92  # ← MODIFY: Your confidence score
source = "internal_kb"  # ← MODIFY: Your source
content_safe = True  # ← MODIFY: Safety check result

# Multi-condition check (ALL must be true)
if confidence >= MIN_CONFIDENCE and source in APPROVED_SOURCES and content_safe:
    # All conditions passed
    status = "approved"
    action = "return_to_user"
    response = "Processing with full approval..."
    print(f"✓ APPROVED: All checks passed")
    print(f"  - Confidence: {confidence} >= {MIN_CONFIDENCE} ✓")
    print(f"  - Source: {source} in approved list ✓")
    print(f"  - Content safe: {content_safe} ✓")

else:
    # At least one condition failed
    status = "rejected"
    action = "require_review"
    response = "This response requires human review."

    # Detailed failure reasons
    print(f"🚫 REJECTED: One or more checks failed")
    if confidence < MIN_CONFIDENCE:
        print(f"  - Confidence too low: {confidence} < {MIN_CONFIDENCE} ✗")
    if source not in APPROVED_SOURCES:
        print(f"  - Source not approved: {source} ✗")
    if not content_safe:
        print(f"  - Content safety check failed ✗")

# Result
result = {
    "status": status,
    "action": action,
    "response": response,
    "checks": {
        "confidence": confidence >= MIN_CONFIDENCE,
        "source": source in APPROVED_SOURCES,
        "safety": content_safe
    }
}

print(f"\nFinal Status: {result['status']}")
```

**Modification Guide:**
- Add/remove conditions as needed
- Adjust thresholds
- Customize failure messages

---

### Template 7: Multi-Condition Gates (OR Logic)

**Use when:** At least ONE condition must be true

**File:** `template_multi_condition_or.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Multi-Condition Gates (OR Logic)
# Use: At least one condition passes → approve
# ═══════════════════════════════════════════════════════════

# Configuration
HIGH_CONFIDENCE = 0.95
TRUSTED_SOURCES = ["internal_kb"]

# Your data
confidence = 0.88  # ← MODIFY: Your confidence score
source = "internal_kb"  # ← MODIFY: Your source

# Multi-condition check (at least ONE must be true)
if confidence >= HIGH_CONFIDENCE or source in TRUSTED_SOURCES:
    # At least one condition passed
    status = "approved"
    response = "Processing request..."

    # Detailed approval reasons
    print(f"✓ APPROVED: At least one check passed")
    if confidence >= HIGH_CONFIDENCE:
        print(f"  - Very high confidence: {confidence} >= {HIGH_CONFIDENCE} ✓")
    if source in TRUSTED_SOURCES:
        print(f"  - Trusted source: {source} ✓")

else:
    # Both conditions failed
    status = "rejected"
    response = "Cannot process - neither high confidence nor trusted source."
    print(f"🚫 REJECTED: All checks failed")
    print(f"  - Confidence: {confidence} < {HIGH_CONFIDENCE} ✗")
    print(f"  - Source: {source} not in trusted list ✗")

# Result
result = {
    "status": status,
    "response": response,
    "confidence": confidence,
    "source": source
}

print(f"\nFinal Status: {result['status']}")
```

**Modification Guide:**
- Add more OR conditions
- Balance between strict (AND) and flexible (OR) logic

---

### Template 8: Nested Logic (Two-Level Checks)

**Use when:** Second check depends on first passing

**File:** `template_nested_logic.py`

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: Nested Logic (Two-Level Checks)
# Use: Check A, then check B (only if A passes)
# ═══════════════════════════════════════════════════════════

# Your data
source_is_trusted = True  # ← MODIFY: First check
confidence = 0.92  # ← MODIFY: Second check
response_text = "RAG combines retrieval..."  # ← MODIFY: Content

# Two-level nested check
if source_is_trusted:
    # Level 1 passed - check level 2
    print(f"✓ Level 1: Source is trusted")

    if confidence > 0.90:
        # Both levels passed
        action = "return_directly"
        final_response = response_text
        add_warning = False
        print(f"  ✓ Level 2: High confidence")
        print(f"  → Action: Return directly")

    else:
        # Level 1 passed, level 2 failed
        action = "return_with_disclaimer"
        final_response = f"{response_text}\n\nNote: This answer has moderate confidence."
        add_warning = True
        print(f"  ⚠ Level 2: Lower confidence")
        print(f"  → Action: Add disclaimer")

else:
    # Level 1 failed - skip level 2
    action = "reject"
    final_response = "I cannot verify this information from untrusted sources."
    add_warning = False
    print(f"🚫 Level 1: Source not trusted")
    print(f"  → Action: Reject (skipping confidence check)")

# Result
result = {
    "action": action,
    "response": final_response,
    "warning_added": add_warning,
    "checks": {
        "source_trusted": source_is_trusted,
        "confidence_checked": source_is_trusted,  # Only checked if source trusted
        "confidence_high": confidence > 0.90 if source_is_trusted else None
    }
}

print(f"\nFinal Action: {result['action']}")
```

**Modification Guide:**
- Adjust nesting levels as needed
- Change check order based on importance
- Add more branches in each level

---

### Template 9: match/case Router (2026 Pattern — Python 3.10+)

**Use when:** Routing by name, type, or status (cleaner than long if/elif chains)

**File:** `template_intent_routing.py` — Version B section

```python
# ═══════════════════════════════════════════════════════════
# TEMPLATE: match/case Router (2026 standard for routing by name)
# Use: Route based on WHAT something IS (not a score/threshold)
# ═══════════════════════════════════════════════════════════

# Pattern A: Intent routing
match user_intent:
    case "search":
        tool_used = "search_tool"
        response = search_database(query)
    case "calculate":
        tool_used = "calculator"
        response = calculate(query)
    case "summarize":
        tool_used = "summarizer"
        response = summarize_text(query)
    case _:                          # ← _ is catch-all (same as else)
        tool_used = "default_llm"
        response = "I'm not sure I understand."

# Pattern B: Stop reason routing (real Anthropic API pattern)
match response.stop_reason:
    case "end_turn":
        return response.content[0].text
    case "tool_use":
        execute_tools(response)
    case "max_tokens":
        handle_truncation()
    case _:
        handle_unexpected()

# Pattern C: Source trust routing
match source:
    case "internal_kb":
        trust_level = "high"
    case "wikipedia":
        trust_level = "medium"
    case _:
        trust_level = "low"
```

**Modification Guide:**
- Each `case "value":` handles one specific named option
- `case _:` is always the last case (catch-all)
- Use for names/types/statuses — NOT for score comparisons

**Rule:** Score check → `if/elif`. Name/type/status routing → `match/case`

---

## Quick Selection Guide

| Need | Template | File |
|:-----|:---------|:-----|
| Quality gate for AI responses | Template 1 | confidence_threshold.py |
| Route to different tools (if/elif) | Template 2 | intent_routing.py |
| Block unsafe content | Template 3 | safety_guards.py |
| Check source trust | Template 4 | source_validation.py |
| Primary → Backup → Default | Template 5 | fallback_chains.py |
| All checks must pass | Template 6 | multi_condition_and.py |
| At least one check passes | Template 7 | multi_condition_or.py |
| Two-level checking | Template 8 | nested_logic.py |
| **Route by name/type (2026)** | **Template 9** | **intent_routing.py (Version B)** |

---

## Your Workflow

1. **Identify** what you need to route/check
2. **Pick** the matching template
3. **Copy** the entire code
4. **Modify** the marked sections (← MODIFY comments)
5. **Test** with your data
6. **Use** in your AI system

---

## You've Completed Pass 3!

You now have:
✓ **8 production-ready templates**
✓ **Copy-paste routing patterns**
✓ **Modification guides** for each template
✓ **Quick selection guide**

**Remember:** You're not writing routing logic from scratch. You're customizing proven patterns that professional AI systems use every day.

---

## Next Steps

1. Pick one template that matches your current need
2. Copy it to your project
3. Modify the values
4. See it work

Then move to **Lesson 04: Loops** to process entire collections!
