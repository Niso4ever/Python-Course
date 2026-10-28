# Lesson 04: Loops & Iteration
## The Assembly Line Theory

Architect, you know how to store collections (L1.5 lists). Now you need to **process each item** one by one.

In AI systems, you constantly:
- Process **every retrieved document**
- Check **every message** in conversation history
- Filter **every search result**
- Apply scoring to **every RAG chunk**

This is where **loops** come in — the assembly line that processes collections.

---

## 1. The For Loop (The Conveyor Belt)

Process each item from a collection, one at a time.

```python
tools = ["search", "summarize", "translate"]

for tool in tools:
    print(f"Loading {tool} module...")
```

**Output:**
```
Loading search module...
Loading summarize module...
Loading translate module...
```

| Symbol | Role |
|:-------|:-----|
| `for` | Start the loop |
| `tool` | Variable holding current item |
| `in` | "From this collection" |
| `tools` | The list you're looping through |
| `:` | Start loop body (like if statements) |

**Pattern:** Indentation shows what's inside the loop.

---

## 2. The Loop Variable (Current Item)

The loop variable is like a **spotlight** on one item at a time.

```python
scores = [0.95, 0.88, 0.92, 0.85]

for score in scores:
    print(f"Current score: {score}")
```

**Output:**
```
Current score: 0.95
Current score: 0.88
Current score: 0.92
Current score: 0.85
```

**What happens:**
- Iteration 1: `score` = 0.95
- Iteration 2: `score` = 0.88
- Iteration 3: `score` = 0.92
- Iteration 4: `score` = 0.85

---

## 3. Real AI Example: Filter Search Results

RAG systems retrieve documents and filter by relevance.

```python
search_results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "Blog", "score": 0.72},
    {"source": "ArXiv", "score": 0.88},
    {"source": "Forum", "score": 0.65}
]

# Keep only high-quality results
high_quality = []

for result in search_results:
    if result["score"] > 0.80:
        high_quality.append(result)
        print(f"✓ Keeping {result['source']} (score: {result['score']})")
    else:
        print(f"✗ Filtering {result['source']} (score: {result['score']})")

print(f"\nFinal: {len(high_quality)} high-quality results")
```

**Output:**
```
✓ Keeping Wikipedia (score: 0.95)
✗ Filtering Blog (score: 0.72)
✓ Keeping ArXiv (score: 0.88)
✗ Filtering Forum (score: 0.65)

Final: 2 high-quality results
```

**Pattern:** Loop + if statement = filtering

---

## 4. The While Loop (Condition-Based)

Keeps running while a condition is True.

```python
token_count = 0
max_tokens = 4096

while token_count < max_tokens:
    print(f"Generating token {token_count}...")
    token_count += 500

print("Token limit reached!")
```

**Output:**
```
Generating token 0...
Generating token 500...
...
Generating token 3500...
Generating token 4000...
Token limit reached!
```

### When to Use Which?

| Use `for` when... | Use `while` when... |
|:------------------|:--------------------|
| Processing a known list | Don't know when to stop |
| "For each item..." | "Keep going until..." |
| Count is fixed | Condition-based |

---

## 5. Loop Control (Break & Continue)

### Break: Stop Early

```python
sources = ["Wikipedia", "ArXiv", "Broken Link", "GitHub"]

for source in sources:
    if source == "Broken Link":
        print(f"Error: {source}. Stopping search.")
        break  # Exit loop immediately
    print(f"Searching {source}...")
```

**Output:**
```
Searching Wikipedia...
Searching ArXiv...
Error: Broken Link. Stopping search.
```

### Continue: Skip Current Item

```python
scores = [0.95, 0.72, 0.88, 0.65, 0.92]

for score in scores:
    if score < 0.80:
        continue  # Skip to next item
    print(f"High-quality: {score}")
```

**Output:**
```
High-quality: 0.95
High-quality: 0.88
High-quality: 0.92
```

**Pattern:** `break` = exit loop, `continue` = skip item

---

## 6. Enumerate (Get Position + Item)

Need to know **which position** you're at?

```python
tools = ["search", "summarize", "translate"]

for index, tool in enumerate(tools):
    print(f"Tool {index}: {tool}")
```

**Output:**
```
Tool 0: search
Tool 1: summarize
Tool 2: translate
```

**Use enumerate when:**
- Displaying numbered lists
- Need position for indexing
- Tracking progress

---

## 7. Nested Loops (Loop Inside Loop)

Process multi-level data (list of lists).

```python
conversations = [
    ["User: Hello", "Agent: Hi!"],
    ["User: What is AI?", "Agent: AI is..."],
    ["User: Thanks", "Agent: Welcome!"]
]

for conv_num, conversation in enumerate(conversations):
    print(f"\n--- Conversation {conv_num + 1} ---")
    for message in conversation:
        print(message)
```

**Output:**
```
--- Conversation 1 ---
User: Hello
Agent: Hi!

--- Conversation 2 ---
User: What is AI?
Agent: AI is...

--- Conversation 3 ---
User: Thanks
Agent: Welcome!
```

**Pattern:** Outer loop for conversations, inner loop for messages

---

## 8. Common AI Loop Patterns

### Pattern 1: Collect Results
```python
results = []
for item in source_list:
    results.append(process(item))
```

### Pattern 2: Filter Collection
```python
filtered = []
for item in items:
    if meets_criteria(item):
        filtered.append(item)
```

### Pattern 3: Transform Data
```python
transformed = []
for item in items:
    transformed.append(transform(item))
```

### Pattern 4: Find First Match
```python
for item in items:
    if matches(item):
        result = item
        break
```

### Pattern 5: Count/Sum
```python
total = 0
for item in items:
    total += item["value"]
```

---

## 9. Real-World Examples

### Example 1: Token Counting
```python
messages = [
    {"content": "Hello", "tokens": 5},
    {"content": "How are you?", "tokens": 8},
    {"content": "Goodbye", "tokens": 6}
]

total_tokens = 0
for message in messages:
    total_tokens += message["tokens"]

print(f"Total tokens: {total_tokens}")
# Output: Total tokens: 19
```

### Example 2: Extract High-Confidence Answers
```python
llm_responses = [
    {"answer": "RAG is...", "confidence": 0.95},
    {"answer": "It combines...", "confidence": 0.72},
    {"answer": "The process...", "confidence": 0.88}
]

for response in llm_responses:
    if response["confidence"] > 0.85:
        print(f"✓ {response['answer']} (conf: {response['confidence']})")
```

### Example 3: Build Conversation Context
```python
conversation = []
user_inputs = ["Hi", "What is AI?", "Thanks"]

for user_input in user_inputs:
    conversation.append({"role": "user", "content": user_input})
    # In real code: get LLM response here
    conversation.append({"role": "assistant", "content": "Response..."})

print(f"Conversation has {len(conversation)} messages")
```

---

## 10. Pattern Recognition Guide

**When you see:**
```python
for item in collection:
    # code
```
**Translation:** "Do this for each item in the collection"

**When you see:**
```python
for item in collection:
    if condition:
        results.append(item)
```
**Translation:** "Filter collection - keep items matching condition"

**When you see:**
```python
for item in collection:
    if condition:
        break
```
**Translation:** "Find first match and stop"

---

## 11. Key Takeaways

✓ **For loops** process known collections
✓ **While loops** run until condition is False
✓ **Break** exits loop early
✓ **Continue** skips current item
✓ **Enumerate** gives position + item
✓ **Nested loops** handle multi-level data

**Most common AI use:**
- Filter RAG results by score
- Process conversation history
- Count tokens across messages
- Transform data formats
- Find matching items

---

## 12. Templates Available

See this lesson folder ([./](./)) for ready-to-use loop patterns: `template_count_sum.py`, `template_filter_collection.py`, `template_find_first.py`.

**Your workflow:**
1. Identify your processing need
2. Find matching template
3. Copy and modify
4. Use in your system

---

## 13. Next Steps

**Immediate:**
1. Review the `template_*.py` files in this lesson folder
2. Recognize loop patterns in real AI code
3. Understand: Most AI code is just looping through lists of dicts

**Coming up:**
- **Lesson 05:** Functions - Package logic into reusable tools
- **Lesson 06:** Classes - Build agent modules

---

**Remember:** You're not memorizing loop syntax. You're recognizing: "Oh, this filters search results" or "This counts tokens." The template handles the rest.
