"""
MY PERSONAL TEMPLATE: AI Agent Configuration
=============================================
Copy-paste this for agent settings and state tracking

Usage:
1. Copy this template
2. Customize for your agent's needs
3. Use to configure RAG systems, chatbots, etc.

2026 note: In real code you may see type-hinted config variables:
  rag_config: dict = {...}             # dict with type label
  agent_state: dict = {...}            # dict with type label
  token_budget: dict = {...}           # dict with type label
"""

# ============================================================================
# TEMPLATE: RAG System Configuration
# ============================================================================

rag_config = {
    # Retrieval settings
    "relevance_threshold": 0.85,              # Min score to include (0.0-1.0)
    "max_context_docs": 3,                    # Max docs in LLM context
    "require_verification": True,             # Only use verified sources?

    # LLM settings
    "model": "claude-opus-5-5",                 # Which LLM to use
    "temperature": 0.7,                       # Creativity (0.0-1.0)
    "max_tokens": 500,                        # Max response length

    # System behavior
    "enable_fallback": True,                  # Use fallback if no results?
    "fallback_message": "I don't have enough information to answer."
}

# ============================================================================
# TEMPLATE: Agent State Tracking
# ============================================================================

# Track what the agent is currently doing
agent_state = {
    # Current status
    "current_task": "searching",              # What step is it on?
    "step_number": 3,                         # Which step (1, 2, 3...)

    # History tracking
    "history": [                              # What has it done?
        "initialized",
        "received_query",
        "searching"
    ],

    # Results so far
    "results_found": 0,                       # How many results?
    "errors": [],                             # Any errors occurred?

    # Metadata
    "start_time": "14:30:00",
    "user_id": "user_123"
}

# Add new step to history
agent_state["history"].append("filtering_results")
agent_state["step_number"] = 4

# ============================================================================
# TEMPLATE: Multi-Tool Agent Configuration
# ============================================================================

agent_tools = {
    # Each tool has its own configuration
    "search": {
        "name": "Vector Search",
        "enabled": True,
        "cost_per_call": 0.01,
        "description": "Search knowledge base"
    },

    "summarize": {
        "name": "Text Summarizer",
        "enabled": True,
        "cost_per_call": 0.005,
        "description": "Summarize long documents"
    },

    "calculate": {
        "name": "Calculator",
        "enabled": False,  # Disabled for now
        "cost_per_call": 0.001,
        "description": "Perform calculations"
    }
}

# Check if a tool is available
if agent_tools["search"]["enabled"]:
    print("Search tool is available")

# Get cost estimate
search_cost = agent_tools["search"]["cost_per_call"]

# ============================================================================
# TEMPLATE: Token Budget Tracking
# ============================================================================

token_budget = {
    "max_tokens": 100000,                     # Monthly limit
    "used_tokens": 0,                         # How many used so far
    "remaining": 100000,                      # How many left
    "calls": []                               # History of calls
}

# After each LLM call, update:
call_tokens = 1500
token_budget["used_tokens"] += call_tokens
token_budget["remaining"] = token_budget["max_tokens"] - token_budget["used_tokens"]
token_budget["calls"].append({
    "tokens": call_tokens,
    "timestamp": "14:30:00"
})

# Check if budget exceeded
if token_budget["remaining"] < 0:
    print("WARNING: Token budget exceeded!")

# ============================================================================
# MODIFY FOR YOUR USE CASE
# ============================================================================

# Custom agent config example:
my_custom_agent = {
    "name": "CustomerSupportBot",
    "version": "2.0",

    # Your custom settings:
    "response_style": "friendly",
    "max_conversation_turns": 10,
    "escalate_to_human": False,

    # Your custom state:
    "active_conversations": 0,
    "total_conversations_today": 0
}
