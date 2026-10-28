"""
TEMPLATE: AI System Evaluator
CURRICULUM PATTERN: L24
DESCRIPTION: Run quality, cost, and latency measurements on any AI system.
Run with: python template_evaluator.py
"""

import time
import json
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

DEMO_MODE = True  # Set False to use a real LLM

# ──────────────────────────────────────────────
# DATA SHAPES
# ──────────────────────────────────────────────

class TestCase(BaseModel):
    question: str = Field(description="Input sent to the system")
    expected: str = Field(description="Ground-truth answer")

class EvalResult(BaseModel):
    question: str = Field(description="Original question")
    expected: str = Field(description="Ground-truth answer")
    actual: str = Field(description="System's answer")
    correct: bool = Field(description="Exact-match pass/fail")
    latency_s: float = Field(description="Response time in seconds")
    input_tokens: int = Field(default=0, description="Tokens in the prompt")
    output_tokens: int = Field(default=0, description="Tokens in the response")

@dataclass
class EvalSummary:
    accuracy: float
    avg_latency_s: float
    total_cost_usd: float
    passed: int
    failed: int
    total: int


# ──────────────────────────────────────────────
# METRIC FUNCTIONS
# ──────────────────────────────────────────────

def precision_at_k(retrieved: list[str], relevant: list[str], k: int) -> float:
    """Of the top-k retrieved docs, what fraction are relevant?

    Args:
        retrieved: Ordered list of retrieved doc IDs.
        relevant: Set of known-relevant doc IDs.
        k: Cutoff rank.

    Returns:
        Precision score between 0.0 and 1.0.
    """
    top_k = retrieved[:k]
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / k if k else 0.0


def recall(retrieved: list[str], relevant: list[str]) -> float:
    """Of all relevant docs, what fraction did we retrieve?

    Args:
        retrieved: List of retrieved doc IDs.
        relevant: Set of known-relevant doc IDs.

    Returns:
        Recall score between 0.0 and 1.0.
    """
    if not relevant:
        return 0.0
    found = sum(1 for doc in relevant if doc in retrieved)
    return found / len(relevant)


MODEL_COSTS: dict[str, dict[str, float]] = {
    "claude-sonnet-5-5": {"input": 0.003,    "output": 0.015},
    "claude-haiku-5-5":  {"input": 0.00025,  "output": 0.00125},
    "gpt-4o":            {"input": 0.0025,   "output": 0.01},
    "gpt-4o-mini":       {"input": 0.00015,  "output": 0.0006},
    "gemini-flash":      {"input": 0.000075, "output": 0.0003},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate USD cost for one API call.

    Args:
        model: Model identifier key from MODEL_COSTS.
        input_tokens: Number of prompt tokens.
        output_tokens: Number of completion tokens.

    Returns:
        Cost in USD.
    """
    rates = MODEL_COSTS.get(model, {"input": 0.001, "output": 0.002})
    return (input_tokens / 1000 * rates["input"]) + (output_tokens / 1000 * rates["output"])


def percentile(values: list[float], p: int) -> float:
    """Return the p-th percentile of a list of values.

    Args:
        values: List of numeric measurements.
        p: Percentile (0–100).

    Returns:
        The value at the requested percentile.
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * p / 100)
    return sorted_vals[min(idx, len(sorted_vals) - 1)]


# ──────────────────────────────────────────────
# EVALUATION RUNNER
# ──────────────────────────────────────────────

def _demo_agent(question: str) -> tuple[str, int, int]:
    """Simulates an LLM response. Returns (answer, input_tokens, output_tokens)."""
    time.sleep(0.05)
    answers = {
        "What is RAG?": "Retrieval-Augmented Generation — fetch docs, then generate.",
        "What is a vector database?": "A database that stores embeddings for similarity search.",
        "What is a tool in AI?": "A function the LLM can call to act on the world.",
    }
    answer = answers.get(question, "I don't know.")
    return answer, len(question.split()) * 3, len(answer.split()) * 2


def run_evaluation(
    test_cases: list[TestCase],
    model: str = "claude-sonnet-5-5",
) -> tuple[list[EvalResult], EvalSummary]:
    """Run a test suite against the agent and return results + summary.

    Args:
        test_cases: List of question/expected pairs.
        model: Model name for cost calculation.

    Returns:
        Tuple of (individual results, aggregate summary).
    """
    results: list[EvalResult] = []

    for case in test_cases:
        start = time.perf_counter()

        if DEMO_MODE:
            actual, input_tok, output_tok = _demo_agent(case.question)
        else:
            # Replace with your real agent call:
            # actual = my_agent.run(case.question)
            actual, input_tok, output_tok = "", 0, 0

        latency = round(time.perf_counter() - start, 3)
        correct = actual.strip().lower() == case.expected.strip().lower()

        results.append(EvalResult(
            question=case.question,
            expected=case.expected,
            actual=actual,
            correct=correct,
            latency_s=latency,
            input_tokens=input_tok,
            output_tokens=output_tok,
        ))

    total = len(results)
    passed = sum(r.correct for r in results)
    total_cost = sum(
        calculate_cost(model, r.input_tokens, r.output_tokens) for r in results
    )
    avg_latency = sum(r.latency_s for r in results) / total if total else 0.0

    summary = EvalSummary(
        accuracy=passed / total if total else 0.0,
        avg_latency_s=round(avg_latency, 3),
        total_cost_usd=round(total_cost, 6),
        passed=passed,
        failed=total - passed,
        total=total,
    )

    return results, summary


# ──────────────────────────────────────────────
# DEMO
# ──────────────────────────────────────────────

if __name__ == "__main__":
    test_suite = [
        TestCase(
            question="What is RAG?",
            expected="Retrieval-Augmented Generation — fetch docs, then generate.",
        ),
        TestCase(
            question="What is a vector database?",
            expected="A database that stores embeddings for similarity search.",
        ),
        TestCase(
            question="What is a tool in AI?",
            expected="WRONG EXPECTED — intentional fail to show metric",
        ),
    ]

    print("Running evaluation...\n")
    results, summary = run_evaluation(test_suite)

    for r in results:
        status = "✓" if r.correct else "✗"
        print(f"  {status} [{r.latency_s}s] {r.question}")
        if not r.correct:
            print(f"      Expected: {r.expected}")
            print(f"      Got:      {r.actual}")

    print(f"\n── Summary ──────────────────────────")
    print(f"  Accuracy:    {summary.accuracy:.0%}  ({summary.passed}/{summary.total})")
    print(f"  Avg latency: {summary.avg_latency_s}s")
    print(f"  Total cost:  ${summary.total_cost_usd:.6f}")

    # RAG retrieval metrics demo
    print(f"\n── Retrieval Metrics ────────────────")
    retrieved = ["doc_a", "doc_c", "doc_b", "doc_x"]
    relevant  = ["doc_a", "doc_b", "doc_d"]
    print(f"  Precision@4: {precision_at_k(retrieved, relevant, 4):.0%}")
    print(f"  Recall:      {recall(retrieved, relevant):.0%}")

    # Latency percentiles demo
    sample_latencies = [0.8, 1.2, 0.9, 2.1, 1.1, 0.7, 3.4, 1.0, 1.3, 0.9]
    print(f"\n── Latency Percentiles ──────────────")
    print(f"  p50: {percentile(sample_latencies, 50):.2f}s")
    print(f"  p95: {percentile(sample_latencies, 95):.2f}s")
    print(f"  p99: {percentile(sample_latencies, 99):.2f}s")
