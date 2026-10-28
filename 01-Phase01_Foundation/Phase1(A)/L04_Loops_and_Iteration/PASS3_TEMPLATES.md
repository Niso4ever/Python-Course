# Lesson 04 - Pass 3: TEMPLATES
## Your Copy-Paste Loop Library

**Goal:** Build your reference library of loop patterns. Copy, modify, use.

**Note (checked 2026-10-28):** 3 of the 12 templates on this page are saved as `.py` files in this folder (`template_filter_collection.py`, `template_count_sum.py`, `template_find_first.py`). The other 9 exist only as the code blocks below; copy them from this page.

---

## How to Use These Templates

1. **Identify** your processing need
2. **Find** the matching template below
3. **Copy** the code
4. **Modify** the values/logic
5. **Use** in your AI system

**You're not writing loops from scratch. You're customizing proven patterns.**

---

## Template Library

### Template 1: Filter Collection

**Use when:** Need to keep only items matching criteria

**File:** `template_filter_collection.py`

```python
# Keep only high-quality results
results = [...]  # Your list of dicts

filtered = []

for item in results:
    if item["score"] > 0.80:  # ← MODIFY: Your condition
        filtered.append(item)

# Use filtered list
```

**Common AI uses:**
- Filter RAG results by relevance score
- Keep high-confidence LLM responses
- Select trusted sources

---

### Template 2: Count/Sum Values

**Use when:** Need total across collection

**File:** `template_count_sum.py`

```python
# Count total tokens
messages = [...]  # Your list of dicts

total_tokens = 0

for message in messages:
    total_tokens += message["tokens"]  # ← MODIFY: Your field

print(f"Total: {total_tokens}")
```

**Common AI uses:**
- Count tokens in conversation
- Sum API costs
- Calculate average scores

---

### Template 3: Extract Specific Fields

**Use when:** Pull one field from each item

**File:** `template_extract_fields.py`

```python
# Extract all sources
documents = [...]  # Your list of dicts

sources = []

for doc in documents:
    sources.append(doc["source"])  # ← MODIFY: Your field

# sources now has list of all sources
```

**Common AI uses:**
- Get all sources from RAG results
- Extract all user messages from conversation
- Collect all tool names

---

### Template 4: Find First Match

**Use when:** Need first item matching condition

**File:** `template_find_first.py`

```python
# Find first high-confidence answer
responses = [...]  # Your list

result = None

for response in responses:
    if response["confidence"] > 0.90:  # ← MODIFY: Your condition
        result = response
        break  # Stop when found

if result:
    print(f"Found: {result}")
else:
    print("No match found")
```

**Common AI uses:**
- Find best RAG result
- Get first available tool
- Locate specific message in history

---

### Template 5: Transform/Map Collection

**Use when:** Convert each item to new format

**File:** `template_transform.py`

```python
# Convert to different format
raw_data = [...]  # Your list

transformed = []

for item in raw_data:
    # Transform each item
    new_item = {
        "text": item["content"],  # ← MODIFY: Your mapping
        "score": item["relevance"],
        "id": item["doc_id"]
    }
    transformed.append(new_item)

# transformed has new format
```

**Common AI uses:**
- Convert RAG results to LLM format
- Reformat conversation for different API
- Transform metadata structure

---

### Template 6: Filter with Continue

**Use when:** Skip unwanted items, process rest

**File:** `template_filter_continue.py`

```python
# Process only high-quality sources
sources = [...]  # Your list

for source in sources:
    # Skip low-quality
    if source["trust"] < 0.70:  # ← MODIFY: Your skip condition
        continue

    # Process this source
    process(source)
```

**Common AI uses:**
- Skip low-trust sources
- Ignore failed API calls
- Filter out errors

---

### Template 7: Enumerate (Numbered Processing)

**Use when:** Need position/index with item

**File:** `template_enumerate.py`

```python
# Display numbered list
items = [...]  # Your list

for index, item in enumerate(items):
    print(f"{index + 1}. {item['name']}")  # ← MODIFY: Your format

# Or use index for other purposes
for i, result in enumerate(search_results):
    result["rank"] = i + 1
```

**Common AI uses:**
- Display numbered search results
- Rank RAG documents
- Track processing progress

---

### Template 8: Nested Loop (Multi-Level)

**Use when:** Processing list of lists

**File:** `template_nested_loop.py`

```python
# Process multiple conversations
all_conversations = [...]  # List of lists

for conv_num, conversation in enumerate(all_conversations):
    print(f"Conversation {conv_num + 1}:")

    for message in conversation:
        print(f"  {message['role']}: {message['content']}")
```

**Common AI uses:**
- Process multiple chat sessions
- Handle batched results
- Multi-level data structures

---

### Template 9: Accumulate with Condition

**Use when:** Sum/count with filtering

**File:** `template_accumulate_conditional.py`

```python
# Count tokens for high-confidence messages only
messages = [...]  # Your list

total_tokens = 0
count = 0

for message in messages:
    if message["confidence"] > 0.85:  # ← MODIFY: Your condition
        total_tokens += message["tokens"]
        count += 1

if count > 0:
    average = total_tokens / count
    print(f"Average tokens: {average}")
```

**Common AI uses:**
- Calculate average for filtered items
- Sum costs for specific model
- Count successful calls only

---

### Template 10: Build New Structure

**Use when:** Create complex output from list

**File:** `template_build_structure.py`

```python
# Group by source
results = [...]  # Your list

by_source = {}

for result in results:
    source = result["source"]  # ← MODIFY: Grouping key

    if source not in by_source:
        by_source[source] = []

    by_source[source].append(result)

# by_source is now: {"Wikipedia": [...], "ArXiv": [...]}
```

**Common AI uses:**
- Group RAG results by source
- Organize by confidence level
- Categorize responses

---

### Template 11: While Loop (Condition-Based)

**Use when:** Don't know iterations needed

**File:** `template_while_loop.py`

```python
# Keep generating until limit
current_tokens = 0
max_tokens = 4096  # ← MODIFY: Your limit

while current_tokens < max_tokens:
    # Generate more
    new_tokens = generate_chunk()  # ← MODIFY: Your process
    current_tokens += new_tokens

    print(f"Progress: {current_tokens}/{max_tokens}")

    # Safety: prevent infinite loop
    if current_tokens > max_tokens * 1.5:
        print("Safety limit reached")
        break
```

**Common AI uses:**
- Token generation loops
- Retry until success
- Wait for condition

---

### Template 12: Early Exit on Budget

**Use when:** Stop when limit reached

**File:** `template_early_exit_budget.py`

```python
# Process until budget exhausted
llm_calls = [...]  # Your list

total_cost = 0.0
max_budget = 10.00  # ← MODIFY: Your budget

processed = []

for call in llm_calls:
    cost = calculate_cost(call)  # ← MODIFY: Your cost function

    if total_cost + cost > max_budget:
        print(f"Budget limit reached: ${total_cost:.2f}")
        break

    # Process this call
    result = execute(call)
    processed.append(result)
    total_cost += cost

print(f"Processed {len(processed)} calls, spent ${total_cost:.2f}")
```

**Common AI uses:**
- Budget limits for API calls
- Token limits
- Rate limiting

---

## Quick Selection Guide

| Need | Template | File |
|:-----|:---------|:-----|
| Keep items matching criteria | Template 1 | filter_collection.py |
| Sum/count values | Template 2 | count_sum.py |
| Extract one field from all items | Template 3 | extract_fields.py |
| Find first match | Template 4 | find_first.py |
| Convert format | Template 5 | transform.py |
| Skip unwanted, process rest | Template 6 | filter_continue.py |
| Need position + item | Template 7 | enumerate.py |
| List of lists | Template 8 | nested_loop.py |
| Sum with filter | Template 9 | accumulate_conditional.py |
| Group/categorize | Template 10 | build_structure.py |
| Don't know iterations | Template 11 | while_loop.py |
| Stop at limit | Template 12 | early_exit_budget.py |

---

## Your Workflow

1. **Identify** what you need (filter? count? find?)
2. **Pick** the matching template
3. **Copy** the entire code
4. **Modify** the marked sections (← MODIFY comments)
5. **Test** with your data
6. **Use** in your AI system

---

## Common Combinations

### Filter + Count
```python
filtered = []
count = 0
for item in items:
    if item["score"] > 0.80:
        filtered.append(item)
        count += 1
```

### Find + Transform
```python
for item in items:
    if matches(item):
        result = transform(item)
        break
```

### Enumerate + Filter
```python
for i, item in enumerate(items):
    if item["quality"] > threshold:
        print(f"Rank {i + 1}: {item['name']}")
```

---

## You've Completed Pass 3!

You now have:
✓ **12 production-ready loop templates**
✓ **Copy-paste patterns for common AI tasks**
✓ **Modification guides** for each template
✓ **Quick selection guide**

**Remember:** You're not writing loops from scratch. You're customizing proven patterns that professional AI systems use every day.

---

## Next Steps

1. Pick one template that matches your current need
2. Copy it to your project
3. Modify the marked sections
4. See it work

Then move to **Lesson 05: Functions** to package your logic into reusable tools!
