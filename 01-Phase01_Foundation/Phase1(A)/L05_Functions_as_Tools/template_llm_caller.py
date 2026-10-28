"""
TEMPLATE: LLM Caller
=====================
Use: Reusable functions for calling LLM APIs

COPY this when you need to:
- Call Claude/Anthropic API
- Manage conversation history
- Handle streaming responses
- Estimate costs before calling

2026 note: All functions use type hints.
  def fn(prompt: str, model: str = "...") -> str:  — same logic, adds type labels
"""

# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Basic LLM Call
# ═══════════════════════════════════════════════════════════
def call_llm(prompt: str, model: str = "claude-sonnet-5-5", max_tokens: int = 1000) -> str:
    """
    Simple one-shot LLM call.
    IN:  prompt (str), model (str), max_tokens (int)
    OUT: response text (str)

    UNCOMMENT and install: pip install anthropic
    """
    # import anthropic
    # client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

    # response = client.messages.create(
    #     model=model,
    #     max_tokens=max_tokens,
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.content[0].text

    # ← REMOVE THIS when using real API:
    return f"[Simulated response | model={model} | tokens≈{len(prompt)//4}]"


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: LLM Call with System Prompt
# ═══════════════════════════════════════════════════════════
def call_llm_with_system(user_message: str, system_prompt: str,
                          model: str = "claude-sonnet-5-5",
                          max_tokens: int = 1000) -> str:
    """
    LLM call with system prompt for agent behavior.
    IN:  user_message, system_prompt, model, max_tokens
    OUT: response text (str)
    """
    # import anthropic
    # client = anthropic.Anthropic()
    # response = client.messages.create(
    #     model=model,
    #     max_tokens=max_tokens,
    #     system=system_prompt,
    #     messages=[{"role": "user", "content": user_message}]
    # )
    # return response.content[0].text

    return f"[Simulated | system='{system_prompt[:30]}...' | user='{user_message[:30]}...']"


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: LLM Call with History (Multi-Turn)
# ═══════════════════════════════════════════════════════════
def call_llm_with_history(messages: list, model: str = "claude-sonnet-5-5",
                           max_tokens: int = 1000) -> str:
    """
    LLM call with full conversation history.
    IN:  messages (list of dicts: [{"role": ..., "content": ...}])
    OUT: response text (str)
    """
    # import anthropic
    # client = anthropic.Anthropic()
    # response = client.messages.create(
    #     model=model,
    #     max_tokens=max_tokens,
    #     messages=messages
    # )
    # return response.content[0].text

    return f"[Simulated | {len(messages)} messages in history]"


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: Safe LLM Call (Error Handling)
# ═══════════════════════════════════════════════════════════
def safe_call_llm(prompt: str, model: str = "claude-sonnet-5-5",
                  max_tokens: int = 1000,
                  fallback: str = "I'm having trouble responding right now.") -> str:
    """
    LLM call with error handling.
    IN:  prompt, model, max_tokens, fallback response
    OUT: response text or fallback (str)
    """
    try:
        return call_llm(prompt, model, max_tokens)
    except Exception as e:
        print(f"LLM call failed: {e}")
        return fallback


# ═══════════════════════════════════════════════════════════
# TEMPLATE 5: Cost Estimator (Before Calling)
# ═══════════════════════════════════════════════════════════
COST_PER_TOKEN = {
    "claude-sonnet-5-5": {"input": 0.000002, "output": 0.00001},
    "claude-opus-5-5":     {"input": 0.000004, "output": 0.00002},
    "claude-haiku-5-5":    {"input": 0.0000001, "output": 0.0000005},  # Haiku 5.5 rate for prompts up to 100k tokens; higher above
}

def estimate_llm_cost(prompt: str, model: str = "claude-sonnet-5-5",
                      expected_output_tokens: int = 500) -> dict:
    """
    Estimate cost before calling the LLM.
    IN:  prompt (str), model (str), expected_output_tokens (int)
    OUT: cost estimate dict
    """
    input_tokens  = len(prompt) / 4
    output_tokens = expected_output_tokens

    rates = COST_PER_TOKEN.get(model, {"input": 0.000002, "output": 0.00001})

    input_cost  = input_tokens  * rates["input"]
    output_cost = output_tokens * rates["output"]

    return {
        "model": model,
        "input_tokens": int(input_tokens),
        "output_tokens": output_tokens,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(input_cost + output_cost, 6)
    }


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    prompt = "What is RAG in the context of AI systems?"

    print("="*60)
    print("TEMPLATE 1: Basic Call")
    print("="*60)
    response = call_llm(prompt)
    print(f"Response: {response}")

    print("\n" + "="*60)
    print("TEMPLATE 2: With System Prompt")
    print("="*60)
    response2 = call_llm_with_system(
        user_message=prompt,
        system_prompt="You are a concise AI assistant. Answer in 2 sentences."
    )
    print(f"Response: {response2}")

    print("\n" + "="*60)
    print("TEMPLATE 3: With History")
    print("="*60)
    history = [
        {"role": "user", "content": "What is AI?"},
        {"role": "assistant", "content": "AI is artificial intelligence."},
        {"role": "user", "content": "What is RAG?"}
    ]
    response3 = call_llm_with_history(history)
    print(f"Response: {response3}")

    print("\n" + "="*60)
    print("TEMPLATE 5: Cost Estimate")
    print("="*60)
    cost = estimate_llm_cost(prompt, model="claude-sonnet-5-5")
    print(f"Model: {cost['model']}")
    print(f"Input tokens: {cost['input_tokens']}")
    print(f"Output tokens (est): {cost['output_tokens']}")
    print(f"Total cost: ${cost['total_cost_usd']:.6f}")
