# Lesson 02 - Pass 1: RECOGNITION
## Learn to SEE Lists and Collections in the Wild

**Goal:** By the end of this pass, you'll instantly recognize list patterns — especially the List of Dicts — and understand what they hold WITHOUT writing any code.

---

## The Shape Recognition Method

Lists have a distinctive VISUAL SHAPE using square brackets `[]`. Learn to recognize them by sight.

> **Key insight:** 80% of real AI code is lists of dictionaries. This is THE pattern you'll see in every RAG result, every conversation history, every batch of LLM responses.

### Shape 1: The Simple List

```python
tools = ["search", "summarize", "translate"]
scores = [0.95, 0.88, 0.76]
```

**Visual Pattern:**
```
name = [item, item, item]
         ↑
    square brackets = list
```

**What to recognize:**
- `[` opens the list
- Items separated by commas
- `]` closes the list
- Items are ordered (position matters)

---

### Shape 2: The List of Dictionaries (THE Pattern)

```python
results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "ArXiv",     "score": 0.88},
    {"source": "Blog",      "score": 0.76}
]
```

**Visual Pattern:**
```
[                          ← list opens
    {key: value, ...},     ← dict item 1
    {key: value, ...},     ← dict item 2
    {key: value, ...}      ← dict item 3 (no trailing comma)
]                          ← list closes
```

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Simple Tool List

```python
# What tools the agent can use
available_tools = ["web_search", "calculator", "read_document"]

# Access by position (index starts at 0)
first_tool = available_tools[0]    # "web_search"
last_tool  = available_tools[-1]   # "read_document"
```

**RECOGNIZE THIS:**
- `[0]` ← first item (Python counts from 0)
- `[-1]` ← last item (negative = count from end)

**What it does:** "Store an ordered collection of tool names."

---

### Example 2: RAG Search Results (THE Core Pattern)

```python
# Vector database returns this after a search:
retrieved_docs = [
    {"source": "KB",      "score": 0.94, "text": "RAG combines retrieval..."},
    {"source": "KB",      "score": 0.89, "text": "Vector databases store..."},
    {"source": "ArXiv",   "score": 0.82, "text": "Semantic search finds..."}
]

# Access first result:
print(retrieved_docs[0])
# → {"source": "KB", "score": 0.94, "text": "RAG combines retrieval..."}

# Access score of first result:
print(retrieved_docs[0]["score"])
# → 0.94
```

**RECOGNIZE THIS:**
- `retrieved_docs[0]` ← entire first dictionary
- `retrieved_docs[0]["score"]` ← one value inside the first dictionary
- Pattern: `list[index]["key"]`

**What it does:** "Multiple search results, each labeled with source, score, and content."

---

### Example 3: Conversation History

```python
# How chatbots remember the conversation:
chat_history = [
    {"role": "user",      "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG stands for Retrieval-Augmented Generation..."},
    {"role": "user",      "content": "How does it work?"},
    {"role": "assistant", "content": "It works by searching a knowledge base first..."}
]
```

**RECOGNIZE THIS:**
- Every message is a dict with `"role"` and `"content"` keys
- The list is the full conversation in order
- The LLM receives this entire list each turn

**What it does:** "Ordered memory of the conversation — every chatbot uses this exact pattern."

---

### Example 4: Growing a List with .append()

```python
# Start with empty list
conversation = []

# Round 1 — add messages one at a time
conversation.append({"role": "user",      "content": "Hello!"})
conversation.append({"role": "assistant", "content": "Hi! How can I help?"})

# Round 2
conversation.append({"role": "user",      "content": "What is Python?"})

# Now conversation has 3 items
print(len(conversation))  # → 3
```

**RECOGNIZE THIS:**
- `[]` ← empty list (warehouse ready to receive items)
- `.append(item)` ← add one item to the end
- `len(list)` ← count of items

**What it does:** "Build a conversation history turn by turn."

---

### Example 5: Multiple LLM Responses

```python
# Compare 3 models on same prompt:
llm_responses = [
    {"model": "claude-sonnet-5-5", "tokens": 1500, "cost": 0.004, "response": "..."},
    {"model": "claude-opus-5-5",   "tokens": 1200, "cost": 0.018, "response": "..."},
    {"model": "gpt-4",             "tokens": 1800, "cost": 0.054, "response": "..."}
]

# Access the cheapest (first) model's name:
cheapest_model = llm_responses[0]["model"]
```

**RECOGNIZE THIS:**
- List of 3 dictionaries — one per model
- Each dict has identical keys (model, tokens, cost, response)
- Access pattern: `list[0]["key"]`

**What it does:** "Track and compare multiple LLM call results in one structure."

---

### Example 6: Checking List Size

```python
docs = search_database(query)

# How many results came back?
count = len(docs)     # → 3

# Is the list empty?
if len(docs) == 0:
    print("No documents found")

# Common shorthand for empty check:
if not docs:
    print("No documents found")
```

**RECOGNIZE THIS:**
- `len(list)` ← number of items
- `if not list:` ← checks if list is empty (same as `len == 0`)

**What it does:** "Guard against empty search results before processing."

---

### Example 7: Tool Definitions (List of Dicts)

```python
# How agents describe their tools to the LLM:
TOOLS = [
    {
        "name":        "web_search",
        "description": "Search the internet for current information.",
        "parameters":  {"query": "string"}
    },
    {
        "name":        "calculator",
        "description": "Evaluate math expressions.",
        "parameters":  {"expression": "string"}
    },
    {
        "name":        "read_document",
        "description": "Read a local file by name.",
        "parameters":  {"filename": "string"}
    }
]
```

**RECOGNIZE THIS:**
- TOOLS is a list of 3 dictionaries
- Each dict describes one tool
- The LLM reads this list to decide which tool to use

**What it does:** "Catalog of available tools — the LLM picks from this list."

---

### Example 8: List Slicing — Keep Last N Items

```python
# Chatbot memory management:
conversation = [
    {"role": "user",      "content": "msg 1"},
    {"role": "assistant", "content": "msg 2"},
    {"role": "user",      "content": "msg 3"},
    # ... 20 more messages
]

# Keep only the last 10 messages (sliding window):
conversation = conversation[-10:]

# Keep first 3 items:
top_3_results = retrieved_docs[:3]
```

**RECOGNIZE THIS:**
- `[-10:]` ← last 10 items
- `[:3]` ← first 3 items
- `[1:4]` ← items at index 1, 2, 3

**What it does:** "Trim conversation to save tokens — only send recent history to LLM."

---

## Access Pattern Summary

```python
results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "ArXiv",     "score": 0.88}
]

results[0]            # → entire first dict
results[0]["score"]   # → 0.95 (value from first dict)
results[-1]           # → entire last dict
len(results)          # → 2 (number of items)
results[:1]           # → [first dict only]
```

---

## Recognition Exercise: What Is This?

```python
# Block A
messages = []
messages.append({"role": "user", "content": "Hello"})
messages.append({"role": "assistant", "content": "Hi!"})

# Block B
docs = [
    {"text": "Python is...", "score": 0.92},
    {"text": "AI means...",  "score": 0.87}
]
top_doc = docs[0]["text"]
```

**Block A:** Empty list → grow with `.append()` → conversation history pattern
**Block B:** List of dicts search results → access first item's text field

---

## Common AI Patterns (Recognition Cheat Sheet)

### Pattern: Conversation History
```python
messages = [
    {"role": "user",      "content": "..."},
    {"role": "assistant", "content": "..."}
]
```
**Recognize:** Chatbot memory — grows every turn

---

### Pattern: RAG Search Results
```python
docs = [
    {"source": "KB", "score": 0.94, "text": "..."},
    {"source": "KB", "score": 0.88, "text": "..."}
]
```
**Recognize:** Vector DB output — sorted by relevance score

---

### Pattern: Tool Registry
```python
tools = [
    {"name": "search",     "description": "..."},
    {"name": "calculator", "description": "..."}
]
```
**Recognize:** LLM reads this to select which tool to call

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** list syntax `[]` by sight
✓ **Identify** the List of Dicts pattern instantly
✓ **Understand** conversation history structure
✓ **Read** access patterns `list[0]["key"]`
✓ **Spot** `.append()` for growing lists
✓ **Know** `len()` and slicing patterns

**Next:**
- **Pass C (Visual):** See lists as warehouses and shelves
- **Pass 3 (Templates):** Copy and modify list patterns for your projects

**Remember:** You're not memorizing. You're training your eyes to SEE patterns.

---

## Pro Tip: The 3-Second Rule

When you see unfamiliar code with `[]`:
1. **Second 1:** Is it a simple list or a list of dicts?
2. **Second 2:** What does each item represent? (message? doc? tool?)
3. **Second 3:** Is the code reading from it, adding to it, or counting it?

That's it. You don't need to understand every detail. Just recognize the pattern.
