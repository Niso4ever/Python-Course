# Lesson 04 - Pass C: VISUAL PATTERNS
## See Loops as Assembly Lines and Flowcharts

**Goal:** Understand loop logic through visual diagrams, not just code.

---

## Visual 1: Simple For Loop (The Conveyor Belt)

### Code:
```python
tools = ["search", "summarize", "translate"]

for tool in tools:
    print(f"Loading {tool}...")
```

### Visual Assembly Line:
```
INPUT LIST: ["search", "summarize", "translate"]
     |
     ↓
┌─────────────────────────────────────────┐
│     CONVEYOR BELT (for loop)            │
│                                         │
│   Item 1: "search"     →  print()      │
│   Item 2: "summarize"  →  print()      │
│   Item 3: "translate"  →  print()      │
│                                         │
└─────────────────────────────────────────┘
     |
     ↓
   DONE
```

**Pattern:** Each item goes through same process

---

## Visual 2: Filter Loop (Quality Control)

### Code:
```python
results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "Blog", "score": 0.72},
    {"source": "ArXiv", "score": 0.88}
]

filtered = []
for result in results:
    if result["score"] > 0.80:
        filtered.append(result)
```

### Visual Flowchart:
```
        START: results list
              |
              ↓
        ┌──────────┐
        │ For each │
        │  result  │
        └──────────┘
              |
              ↓
        ┌─────────────┐
        │ Score > 80? │
        └─────────────┘
           /        \
         YES         NO
         /             \
        ↓               ↓
   ┌─────────┐    ┌─────────┐
   │  KEEP   │    │  SKIP   │
   │ (append)│    │         │
   └─────────┘    └─────────┘
        \             /
         \           /
          ↓         ↓
      More items?
          |
         NO
          ↓
     filtered list
```

**Pattern:** Assembly line with quality inspection

---

## Visual 3: Accumulator Pattern (Counting/Summing)

### Code:
```python
messages = [
    {"content": "Hi", "tokens": 5},
    {"content": "Hello", "tokens": 8},
    {"content": "Bye", "tokens": 4}
]

total = 0
for msg in messages:
    total += msg["tokens"]
```

### Visual Accumulator:
```
┌─────────────────────────────────┐
│  ACCUMULATOR (total = 0)        │
└─────────────────────────────────┘
              |
              ↓
   ┌──────────────────────┐
   │ Message 1: +5 tokens │
   │ total = 0 + 5 = 5    │
   └──────────────────────┘
              |
              ↓
   ┌──────────────────────┐
   │ Message 2: +8 tokens │
   │ total = 5 + 8 = 13   │
   └──────────────────────┘
              |
              ↓
   ┌──────────────────────┐
   │ Message 3: +4 tokens │
   │ total = 13 + 4 = 17  │
   └──────────────────────┘
              |
              ↓
        FINAL: 17
```

**Pattern:** Running total grows with each item

---

## Visual 4: Break Pattern (Early Exit)

### Code:
```python
responses = [
    {"answer": "Maybe", "conf": 0.65},
    {"answer": "Likely", "conf": 0.88},
    {"answer": "Certain", "conf": 0.95}
]

for response in responses:
    if response["conf"] > 0.90:
        best = response["answer"]
        break
```

### Visual Flowchart:
```
        START
          |
          ↓
    ┌──────────┐
    │ Check    │
    │ item 1   │
    └──────────┘
          |
          ↓
    ┌────────────┐
    │ conf > 90? │
    └────────────┘
       /      \
     NO        YES ──→ SAVE & EXIT ──→ DONE
     /                 (break)
    ↓
┌──────────┐
│ Check    │
│ item 2   │
└──────────┘
    |
    ↓
┌────────────┐
│ conf > 90? │
└────────────┘
   /      \
 NO        YES ──→ SAVE & EXIT ──→ DONE
 /                 (break)
↓
(continue...)
```

**Pattern:** Stop as soon as condition met

---

## Visual 5: Continue Pattern (Skip Items)

### Code:
```python
sources = [
    {"name": "KB", "trust": 0.95},
    {"name": "Blog", "trust": 0.45},
    {"name": "ArXiv", "trust": 0.88}
]

for source in sources:
    if source["trust"] < 0.70:
        continue
    process(source)
```

### Visual Assembly Line:
```
┌──────────────────────────────────────────┐
│         ASSEMBLY LINE                    │
│                                          │
│  Item 1: KB (0.95)                       │
│    ✓ trust >= 0.70  →  PROCESS          │
│                                          │
│  Item 2: Blog (0.45)                     │
│    ✗ trust < 0.70   →  SKIP (continue)  │
│                                          │
│  Item 3: ArXiv (0.88)                    │
│    ✓ trust >= 0.70  →  PROCESS          │
│                                          │
└──────────────────────────────────────────┘

PROCESSED: [KB, ArXiv]
SKIPPED: [Blog]
```

**Pattern:** Conveyor belt with rejection

---

## Visual 6: Enumerate Pattern (Numbered Processing)

### Code:
```python
tools = ["search", "summarize", "translate"]

for i, tool in enumerate(tools):
    print(f"Tool {i}: {tool}")
```

### Visual Numbered Line:
```
┌─────────────────────────────────────┐
│  POSITION  │  ITEM     │  OUTPUT    │
├────────────┼───────────┼────────────┤
│     0      │  search   │ Tool 0:... │
│     1      │ summarize │ Tool 1:... │
│     2      │ translate │ Tool 2:... │
└─────────────────────────────────────┘

enumerate() gives both:
   i (position)  +  tool (item)
```

**Pattern:** Numbered conveyor belt

---

## Visual 7: Nested Loop (Multi-Level Processing)

### Code:
```python
conversations = [
    [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello"}
    ],
    [
        {"role": "user", "content": "Bye"},
        {"role": "assistant", "content": "Goodbye"}
    ]
]

for conversation in conversations:
    for message in conversation:
        print(message)
```

### Visual Nested Structure:
```
┌─────────────────────────────────────────────┐
│  OUTER LOOP: Conversations                  │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Conversation 1                       │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │ INNER LOOP: Messages            │ │ │
│  │  │                                 │ │ │
│  │  │  Message 1: {user: "Hi"}       │ │ │
│  │  │  Message 2: {assistant: "..."}  │ │ │
│  │  └─────────────────────────────────┘ │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Conversation 2                       │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │ INNER LOOP: Messages            │ │ │
│  │  │                                 │ │ │
│  │  │  Message 1: {user: "Bye"}      │ │ │
│  │  │  Message 2: {assistant: "..."}  │ │ │
│  │  └─────────────────────────────────┘ │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Pattern:** Loop inside loop, process all combinations

---

## Visual 8: While Loop (Condition-Based)

### Code:
```python
tokens = 0
max_tokens = 100

while tokens < max_tokens:
    tokens += 25
    print(f"Generated {tokens}")
```

### Visual Flowchart:
```
        START
          |
    tokens = 0
          |
          ↓
    ┌──────────────┐
    │ tokens < 100?│ ←─────┐
    └──────────────┘       │
         /     \           │
       YES      NO         │
       /          \        │
      ↓            ↓       │
  ┌─────────┐   DONE      │
  │Add +25  │             │
  │Print    │             │
  └─────────┘             │
      |                   │
      └───────────────────┘
       (loop back)
```

**Key Difference from For:**
- For: "Do this N times"
- While: "Keep doing until condition False"

---

## Visual 9: Real RAG Pipeline

### Code:
```python
docs = search_vector_db(query, top_k=10)

high_quality = []
for doc in docs:
    if doc["score"] < 0.70:
        continue
    high_quality.append(doc)
    if len(high_quality) >= 3:
        break

context = combine(high_quality)
```

### Visual Pipeline:
```
┌──────────────────────────────────────────────┐
│  INPUT: 10 documents from vector DB          │
└──────────────────────────────────────────────┘
                    |
                    ↓
        ┌───────────────────────┐
        │  QUALITY FILTER       │
        │  (score >= 0.70)      │
        └───────────────────────┘
                    |
         ┌──────────┴──────────┐
         ↓                     ↓
    ✓ PASS                 ✗ SKIP
    (append)              (continue)
         |
         ↓
    ┌────────────┐
    │ Count = 3? │
    └────────────┘
         |
        YES ──→ STOP (break)
         |
        NO ──→ Continue loop
         |
         ↓
┌─────────────────────────┐
│ OUTPUT: 3 best docs     │
└─────────────────────────┘
         |
         ↓
    Combine into context
```

**Pattern:** Filter → Collect → Limit → Stop

---

## Shape Comparison Chart

### Simple Loop
```
  ┌─┐
  │ │ → process item
  │ │ → process item
  │ │ → process item
  └─┘
```
Each item gets same treatment

---

### Filter Loop
```
  ┌─┐
  │ │ → check → keep/skip
  │ │ → check → keep/skip
  │ │ → check → keep/skip
  └─┘
```
Decision for each item

---

### Accumulator
```
  total = 0
     |
  ┌─┐
  │ │ → +5  (total = 5)
  │ │ → +8  (total = 13)
  │ │ → +4  (total = 17)
  └─┘
```
Running total grows

---

### Break (Early Exit)
```
  ┌─┐
  │ │ → check → NO, continue
  │ │ → check → YES → EXIT
  └─┘
    (remaining items skipped)
```
Stop when found

---

### Nested Loop
```
  ┌─┐ Outer
  │ ├─┐ Inner
  │ │ │ → item
  │ │ │ → item
  │ └─┘
  │
  │ ├─┐ Inner
  │ │ │ → item
  │ │ │ → item
  │ └─┘
  └─┘
```
Loop within loop

---

## Color Coding Method (For Your Practice)

When reading loop code, mentally color it:

- **🔵 Blue** = Loop structure (for/while)
- **🟢 Green** = What happens to each item
- **🟡 Yellow** = Control flow (break/continue)
- **🟠 Orange** = Accumulators/counters

```python
🔵for result in search_results:
    🔵if result["score"] > 0.80:
        🟢filtered.append(result)
        🟠count += 1
        🔵if count >= 3:
            🟡break
```

---

## Visual Recognition Exercise

Look at this code and draw the shape in your mind:

```python
total_cost = 0

for call in llm_calls:
    if call["model"] == "claude-opus-5-5":
        cost = call["tokens"] * 0.015
    else:
        cost = call["tokens"] * 0.003

    total_cost += cost

    if total_cost > 100.00:
        print("Budget exceeded!")
        break
```

**Mental Image:**
```
Accumulator (total_cost)
    |
  Loop through calls
    |
  Check model type → Calculate cost
    |
  Add to total
    |
  Check budget → Break if exceeded
```

**Pattern:** Accumulate + condition check + early exit

---

## The Assembly Line Metaphor

### For Loop = Conveyor Belt
```
[Item] → [Item] → [Item] → [Item]
   ↓        ↓        ↓        ↓
 Process Process Process Process
```
Fixed number of items

---

### While Loop = Production Line
```
    Condition?
       YES → Process → Check again
       NO  → STOP
```
Runs until condition says stop

---

### Filter = Quality Control
```
[Item] → Check → ✓ PASS → Keep
[Item] → Check → ✗ FAIL → Discard
[Item] → Check → ✓ PASS → Keep
```

---

### Break = Emergency Stop
```
[Item] → Process
[Item] → Process
[Item] → PROBLEM → STOP LINE
[Item] → (not processed)
[Item] → (not processed)
```

---

## You've Completed Pass C!

You can now:
✓ **Visualize** loops as assembly lines
✓ **See** filter/accumulate/break patterns
✓ **Understand** nested loops as multi-level processing
✓ **Draw** mental flowcharts for loops
✓ **Recognize** patterns by visual structure

**Next:**
- **Pass 3 (Templates):** Copy and modify loop patterns for your AI systems

**Remember:** When you see loops in real code, visualize the assembly line. You'll instantly understand what it does without tracing every iteration.

---

## Pro Tip: The Mental Assembly Line

Whenever you see a loop:
1. **Identify the conveyor belt** (what's being looped?)
2. **See the process** (what happens to each item?)
3. **Spot the exits** (break/continue/end?)

You don't need to trace every item. Just see the pattern and flow.
