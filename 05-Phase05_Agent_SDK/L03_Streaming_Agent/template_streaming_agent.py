"""
TEMPLATE: Streaming Agent
CURRICULUM PATTERN: Ph5-L03
DESCRIPTION: Live token-by-token output using client.messages.stream().
             DEMO_MODE simulates streaming with time.sleep between chunks.
Run with: python template_streaming_agent.py
"""

import time
import asyncio
from dataclasses import dataclass

DEMO_MODE = True

# ──────────────────────────────────────────────
# DEMO SIMULATION
# ──────────────────────────────────────────────

DEMO_ANSWERS: dict[str, str] = {
    "rag": (
        "RAG — Retrieval-Augmented Generation — is a pattern that combines a "
        "search system with an LLM. Instead of relying on training data alone, "
        "the agent first retrieves relevant documents from a knowledge base, "
        "then generates an answer grounded in those documents. "
        "This reduces hallucinations and keeps answers current."
    ),
    "agent": (
        "An AI agent is a system that uses an LLM to decide what to do, "
        "then executes actions (tool calls), observes the results, "
        "and repeats until the task is complete. "
        "The key difference from a chatbot: agents act, not just respond."
    ),
    "stream": (
        "Streaming means tokens arrive one by one as the LLM generates them, "
        "rather than waiting for the complete response. "
        "For long answers, streaming dramatically improves perceived speed. "
        "The user sees progress immediately instead of a long pause."
    ),
}

def _get_demo_answer(query: str) -> str:
    q = query.lower()
    for key, answer in DEMO_ANSWERS.items():
        if key in q:
            return answer
    return (
        f"This is a simulated streaming response for '{query}'. "
        "In real mode, Claude would generate a full answer here, "
        "streaming each token as it's produced by the model."
    )

def _demo_stream(text: str, chunk_size: int = 4, delay: float = 0.04) -> None:
    """Simulate streaming by printing text in small chunks with delay."""
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        print(chunk, end="", flush=True)
        time.sleep(delay)
    print()


# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────

@dataclass
class StreamConfig:
    model: str = "claude-sonnet-5-5"
    max_tokens: int = 1024
    system_prompt: str = "You are a clear technical explainer. Use plain English."


# ──────────────────────────────────────────────
# STREAMING RUNNERS
# ──────────────────────────────────────────────

def stream_response(query: str, config: StreamConfig) -> str:
    """Stream a response, printing tokens as they arrive.

    Args:
        query: The user's question.
        config: Model and prompt configuration.

    Returns:
        The complete response text after streaming finishes.
    """
    if DEMO_MODE:
        answer = _get_demo_answer(query)
        print(f"Streaming: ", end="")
        _demo_stream(answer)
        return answer

    import anthropic  # type: ignore
    client = anthropic.Anthropic()
    full_text = ""

    with client.messages.stream(
        model=config.model,
        max_tokens=config.max_tokens,
        system=config.system_prompt,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text += text
    print()
    return full_text


def stream_with_final(query: str, config: StreamConfig) -> tuple[str, dict]:
    """Stream response and also return the final structured message.

    Args:
        query: The user's question.
        config: Model and prompt configuration.

    Returns:
        Tuple of (streamed_text, usage_dict with input/output tokens).
    """
    if DEMO_MODE:
        answer = _get_demo_answer(query)
        _demo_stream(answer)
        return answer, {"input_tokens": 50, "output_tokens": len(answer.split()) * 2}

    import anthropic  # type: ignore
    client = anthropic.Anthropic()
    full_text = ""

    with client.messages.stream(
        model=config.model,
        max_tokens=config.max_tokens,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text += text
        final = stream.get_final_message()

    print()
    usage = {
        "input_tokens": final.usage.input_tokens,
        "output_tokens": final.usage.output_tokens,
    }
    return full_text, usage


# ──────────────────────────────────────────────
# DEMO
# ──────────────────────────────────────────────

def main() -> None:
    config = StreamConfig()

    queries = [
        ("What is RAG?", "stream_response"),
        ("What is an AI agent?", "stream_with_final"),
    ]

    for i, (query, mode) in enumerate(queries, 1):
        print(f"\n{'='*55}")
        print(f"Query {i} ({mode}): {query}")
        print("-" * 55)

        if mode == "stream_response":
            stream_response(query, config)
        else:
            text, usage = stream_with_final(query, config)
            print(f"\nTokens used: input={usage['input_tokens']}, output={usage['output_tokens']}")

    print(f"\n[{'DEMO' if DEMO_MODE else 'REAL API'} MODE]")
    if DEMO_MODE:
        print("[Set DEMO_MODE=False and add ANTHROPIC_API_KEY for real streaming]")


if __name__ == "__main__":
    main()
