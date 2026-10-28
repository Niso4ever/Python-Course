# Lesson 20: Evaluation & Metrics — Measuring AI Quality
## The Quality Inspector Theory

> **2026 Reality:** Building an AI system is easy. Knowing if it's GOOD is hard.
> An architect who builds but never measures is guessing.
> Evaluation is THE skill that separates hobbyist from professional.

---

## The Architect's Question

It's NOT: "Does it run?"
It IS: "How well does it perform, at what cost, with what latency?"

```
BEFORE EVALUATION:
  "My RAG system seems to work pretty well."

AFTER EVALUATION:
  "My RAG system retrieves relevant docs 84% of the time (precision@4),
   answers correctly 76% of the time (accuracy), costs $0.003/query,
   and has p95 latency of 2.1 seconds."
```

The second statement is what an architect delivers.

---

## 1. RAG Evaluation Metrics

### Retrieval Quality (Is it finding the right documents?)

```python
def precision_at_k(retrieved: list[str], relevant: list[str], k: int) -> float:
    """Of the top-k retrieved docs, how many are actually relevant?"""
    top_k = retrieved[:k]
    relevant_found = sum(1 for doc in top_k if doc in relevant)
    return relevant_found / k

def recall(retrieved: list[str], relevant: list[str]) -> float:
    """Of all relevant docs, how many did we find?"""
    found = sum(1 for doc in relevant if doc in retrieved)
    return found / len(relevant) if relevant else 0

# Example:
retrieved_docs = ["doc_a", "doc_c", "doc_b", "doc_x"]
relevant_docs = ["doc_a", "doc_b", "doc_d"]

print(f"Precision@4: {precision_at_k(retrieved_docs, relevant_docs, 4):.0%}")  # 50%
print(f"Recall: {recall(retrieved_docs, relevant_docs):.0%}")  # 67%
```

### Answer Quality (Is the answer correct?)

```python
def answer_accuracy(predictions: list[str], ground_truth: list[str]) -> float:
    """Exact match accuracy."""
    correct = sum(1 for p, g in zip(predictions, ground_truth) if p.strip().lower() == g.strip().lower())
    return correct / len(ground_truth)

# Better: LLM-as-Judge (2026 standard)
def llm_judge(question: str, answer: str, reference: str) -> dict:
    """Use an LLM to evaluate answer quality."""
    prompt = f"""Rate this answer on a scale of 1-5:
    Question: {question}
    Answer: {answer}  
    Reference: {reference}
    
    Return JSON: {{"score": int, "reasoning": str}}"""
    
    # Call your LLM here
    # result = llm.generate(prompt)
    # return json.loads(result)
```

---

## 2. Agent Evaluation Metrics

```python
# Task completion rate
def task_completion(results: list[dict]) -> float:
    """What percentage of tasks did the agent complete successfully?"""
    completed = sum(1 for r in results if r.get("completed"))
    return completed / len(results)

# Tool use efficiency
def tool_efficiency(results: list[dict]) -> dict:
    """How many tool calls per task? Fewer = more efficient."""
    total_calls = sum(r.get("tool_calls", 0) for r in results)
    avg_calls = total_calls / len(results)
    return {"avg_tool_calls": avg_calls, "total": total_calls}

# Error rate
def error_rate(results: list[dict]) -> float:
    """How often does the agent encounter errors?"""
    errors = sum(1 for r in results if r.get("error"))
    return errors / len(results)
```

---

## 3. Token Economics (The Architect's Budget)

```python
# Cost calculation for any LLM
MODEL_COSTS = {
    "gpt-4o-mini":       {"input": 0.00015, "output": 0.0006},   # per 1K tokens
    "gpt-4o":            {"input": 0.0025,  "output": 0.01},
    "claude-sonnet-5-5": {"input": 0.003,   "output": 0.015},
    "gemini-flash":      {"input": 0.000075,"output": 0.0003},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost for a single API call."""
    costs = MODEL_COSTS.get(model, {"input": 0.001, "output": 0.002})
    return (input_tokens / 1000 * costs["input"]) + (output_tokens / 1000 * costs["output"])

def daily_cost_estimate(queries_per_day: int, avg_input: int, avg_output: int, model: str) -> dict:
    """Estimate daily/monthly costs."""
    per_query = calculate_cost(model, avg_input, avg_output)
    daily = per_query * queries_per_day
    monthly = daily * 30
    return {
        "per_query": f"${per_query:.4f}",
        "daily": f"${daily:.2f}",
        "monthly": f"${monthly:.2f}",
        "model": model
    }

# Example: RAG system with 500 queries/day
print(daily_cost_estimate(500, 2000, 500, "gpt-4o-mini"))
# {'per_query': '$0.0006', 'daily': '$0.30', 'monthly': '$9.00'}

print(daily_cost_estimate(500, 2000, 500, "gpt-4o"))
# {'per_query': '$0.0100', 'daily': '$5.00', 'monthly': '$150.00'}
# 16x more expensive for the same task!
```

**Architect's decision:** Start with the cheapest model. Only upgrade when quality metrics demand it.

---

## 4. Latency Measurement

```python
import time

def measure_latency(func, *args, **kwargs) -> dict:
    """Measure execution time of any function."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return {"result": result, "latency_seconds": round(elapsed, 3)}

# Usage
timing = measure_latency(agent.run_sync, "What is RAG?")
print(f"Answer in {timing['latency_seconds']}s")

# Track p50, p95, p99 latencies
def percentile_latency(latencies: list[float], p: int) -> float:
    """Calculate p50, p95, p99 latency."""
    sorted_l = sorted(latencies)
    idx = int(len(sorted_l) * p / 100)
    return sorted_l[min(idx, len(sorted_l) - 1)]
```

---

## 5. The Evaluation Pipeline

```python
# Every project should have this file: eval.py

def run_evaluation(test_cases: list[dict]) -> dict:
    """Run full evaluation suite."""
    results = []
    
    for case in test_cases:
        start = time.perf_counter()
        answer = agent.run_sync(case["question"])
        latency = time.perf_counter() - start
        
        results.append({
            "question": case["question"],
            "expected": case["expected"],
            "actual": answer,
            "correct": answer.strip().lower() == case["expected"].strip().lower(),
            "latency": latency,
            "tokens_used": getattr(answer, 'usage', {})
        })
    
    # Aggregate metrics
    accuracy = sum(r["correct"] for r in results) / len(results)
    avg_latency = sum(r["latency"] for r in results) / len(results)
    
    return {
        "accuracy": f"{accuracy:.1%}",
        "avg_latency": f"{avg_latency:.2f}s",
        "total_tests": len(results),
        "passed": sum(r["correct"] for r in results),
        "failed": sum(not r["correct"] for r in results),
    }
```

---

## 6. The Evaluation Matrix (Architect's Checklist)

| What to Measure | Metric | Target |
|:----------------|:-------|:-------|
| **Retrieval quality** | Precision@k, Recall | >80% |
| **Answer quality** | Accuracy, LLM-as-judge | >75% |
| **Cost** | $/query, $/day, $/month | Depends on budget |
| **Latency** | p50, p95 response time | <3s for interactive |
| **Reliability** | Error rate, uptime | <5% errors |
| **Safety** | Toxicity rate, PII leaks | <0.1% |
| **Token efficiency** | Tokens/query, cache hit rate | Optimize continuously |

---

## 7. Key Takeaways

✓ **Build → Measure → Improve** is the architect's loop
✓ **Precision@k and Recall** measure retrieval quality
✓ **LLM-as-Judge** is the 2026 standard for answer quality
✓ **Token economics** can make or break a project (16x cost difference between models)
✓ **Every project needs an eval.py** — no exceptions
✓ **Start with the cheapest model** — upgrade only when metrics demand it
✓ **Track latency percentiles** — p95 matters more than average
