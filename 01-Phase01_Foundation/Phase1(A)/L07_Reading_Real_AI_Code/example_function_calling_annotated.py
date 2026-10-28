"""
LESSON 5: FUNCTION CALLING AGENT (ANNOTATED)
============================================
This shows an agent that decides which tool to use.

The "advanced" pattern: Agent picks from available tools based on user input.
Spoiler: It's just L1-L4 patterns orchestrated!
"""

# ═══════════════════════════════════════════════════════════
# L3: FUNCTIONS - Define available tools
# ═══════════════════════════════════════════════════════════

def search_database(query):
    """Search internal knowledge base"""
    # Simulate database search
    results = [
        {"title": "RAG Overview", "content": "RAG combines retrieval..."},
        {"title": "Vector Search", "content": "Semantic search uses..."}
    ]
    return results

def calculate(expression):
    """Perform mathematical calculation"""
    # Simulate calculator
    try:
        result = eval(expression)  # In real code, use safer math parser
        return {"expression": expression, "result": result}
    except:
        return {"error": "Invalid expression"}

def get_weather(city):
    """Get current weather for a city"""
    # Simulate weather API
    weather_data = {
        "San Francisco": {"temp": 65, "condition": "Sunny"},
        "New York": {"temp": 45, "condition": "Cloudy"},
        "London": {"temp": 55, "condition": "Rainy"}
    }
    return weather_data.get(city, {"error": "City not found"})

print("✓ L3 PATTERN SPOTTED: Three tool functions defined")
print("  - search_database()")
print("  - calculate()")
print("  - get_weather()")
print()


# ═══════════════════════════════════════════════════════════
# L1.5: LIST OF DICTS - Tool Registry (THE PATTERN!)
# ═══════════════════════════════════════════════════════════
available_tools = [
    {
        "name": "search_database",
        "description": "Search internal knowledge base for information",
        "function": search_database,  # ← Store function reference in dict!
        "examples": ["What is RAG?", "Explain vector search"]
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "function": calculate,
        "examples": ["2 + 2", "100 * 0.15"]
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "function": get_weather,
        "examples": ["Weather in San Francisco", "London weather"]
    }
]

print("✓ L1.5 PATTERN SPOTTED: available_tools is a list of dictionaries")
print(f"  Total tools: {len(available_tools)}")
print(f"  Each dict contains: name, description, function, examples")
print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Agent decision maker
# ═══════════════════════════════════════════════════════════
def agent_decide(user_input, tools):
    """
    Decide which tool to use based on user input
    In real code: Ask LLM to analyze and choose
    Here: Simple keyword matching

    Returns: DICTIONARY (L1!) with decision
    """
    user_lower = user_input.lower()

    # L2: Logic gates to pick tool
    if any(word in user_lower for word in ["what", "explain", "search", "find"]):
        chosen_tool = "search_database"
        reasoning = "User is asking a knowledge question"

    elif any(word in user_lower for word in ["calculate", "math", "+", "-", "*", "/"]):
        chosen_tool = "calculate"
        reasoning = "User wants a calculation"

    elif any(word in user_lower for word in ["weather", "temperature", "forecast"]):
        chosen_tool = "get_weather"
        reasoning = "User is asking about weather"

    else:
        chosen_tool = "search_database"  # Default
        reasoning = "Unclear - defaulting to search"

    # L1: Return decision as dictionary
    return {
        "tool_name": chosen_tool,
        "reasoning": reasoning,
        "confidence": 0.85
    }

print("✓ L3 PATTERN SPOTTED: agent_decide is a function")
print("  Input: user text + tool list")
print("  Output: DICTIONARY with decision")
print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Execute chosen tool
# ═══════════════════════════════════════════════════════════
def execute_tool(tool_name, tools, user_input):
    """
    Find and execute the chosen tool
    This is where the magic happens: CALLING A FUNCTION STORED IN A DICT!
    """
    # L2.5: Loop through tools list
    for tool in tools:
        # L2: Check if this is the right tool
        if tool["name"] == tool_name:
            print(f"✓ Found tool: {tool_name}")

            # Extract the actual function from the dictionary
            tool_function = tool["function"]  # ← L1: Access dict value

            # L3: CALL THE FUNCTION!
            # This is the powerful part: we stored a function in a dict,
            # now we're calling it dynamically
            result = tool_function(user_input)

            return result

    # If tool not found
    return {"error": f"Tool '{tool_name}' not found"}

print("✓ L3 PATTERN SPOTTED: execute_tool is a function")
print("  It calls OTHER functions dynamically!")
print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Complete agent workflow
# ═══════════════════════════════════════════════════════════
def run_agent(user_input, tools):
    """
    Complete agent execution:
    1. Decide which tool to use (L3)
    2. Execute that tool (L3)
    3. Return structured result (L1)
    """
    print(f"\n{'='*60}")
    print(f"USER INPUT: {user_input}")
    print(f"{'='*60}")

    # Step 1: Decide
    decision = agent_decide(user_input, tools)
    print(f"\n🤔 DECISION:")
    print(f"   Tool: {decision['tool_name']}")
    print(f"   Reasoning: {decision['reasoning']}")
    print(f"   Confidence: {decision['confidence']}")

    # Step 2: Execute
    print(f"\n⚙️  EXECUTING TOOL...")
    result = execute_tool(decision["tool_name"], tools, user_input)

    # Step 3: Package result (L1: Dictionary)
    final_result = {
        "user_input": user_input,
        "tool_used": decision["tool_name"],
        "reasoning": decision["reasoning"],
        "result": result,
        "timestamp": "2026-02-28"
    }

    print(f"\n✅ RESULT:")
    print(f"   {result}")

    return final_result

print("✓ L3 PATTERN SPOTTED: run_agent orchestrates the workflow")
print()


# ═══════════════════════════════════════════════════════════
# DEMONSTRATION: Run the agent with different inputs
# ═══════════════════════════════════════════════════════════

# Test 1: Knowledge question
result1 = run_agent("What is RAG?", available_tools)

# Test 2: Calculation
result2 = run_agent("Calculate 150 * 0.20", available_tools)

# Test 3: Weather query
result3 = run_agent("What's the weather in London?", available_tools)


# ═══════════════════════════════════════════════════════════
# L1.5: LIST OF DICTS - Store interaction history
# ═══════════════════════════════════════════════════════════
interaction_history = [result1, result2, result3]

print(f"\n{'='*60}")
print("INTERACTION HISTORY (LIST OF DICTS):")
print(f"{'='*60}")
print(f"✓ L1.5 PATTERN SPOTTED: Stored {len(interaction_history)} interactions")

for i, interaction in enumerate(interaction_history, 1):  # ← L2.5: Loop!
    print(f"\n{i}. Tool Used: {interaction['tool_used']}")
    print(f"   Input: {interaction['user_input']}")

print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Analytics on tool usage
# ═══════════════════════════════════════════════════════════
def analyze_tool_usage(history):
    """
    Analyze which tools are used most
    Input: LIST OF DICTS (L1.5)
    Output: DICTIONARY (L1) with stats
    """
    # L1: Create empty dict for counting
    tool_counts = {}

    # L2.5: Loop through history
    for interaction in history:
        tool_name = interaction["tool_used"]

        # L2: Check if tool already in counts
        if tool_name in tool_counts:
            tool_counts[tool_name] += 1
        else:
            tool_counts[tool_name] = 1

    # L1: Return stats dictionary
    return {
        "total_interactions": len(history),
        "tool_counts": tool_counts,
        "most_used": max(tool_counts, key=tool_counts.get) if tool_counts else None
    }

stats = analyze_tool_usage(interaction_history)

print(f"{'='*60}")
print("USAGE ANALYTICS:")
print(f"{'='*60}")
print(f"Total Interactions: {stats['total_interactions']}")
print(f"Tool Breakdown: {stats['tool_counts']}")
print(f"Most Used: {stats['most_used']}")
print()


# ═══════════════════════════════════════════════════════════
# L2: LOGIC GATE - Usage limits
# ═══════════════════════════════════════════════════════════
MAX_DAILY_CALLS = 100

if stats["total_interactions"] > MAX_DAILY_CALLS:
    print("⚠️  L2 PATTERN: Usage limit exceeded!")
    print(f"   {stats['total_interactions']} > {MAX_DAILY_CALLS}")
    print("   Action: Throttle or notify admin")
else:
    remaining = MAX_DAILY_CALLS - stats["total_interactions"]
    print(f"✓ L2 PATTERN: Within usage limits")
    print(f"   {remaining} calls remaining today")

print()


# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print("="*60)
print("🎯 PATTERNS USED IN THIS FUNCTION-CALLING AGENT:")
print("="*60)
print("   L1:   Dictionaries for decisions, results, stats")
print("   L1.5: List of dicts for tools and history")
print("   L2:   If/else for tool selection and limits")
print("   L2.5: For loops to search tools and analyze history")
print("   L3:   Functions for decide, execute, analyze")
print("   L3+:  Storing functions IN dictionaries (advanced!)")
print()
print("💡 INSIGHT: Function-calling agents = L1-L4 patterns orchestrated")
print("   The agent doesn't 'know' anything - it just:")
print("   1. Picks from a list of dicts (L1.5)")
print("   2. Calls the function stored in that dict (L3)")
print("   3. Returns result as dict (L1)")
print()
print("🚀 YOU NOW UNDERSTAND FUNCTION CALLING!")
