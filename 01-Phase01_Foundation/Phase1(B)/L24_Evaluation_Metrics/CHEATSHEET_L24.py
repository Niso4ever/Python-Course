"""
CHEATSHEET L24 — Evaluation & Metrics
The 7 numbers every AI architect tracks.
"""

# ── 1. ACCURACY (exact match) ─────────────────────────────────────────────────
correct = sum(1 for p, g in zip(predictions, ground_truth) if p.strip() == g.strip())
accuracy = correct / len(ground_truth)                         # → 0.0 to 1.0

# ── 2. PRECISION@K (retrieval) ───────────────────────────────────────────────
hits = sum(1 for doc in retrieved[:k] if doc in relevant_set)
precision_at_k = hits / k                                      # → 0.0 to 1.0

# ── 3. RECALL (retrieval) ────────────────────────────────────────────────────
found = sum(1 for doc in relevant_set if doc in retrieved)
recall = found / len(relevant_set)                             # → 0.0 to 1.0

# ── 4. LATENCY ───────────────────────────────────────────────────────────────
import time
start = time.perf_counter()
result = agent.run(query)
latency = time.perf_counter() - start                         # → seconds

# ── 5. PERCENTILE LATENCY ────────────────────────────────────────────────────
sorted_l = sorted(latencies)
p95 = sorted_l[int(len(sorted_l) * 0.95)]                    # → p95 cutoff

# ── 6. COST PER QUERY ────────────────────────────────────────────────────────
# claude-sonnet-5-5: $0.002/1K input, $0.010/1K output (pricing page, 2026-10-28)
cost = (input_tokens / 1000 * 0.003) + (output_tokens / 1000 * 0.015)

# ── 7. LLM-AS-JUDGE (2026 standard) ─────────────────────────────────────────
judge_prompt = f"Rate 1-5: Q={question} | Answer={answer} | Ref={reference}. Return JSON {{score, reason}}"
# score = json.loads(llm.generate(judge_prompt))["score"]

# ── THE EVAL MATRIX ──────────────────────────────────────────────────────────
# What              Metric            Target
# ─────────────────────────────────────────────
# Retrieval         Precision@k       > 80%
# Answer quality    Accuracy/Judge    > 75%
# Speed             p95 latency       < 3s
# Cost              $/query           per budget
# Reliability       Error rate        < 5%
