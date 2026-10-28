"""
MY PERSONAL TEMPLATE: LLM API Call Metadata
============================================
Copy-paste this whenever you need to track LLM calls

Usage:
1. Copy this template
2. Modify the values
3. Use it to log every LLM interaction
"""

# ============================================================================
# TEMPLATE: Track a single LLM API call
# ============================================================================

llm_call_metadata = {
    # Model information
    "model": "claude-opus-5-5",       # Which model
    "provider": "anthropic",                  # anthropic, openai, etc.

    # Token usage (for cost tracking)
    "tokens_total": 1523,                     # Total tokens
    "tokens_input": 412,                      # Prompt tokens
    "tokens_output": 1111,                    # Response tokens

    # Performance metrics
    "latency_ms": 842,                        # Response time
    "temperature": 0.7,                       # Sampling temperature

    # Cost tracking
    "cost_usd": 0.0234,                       # Estimated cost

    # Status
    "success": True,                          # Did call succeed?
    "error_message": None,                    # Error if failed

    # Timestamps
    "timestamp": "2026-02-26T14:30:00Z"      # When it happened
}

# ============================================================================
# HOW TO USE THIS
# ============================================================================

# After making an LLM call, fill in the metadata:
# 2026 style — type hints added (same function, just labeled):
def log_llm_call(prompt: str, response: str, model: str = "claude-opus-5-5") -> dict:
    """Track an LLM call for monitoring/debugging"""

    call_metadata = {
        "model": model,
        "tokens_total": len(prompt) + len(response),  # Simplified
        "prompt_length": len(prompt),
        "response_length": len(response),
        "timestamp": "2026-02-26T14:30:00Z"  # Use real timestamp
    }

    # In production: Send to logging service
    print(f"LLM Call logged: {call_metadata}")
    return call_metadata


# ============================================================================
# MODIFY FOR YOUR USE CASE
# ============================================================================

# If you need to track additional info:
extended_llm_metadata = {
    "model": "claude-opus-5-5",
    "tokens": 1500,
    "cost": 0.02,

    # Add your custom fields here:
    "user_id": "user_123",
    "session_id": "session_456",
    "use_case": "customer_support",
    "quality_score": 0.92
}
