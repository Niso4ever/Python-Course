"""
TEMPLATE: Debug Toolkit for AI Projects
=========================================
Drop-in debugging functions for any AI pipeline.

COPY what you need. Remove when done debugging.

Usage: paste at top of your file, call the functions before failing lines.
"""
import os
import json
import time
from typing import Any

# ═══════════════════════════════════════════════════════════
# TOOL 1: Universal Variable Inspector
# ═══════════════════════════════════════════════════════════
def inspect(var: Any, label: str = "variable", max_len: int = 200):
    """
    Print everything useful about any variable.
    Use before any line that crashes with AttributeError or TypeError.
    """
    print(f"\n{'─'*50}")
    print(f"INSPECT: {label}")
    print(f"  type:  {type(var).__name__}")
    print(f"  repr:  {repr(var)[:max_len]}")
    if isinstance(var, dict):
        print(f"  keys:  {list(var.keys())}")
    elif isinstance(var, list):
        print(f"  len:   {len(var)}")
        if var:
            print(f"  first: {repr(var[0])[:max_len]}")
    elif isinstance(var, str):
        print(f"  len:   {len(var)}")
    print(f"{'─'*50}")

# Usage:
# inspect(response, "llm response")
# inspect(docs, "retrieved docs")
# inspect(docs[0], "first doc")


# ═══════════════════════════════════════════════════════════
# TOOL 2: RAG Pipeline Audit (stage by stage)
# ═══════════════════════════════════════════════════════════
def audit_rag_call(question: str, docs: list, context: str,
                   prompt: str, response: str):
    """
    Print a full audit of one RAG pipeline call.
    Paste this into your answer() method to see every stage.
    """
    print(f"\n{'='*60}")
    print(f"RAG AUDIT: '{question[:60]}'")

    print(f"\n[1] RETRIEVAL: {len(docs)} docs found")
    if not docs:
        print("    ⚠ WARNING: No documents! Check: db populated? threshold too high?")
    for i, d in enumerate(docs[:3]):
        score = d.get("score", d.get("distance", d.get("relevance", "?")))
        text  = str(d.get("text", d.get("page_content", d)))[:80]
        print(f"    Doc {i+1}: score={score} | {text}")

    print(f"\n[2] CONTEXT: {len(context)} chars (~{len(context)//4} tokens)")
    if len(context) < 20:
        print("    ⚠ WARNING: Context almost empty!")
    print(f"    Preview: {context[:150]}")

    print(f"\n[3] PROMPT: ~{len(prompt)//4} tokens")
    print(f"    Full prompt:\n    {prompt[:300]}")

    print(f"\n[4] RESPONSE: {len(response)} chars")
    print(f"    {response[:300]}")
    print(f"{'='*60}\n")


# ═══════════════════════════════════════════════════════════
# TOOL 3: Timer Decorator
# ═══════════════════════════════════════════════════════════
def timed(func):
    """
    Decorator: prints how long a function takes.
    Add @timed above any slow function to measure it.
    """
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱ {func.__name__}() took {elapsed:.2f}s")
        return result
    return wrapper

# Usage:
# @timed
# def answer(self, question):
#     ...


# ═══════════════════════════════════════════════════════════
# TOOL 4: Token Budget Tracker
# ═══════════════════════════════════════════════════════════
class TokenBudget:
    """
    Track token usage across multiple LLM calls.
    Attach to your agent to monitor costs.
    """
    RATES = {
        "claude-sonnet-5-5":         {"input": 0.000002, "output": 0.00001},
        "claude-opus-5-5":           {"input": 0.000004, "output": 0.00002},
        "claude-haiku-5-5":          {"input": 0.0000001, "output": 0.0000005},  # Haiku 5.5 rate for prompts up to 100k tokens; higher above
    }

    def __init__(self, model: str = "claude-sonnet-5-5"):
        self.model        = model
        self.total_input  = 0
        self.total_output = 0
        self.calls        = 0

    def track(self, input_tokens: int, output_tokens: int):
        self.total_input  += input_tokens
        self.total_output += output_tokens
        self.calls        += 1

    def report(self):
        rates      = self.RATES.get(self.model, self.RATES["claude-sonnet-5-5"])
        input_cost  = self.total_input  * rates["input"]
        output_cost = self.total_output * rates["output"]
        total_cost  = input_cost + output_cost

        print(f"\n{'='*40}")
        print(f"TOKEN BUDGET REPORT")
        print(f"  Model:        {self.model}")
        print(f"  API calls:    {self.calls}")
        print(f"  Input tokens: {self.total_input:,}")
        print(f"  Output tokens:{self.total_output:,}")
        print(f"  Cost:         ${total_cost:.4f}")
        print(f"  Per call:     ${total_cost/max(self.calls,1):.4f}")
        print(f"{'='*40}")

# Usage:
# budget = TokenBudget("claude-sonnet-5-5")
# response = client.messages.create(...)
# budget.track(response.usage.input_tokens, response.usage.output_tokens)
# budget.report()


# ═══════════════════════════════════════════════════════════
# TOOL 5: Safe Retry Wrapper
# ═══════════════════════════════════════════════════════════
import time as _time

def with_retry(func, *args, max_retries: int = 3, **kwargs):
    """
    Call any function with automatic retry on failure.
    Works for sync functions.
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            wait = 2 ** attempt
            print(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
            _time.sleep(wait)
    raise RuntimeError(f"Failed after {max_retries} attempts")

# Usage:
# result = with_retry(client.messages.create,
#                     model="claude-sonnet-5-5",
#                     max_tokens=1000,
#                     messages=[...])


# ═══════════════════════════════════════════════════════════
# TOOL 6: JSON Parse Safety
# ═══════════════════════════════════════════════════════════
def safe_json(text: str, default: Any = None) -> Any:
    """Parse JSON from LLM output safely — never crashes."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from a larger text (LLM sometimes adds explanation)
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        print(f"Warning: Could not parse as JSON. Raw: {text[:100]}")
        return default or {"raw_text": text}

# Usage:
# data = safe_json(llm_response)   # never crashes


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=== Debug Toolkit Demo ===\n")

    # inspect()
    sample_docs = [
        {"text": "RAG is Retrieval-Augmented Generation.", "score": 0.92},
        {"text": "Vector databases store embeddings.", "score": 0.85},
    ]
    inspect(sample_docs, "retrieved docs")
    inspect(sample_docs[0], "first doc")

    # audit_rag_call()
    audit_rag_call(
        question="What is RAG?",
        docs=sample_docs,
        context="RAG is Retrieval-Augmented Generation. Vector databases store embeddings.",
        prompt="Context: RAG is...\nQ: What is RAG?\nAnswer:",
        response="RAG stands for Retrieval-Augmented Generation, a technique that..."
    )

    # safe_json()
    print("safe_json() tests:")
    print(safe_json('{"answer": "yes", "confidence": 0.9}'))
    print(safe_json("Here is the answer: not json at all"))

    # TokenBudget
    budget = TokenBudget("claude-sonnet-5-5")
    budget.track(500, 200)
    budget.track(800, 350)
    budget.report()
