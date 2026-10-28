"""
═══════════════════════════════════════════════════════════════════
LESSON 2.5 CHEATSHEET: Loops & Iteration
═══════════════════════════════════════════════════════════════════

Quick reference for loop patterns in AI systems.
Keep this open while coding!

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. FOR LOOP (Process each item)
# ═══════════════════════════════════════════════════════════

for item in collection:
    # Runs for each item
    process(item)

# Example:
tools = ["search", "summarize", "translate"]
for tool in tools:
    print(f"Loading {tool}...")


# ═══════════════════════════════════════════════════════════
# 2. LOOP VARIABLE (Holds current item)
# ═══════════════════════════════════════════════════════════

scores = [0.95, 0.88, 0.92]
for score in scores:  # 'score' holds one value at a time
    print(score)


# ═══════════════════════════════════════════════════════════
# 3. WHILE LOOP (Condition-based)
# ═══════════════════════════════════════════════════════════

while condition:
    # Keeps running while True
    do_something()

# Example:
tokens = 0
while tokens < 100:
    tokens += 25
    print(f"Generated {tokens}")


# ═══════════════════════════════════════════════════════════
# 4. BREAK (Exit loop early)
# ═══════════════════════════════════════════════════════════

for item in items:
    if found_what_we_need(item):
        break  # Stop loop immediately

# Example:
for response in responses:
    if response["confidence"] > 0.90:
        best = response
        break  # Found it, stop searching


# ═══════════════════════════════════════════════════════════
# 5. CONTINUE (Skip current item)
# ═══════════════════════════════════════════════════════════

for item in items:
    if should_skip(item):
        continue  # Skip to next item
    process(item)

# Example:
for result in results:
    if result["score"] < 0.70:
        continue  # Skip low scores
    use_result(result)


# ═══════════════════════════════════════════════════════════
# 6. ENUMERATE (Get position + item)
# ═══════════════════════════════════════════════════════════

for index, item in enumerate(collection):
    # index = position (0, 1, 2...)
    # item = actual value
    print(f"{index}: {item}")

# Example:
tools = ["search", "summarize"]
for i, tool in enumerate(tools):
    print(f"Tool {i + 1}: {tool}")


# ═══════════════════════════════════════════════════════════
# 7. NESTED LOOPS (Loop inside loop)
# ═══════════════════════════════════════════════════════════

for outer_item in outer_list:
    for inner_item in inner_list:
        process(outer_item, inner_item)

# Example:
conversations = [
    ["User: Hi", "Agent: Hello"],
    ["User: Bye", "Agent: Goodbye"]
]
for conversation in conversations:
    for message in conversation:
        print(message)


# ═══════════════════════════════════════════════════════════
# 8. COMMON AI PATTERNS
# ═══════════════════════════════════════════════════════════

# Pattern: Filter (keep matching items)
filtered = []
for item in items:
    if item["score"] > 0.80:
        filtered.append(item)

# Pattern: Sum/Count
total = 0
for item in items:
    total += item["value"]

# Pattern: Extract field
names = []
for item in items:
    names.append(item["name"])

# Pattern: Find first match
result = None
for item in items:
    if matches(item):
        result = item
        break

# Pattern: Transform
transformed = []
for item in items:
    new_item = convert(item)
    transformed.append(new_item)

# Pattern: Group by category
by_category = {}
for item in items:
    category = item["category"]
    if category not in by_category:
        by_category[category] = []
    by_category[category].append(item)


# ═══════════════════════════════════════════════════════════
# 9. INDENTATION RULES
# ═══════════════════════════════════════════════════════════

# ✓ CORRECT:
for item in items:
    action1()  # 4 spaces
    action2()  # 4 spaces
done()         # No indent - always runs

# ✗ WRONG:
for item in items:
action1()  # No indent - ERROR!


# ═══════════════════════════════════════════════════════════
# 10. LIST COMPREHENSION (Shorthand)
# ═══════════════════════════════════════════════════════════

# Instead of:
filtered = []
for item in items:
    if item["score"] > 0.80:
        filtered.append(item)

# You can write:
filtered = [item for item in items if item["score"] > 0.80]

# Extract field:
names = [item["name"] for item in items]

# Transform:
doubled = [x * 2 for x in numbers]


# ═══════════════════════════════════════════════════════════
# 11. LOOP WITH ACCUMULATOR
# ═══════════════════════════════════════════════════════════

# Running total
total = 0
for value in values:
    total += value

# Running list
results = []
for item in items:
    results.append(process(item))

# Multiple accumulators
total_cost = 0
total_tokens = 0
for call in llm_calls:
    total_cost += call["cost"]
    total_tokens += call["tokens"]


# ═══════════════════════════════════════════════════════════
# 12. WHEN TO USE WHAT
# ═══════════════════════════════════════════════════════════

"""
Use FOR when:
✓ Processing known collection
✓ "Do this for each item"
✓ Filtering, counting, transforming

Use WHILE when:
✓ Don't know how many iterations
✓ "Keep going until..."
✓ Waiting for condition

Use BREAK when:
✓ Found what you need
✓ Error encountered
✓ Limit reached

Use CONTINUE when:
✓ Skip unwanted items
✓ Filter within loop
✓ Ignore errors

Use ENUMERATE when:
✓ Need position/rank
✓ Numbered output
✓ Index required
"""


# ═══════════════════════════════════════════════════════════
# 13. LOOP PERFORMANCE TIPS
# ═══════════════════════════════════════════════════════════

# ✓ GOOD: Exit early when possible
for item in large_list:
    if found_match(item):
        result = item
        break  # Don't process rest

# ✗ AVOID: Unnecessary work
for item in large_list:
    if found_match(item):
        result = item
    # Keeps looping unnecessarily!

# ✓ GOOD: Filter first if checking all items
filtered = [x for x in items if x["score"] > 0.80]
for item in filtered:
    expensive_process(item)

# ✗ AVOID: Check condition inside loop repeatedly
for item in items:
    if item["score"] > 0.80:  # Checking every time
        expensive_process(item)


# ═══════════════════════════════════════════════════════════
# 14. COMMON MISTAKES TO AVOID
# ═══════════════════════════════════════════════════════════

# ✗ WRONG: Modifying list while looping
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # Causes issues!

# ✓ CORRECT: Create new list
items = [1, 2, 3, 4, 5]
odd_items = [item for item in items if item % 2 != 0]

# ✗ WRONG: Infinite while loop
# while True:
#     process()  # Never stops!

# ✓ CORRECT: Include exit condition
count = 0
while count < 10:
    process()
    count += 1


# ═══════════════════════════════════════════════════════════
# 15. DEBUGGING TIPS
# ═══════════════════════════════════════════════════════════

# Print loop progress
for i, item in enumerate(items):
    print(f"Processing item {i + 1}/{len(items)}")
    process(item)

# Track what's happening
filtered = []
for item in items:
    if item["score"] > 0.80:
        filtered.append(item)
        print(f"Kept: {item['name']}")  # See what's kept
    else:
        print(f"Skipped: {item['name']}")  # See what's skipped

# Verify loop runs
print(f"Starting loop with {len(items)} items")
for item in items:
    process(item)
print(f"Loop completed")


# ═══════════════════════════════════════════════════════════
# 16. TEMPLATE QUICK LINKS
# ═══════════════════════════════════════════════════════════

"""
Available templates in this folder:
- template_filter_collection.py    → Keep matching items
- template_count_sum.py             → Total values
- template_find_first.py            → First match
- template_extract_fields.py        → Pull specific field
- template_transform.py             → Convert format
- template_enumerate.py             → Numbered processing
- template_nested_loop.py           → Multi-level data
"""


# ═══════════════════════════════════════════════════════════
# 17. REAL AI EXAMPLES
# ═══════════════════════════════════════════════════════════

# Filter RAG results
high_quality = [doc for doc in docs if doc["score"] > 0.80]

# Count tokens
total_tokens = sum(msg["tokens"] for msg in conversation)

# Extract sources
sources = [doc["source"] for doc in documents]

# Find best answer
best = None
for response in responses:
    if response["confidence"] > 0.90:
        best = response
        break

# Build citation list
for i, doc in enumerate(retrieved_docs, 1):
    print(f"[{i}] {doc['source']}: {doc['title']}")


# ═══════════════════════════════════════════════════════════
# 18. QUICK DECISION TREE
# ═══════════════════════════════════════════════════════════

"""
Need to:
├─ Process all items? → for loop
├─ Keep some items? → for + if + append
├─ Sum/count? → for + accumulator
├─ Find first match? → for + if + break
├─ Skip some items? → for + if + continue
├─ Need position? → for + enumerate
├─ Don't know iterations? → while loop
└─ Multi-level data? → nested for loops
"""


# ═══════════════════════════════════════════════════════════
# END OF CHEATSHEET
# ═══════════════════════════════════════════════════════════

print("Keep this cheatsheet open while coding!")
print("Copy patterns as needed - don't memorize!")
