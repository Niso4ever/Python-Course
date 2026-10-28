"""
TEMPLATE: Count/Sum Values
===========================
Use: Calculate totals across collection

COPY this template when you need to:
- Count total tokens in conversation
- Sum API costs
- Calculate average scores
- Track usage metrics
"""

# ═══════════════════════════════════════════════════════════
# YOUR DATA (← REPLACE WITH REAL DATA)
# ═══════════════════════════════════════════════════════════
conversation = [
    {"role": "user", "content": "Hello", "tokens": 5},
    {"role": "assistant", "content": "Hi there!", "tokens": 8},
    {"role": "user", "content": "What is RAG?", "tokens": 12},
    {"role": "assistant", "content": "RAG is...", "tokens": 45},
    {"role": "user", "content": "Thanks!", "tokens": 6}
]


# ═══════════════════════════════════════════════════════════
# SUM PATTERN
# ═══════════════════════════════════════════════════════════
total_tokens = 0

for message in conversation:
    total_tokens += message["tokens"]  # ← MODIFY: Your field to sum

print(f"Total tokens: {total_tokens}")


# ═══════════════════════════════════════════════════════════
# COUNT PATTERN
# ═══════════════════════════════════════════════════════════
user_message_count = 0

for message in conversation:
    if message["role"] == "user":  # ← MODIFY: Your condition
        user_message_count += 1

print(f"User messages: {user_message_count}")


# ═══════════════════════════════════════════════════════════
# AVERAGE PATTERN
# ═══════════════════════════════════════════════════════════
total = 0
count = 0

for message in conversation:
    total += message["tokens"]
    count += 1

if count > 0:
    average = total / count
    print(f"Average tokens per message: {average:.2f}")


# ═══════════════════════════════════════════════════════════
# CONDITIONAL SUM (Sum only specific items)
# ═══════════════════════════════════════════════════════════
assistant_tokens = 0

for message in conversation:
    if message["role"] == "assistant":
        assistant_tokens += message["tokens"]

print(f"Assistant tokens: {assistant_tokens}")


# ═══════════════════════════════════════════════════════════
# MULTIPLE COUNTERS AT ONCE
# ═══════════════════════════════════════════════════════════
stats = {
    "total_tokens": 0,
    "user_tokens": 0,
    "assistant_tokens": 0,
    "message_count": 0
}

for message in conversation:
    stats["total_tokens"] += message["tokens"]
    stats["message_count"] += 1

    if message["role"] == "user":
        stats["user_tokens"] += message["tokens"]
    elif message["role"] == "assistant":
        stats["assistant_tokens"] += message["tokens"]

print(f"\n{'='*50}")
print(f"CONVERSATION STATISTICS:")
print(f"{'='*50}")
for key, value in stats.items():
    print(f"{key}: {value}")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Sum API costs
------------------------
llm_calls = [
    {"model": "claude-opus-5-5", "tokens": 1500, "cost_per_token": 0.015},
    {"model": "claude-sonnet-5-5", "tokens": 1200, "cost_per_token": 0.003}
]

total_cost = 0
for call in llm_calls:
    total_cost += call["tokens"] * call["cost_per_token"]

Example 2: Count by category
-----------------------------
counts_by_model = {}

for call in llm_calls:
    model = call["model"]
    if model not in counts_by_model:
        counts_by_model[model] = 0
    counts_by_model[model] += 1

Example 3: Running total with limit
------------------------------------
total = 0
max_budget = 100.0

for call in llm_calls:
    cost = call["tokens"] * call["cost_per_token"]

    if total + cost > max_budget:
        print("Budget exceeded!")
        break

    total += cost

Example 4: Calculate weighted average
--------------------------------------
total_score = 0
total_weight = 0

for result in search_results:
    total_score += result["score"] * result["weight"]
    total_weight += result["weight"]

weighted_avg = total_score / total_weight if total_weight > 0 else 0
"""
