# Lesson 04 - Pass 1: RECOGNITION
## Learn to SEE Loops in AI Code

**Goal:** By the end of this pass, you'll instantly recognize loop patterns and understand what they do WITHOUT writing any code.

---

## The Shape Recognition Method

Loops have distinctive VISUAL SHAPES. Learn to recognize them by sight.

### Shape 1: The For Loop

```python
for item in collection:
    ← INDENT (do something with item)
```

**Visual Pattern:**
- `for` keyword
- Loop variable (`item`)
- `in` keyword
- Collection (`list`)
- Colon `:`
- Indented body

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Filter RAG Results

```python
# RAG system - keep high-quality documents
search_results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "Blog", "score": 0.72},
    {"source": "ArXiv", "score": 0.88}
]

high_quality = []

for result in search_results:
    if result["score"] > 0.80:
        high_quality.append(result)
```

**RECOGNIZE THIS:**
- Line 8: `for result in search_results:` ← Loop through list
- Line 9-10: Indented ← Runs for each item
- Pattern: Loop + if = filtering

**What it does:** "Check each result. Keep those with score > 0.80."

---

### Example 2: Count Total Tokens

```python
# Count tokens across conversation
messages = [
    {"role": "user", "content": "Hello", "tokens": 5},
    {"role": "assistant", "content": "Hi!", "tokens": 3},
    {"role": "user", "content": "Bye", "tokens": 4}
]

total_tokens = 0

for message in messages:
    total_tokens += message["tokens"]

print(f"Total: {total_tokens}")  # 12
```

**RECOGNIZE THIS:**
- Line 10: Loop through messages
- Line 11: Add each message's tokens to total
- Pattern: Loop + accumulate = sum

**What it does:** "Add up all token counts."

---

### Example 3: Build Citation List

```python
# Extract sources from RAG results
documents = [
    {"text": "...", "source": "Wikipedia"},
    {"text": "...", "source": "ArXiv"},
    {"text": "...", "source": "Blog"}
]

sources = []

for doc in documents:
    sources.append(doc["source"])

print(sources)  # ["Wikipedia", "ArXiv", "Blog"]
```

**RECOGNIZE THIS:**
- Loop through documents
- Extract one field (source)
- Build new list

**Pattern:** Loop + extract = collect specific fields

**What it does:** "Get all sources from documents."

---

### Example 4: Find First Match

```python
# Find first high-confidence answer
responses = [
    {"answer": "Maybe...", "confidence": 0.65},
    {"answer": "Probably...", "confidence": 0.88},
    {"answer": "Definitely...", "confidence": 0.95}
]

for response in responses:
    if response["confidence"] > 0.90:
        best_answer = response["answer"]
        break  # Stop when found

print(best_answer)  # "Definitely..."
```

**RECOGNIZE THIS:**
- Loop through responses
- `if` checks condition
- `break` stops loop early

**Pattern:** Loop + if + break = find first match

**What it does:** "Find first response with confidence > 0.90, then stop."

---

### Example 5: Process Conversation History

```python
# Add context markers to conversation
conversation = [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello!"},
    {"role": "user", "content": "Help me"}
]

for i, message in enumerate(conversation):
    print(f"Message {i}: [{message['role']}] {message['content']}")
```

**Output:**
```
Message 0: [user] Hi
Message 1: [assistant] Hello!
Message 2: [user] Help me
```

**RECOGNIZE THIS:**
- `enumerate(conversation)` gives both index and item
- `i` = position, `message` = item
- Pattern: enumerate = numbered processing

**What it does:** "Display each message with its number."

---

### Example 6: Skip Low-Quality Items

```python
# Process only high-quality sources
sources = [
    {"name": "internal_kb", "trust": 0.95},
    {"name": "random_blog", "trust": 0.45},
    {"name": "arxiv", "trust": 0.88}
]

for source in sources:
    if source["trust"] < 0.70:
        continue  # Skip this one
    print(f"Using {source['name']}")
```

**Output:**
```
Using internal_kb
Using arxiv
```

**RECOGNIZE THIS:**
- `continue` skips current item
- Rest of loop continues with next item
- Pattern: continue = skip unwanted items

**What it does:** "Process only sources with trust >= 0.70."

---

### Example 7: Nested Loop (Messages in Conversations)

```python
# Process multiple conversations
all_conversations = [
    [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"}
    ],
    [
        {"role": "user", "content": "Bye"},
        {"role": "assistant", "content": "Goodbye!"}
    ]
]

for conv_num, conversation in enumerate(all_conversations):
    print(f"Conversation {conv_num + 1}:")
    for message in conversation:
        print(f"  {message['role']}: {message['content']}")
```

**RECOGNIZE THIS:**
- Outer loop: Through conversations
- Inner loop: Through messages in each conversation
- TWO levels of indentation

**Visual Pattern:**
```
for outer_item in outer_list:
    ← INDENT LEVEL 1
    for inner_item in inner_list:
        ← INDENT LEVEL 2
```

**What it does:** "For each conversation, process each message inside it."

---

### Example 8: While Loop (Token Limit)

```python
# Generate until token limit
current_tokens = 0
max_tokens = 100

while current_tokens < max_tokens:
    current_tokens += 25
    print(f"Generated {current_tokens} tokens")

print("Limit reached!")
```

**RECOGNIZE THIS:**
- `while condition:` ← Keep going while True
- Condition checked each iteration
- Must have way to become False

**Pattern:** while = condition-based loop

**What it does:** "Keep generating tokens until we reach 100."

---

## Loop Control Keywords

RECOGNIZE these symbols:

| Keyword | Meaning | Example Use |
|:--------|:--------|:------------|
| `for` | Start loop | `for item in list:` |
| `in` | From collection | `for x in items:` |
| `while` | Loop while condition | `while count < 10:` |
| `break` | Exit loop immediately | Stop when found |
| `continue` | Skip to next item | Skip low-quality |
| `enumerate()` | Get index + item | Numbered lists |

---

## Recognition Exercise: Read These Code Blocks

### Block 1
```python
tools = ["search", "summarize", "translate"]

for tool in tools:
    print(f"Loading {tool}...")
```

**Questions:**
1. What's being looped? → List of tools
2. What's the loop variable? → `tool`
3. How many times does it run? → 3 times (one per tool)

---

### Block 2
```python
scores = [0.95, 0.72, 0.88, 0.65, 0.92]
count = 0

for score in scores:
    if score > 0.80:
        count += 1
```

**Questions:**
1. What's being counted? → Scores over 0.80
2. Final count value? → 3 (0.95, 0.88, 0.92)
3. Pattern? → Loop + if + count

---

### Block 3
```python
for doc in documents:
    if doc["score"] < 0.70:
        continue
    process(doc)
```

**Questions:**
1. What does `continue` do? → Skips low-score docs
2. What gets processed? → Only docs with score >= 0.70
3. Pattern? → Filter with continue

---

## Common AI Patterns (Recognition Cheat Sheet)

### Pattern: Filter Collection
```python
filtered = []
for item in items:
    if condition:
        filtered.append(item)
```
**Recognize:** Building new list with matching items

---

### Pattern: Sum/Count
```python
total = 0
for item in items:
    total += item["value"]
```
**Recognize:** Accumulating values

---

### Pattern: Extract Fields
```python
names = []
for item in items:
    names.append(item["name"])
```
**Recognize:** Pulling one field from each item

---

### Pattern: Find First
```python
for item in items:
    if matches(item):
        result = item
        break
```
**Recognize:** Stop at first match

---

### Pattern: Transform
```python
transformed = []
for item in items:
    transformed.append(modify(item))
```
**Recognize:** Convert each item

---

## Final Recognition Test

Look at this real RAG code and identify the pattern:

```python
retrieved_docs = search_vector_db(query, top_k=10)

filtered_docs = []
total_score = 0

for doc in retrieved_docs:
    if doc["score"] < 0.70:
        continue

    filtered_docs.append(doc)
    total_score += doc["score"]

    if len(filtered_docs) >= 3:
        break

average_score = total_score / len(filtered_docs)
```

**RECOGNIZE:**
1. Loop through? → retrieved_docs
2. Line 6-7: What pattern? → Skip low scores (continue)
3. Line 9: What pattern? → Collect filtered docs
4. Line 10: What pattern? → Sum scores
5. Line 12-13: What pattern? → Stop at 3 docs (break)
6. Overall purpose? → Get top 3 high-quality docs with average score

**This is:** Filter + collect + sum + limit

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** for/while loops by sight
✓ **Identify** loop variables and collections
✓ **Spot** break/continue patterns
✓ **Understand** what loops do without running them
✓ **See** common AI patterns (filter, sum, extract, find)

**Next:**
- **Pass C (Visual):** See loops as flowcharts and assembly lines
- **Pass 3 (Templates):** Copy and modify loop patterns

**Remember:** You're not memorizing loop syntax. You're training your eyes to SEE patterns. When you read AI code, you'll think: "Oh, that's filtering RAG results" or "That's counting tokens."

---

## Pro Tip: The 3-Second Rule

When you see unfamiliar code with loops:
1. **Second 1:** Identify what's being looped (list of what?)
2. **Second 2:** See what happens to each item (filter? count? extract?)
3. **Second 3:** Understand the purpose (why are we doing this?)

That's it. You don't need to trace every iteration. Just recognize the pattern.
