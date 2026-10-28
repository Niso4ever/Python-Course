"""
TEMPLATE: Intent Routing (Multi-Tool Agent)
============================================
Use: Route user requests to appropriate tools based on intent

COPY this template when you need to:
- Build multi-tool agents
- Route different intents to different handlers
- Classify and dispatch user requests

2026 NOTE: Two versions below.
- Version A: if/elif/else  (works everywhere, still common)
- Version B: match/case    (Python 3.10+, preferred for routing by name)
"""

# ═══════════════════════════════════════════════════════════
# YOUR DATA (← REPLACE WITH REAL DATA)
# ═══════════════════════════════════════════════════════════
user_intent = "search"  # ← From your intent classifier
user_query = "What is RAG?"  # ← Actual user input


# ═══════════════════════════════════════════════════════════
# VERSION A: if/elif/else  (classic, still valid)
# ═══════════════════════════════════════════════════════════

if user_intent == "greeting":
    # ─────────────────────────────────────────────────────────
    # GREETING HANDLER
    # ─────────────────────────────────────────────────────────
    tool_used = "greeting_handler"
    response = "Hello! How can I help you today?"
    print(f"✓ ROUTE: Greeting → Simple response")

elif user_intent == "search":
    # ─────────────────────────────────────────────────────────
    # SEARCH TOOL
    # ─────────────────────────────────────────────────────────
    tool_used = "search_tool"
    # UNCOMMENT when you have your search function:
    # response = search_database(user_query)

    # For now:
    response = f"Searching knowledge base for: {user_query}"
    print(f"✓ ROUTE: Search → Knowledge base")

elif user_intent == "calculate":
    # ─────────────────────────────────────────────────────────
    # CALCULATOR TOOL
    # ─────────────────────────────────────────────────────────
    tool_used = "calculator"
    # UNCOMMENT when you have your calculator function:
    # response = calculate(user_query)

    # For now:
    response = f"Calculating: {user_query}"
    print(f"✓ ROUTE: Calculate → Math tool")

elif user_intent == "weather":
    # ─────────────────────────────────────────────────────────
    # WEATHER API
    # ─────────────────────────────────────────────────────────
    tool_used = "weather_api"
    # UNCOMMENT when you have your weather function:
    # location = extract_location(user_query)
    # response = get_weather(location)

    # For now:
    response = f"Fetching weather for query: {user_query}"
    print(f"✓ ROUTE: Weather → API call")

elif user_intent == "summarize":
    # ─────────────────────────────────────────────────────────
    # SUMMARIZATION TOOL
    # ─────────────────────────────────────────────────────────
    tool_used = "summarizer"
    # UNCOMMENT when you have your summarization function:
    # response = summarize_text(user_query)

    # For now:
    response = f"Summarizing: {user_query}"
    print(f"✓ ROUTE: Summarize → Text processor")

else:
    # ─────────────────────────────────────────────────────────
    # DEFAULT / UNKNOWN INTENT
    # ─────────────────────────────────────────────────────────
    tool_used = "default_llm"
    response = "I'm not sure I understand. Could you rephrase that?"
    print(f"⚠ ROUTE: Unknown intent '{user_intent}' → Default handler")


# ═══════════════════════════════════════════════════════════
# RESULT (Use this in your AI system)
# ═══════════════════════════════════════════════════════════
result = {
    "intent": user_intent,
    "tool_used": tool_used,
    "response": response,
    "query": user_query
}

print(f"\n{'='*50}")
print(f"ROUTING RESULT:")
print(f"{'='*50}")
print(f"Intent: {result['intent']}")
print(f"Tool: {result['tool_used']}")
print(f"Response: {result['response']}")


# ═══════════════════════════════════════════════════════════
# VERSION B: match/case  (Python 3.10+, 2026 preferred style)
# Use this when routing by a name/type — cleaner, more readable
# ═══════════════════════════════════════════════════════════

match user_intent:
    case "greeting":
        tool_used = "greeting_handler"
        response = "Hello! How can I help you today?"
        print("✓ ROUTE: Greeting → Simple response")

    case "search":
        tool_used = "search_tool"
        # response = search_database(user_query)  ← UNCOMMENT when ready
        response = f"Searching knowledge base for: {user_query}"
        print("✓ ROUTE: Search → Knowledge base")

    case "calculate":
        tool_used = "calculator"
        # response = calculate(user_query)  ← UNCOMMENT when ready
        response = f"Calculating: {user_query}"
        print("✓ ROUTE: Calculate → Math tool")

    case "weather":
        tool_used = "weather_api"
        # response = get_weather(extract_location(user_query))  ← UNCOMMENT
        response = f"Fetching weather for: {user_query}"
        print("✓ ROUTE: Weather → API call")

    case "summarize":
        tool_used = "summarizer"
        # response = summarize_text(user_query)  ← UNCOMMENT when ready
        response = f"Summarizing: {user_query}"
        print("✓ ROUTE: Summarize → Text processor")

    case _:                                       # ← catch-all (like else)
        tool_used = "default_llm"
        response = "I'm not sure I understand. Could you rephrase that?"
        print(f"⚠ ROUTE: Unknown intent '{user_intent}' → Default handler")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Add new tool
-----------------------
elif user_intent == "translate":
    tool_used = "translator"
    response = translate(user_query, target_lang="es")

Example 2: Combine multiple intents
------------------------------------
elif user_intent in ["search", "question", "query"]:
    tool_used = "search_tool"
    response = search_database(user_query)

Example 3: Priority routing
----------------------------
if user_intent == "emergency":
    tool_used = "priority_handler"
    response = escalate_to_human(user_query)
elif user_intent == "greeting":
    # ... rest of routing

Example 4: Tool selection based on content
-------------------------------------------
elif user_intent == "search":
    if "weather" in user_query.lower():
        tool_used = "weather_api"
        response = get_weather(user_query)
    else:
        tool_used = "search_tool"
        response = search_database(user_query)
"""
