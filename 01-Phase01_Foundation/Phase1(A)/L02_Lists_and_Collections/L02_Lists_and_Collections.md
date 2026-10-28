# Lesson 02: Lists & Collections
## The Warehouse Theory

Architect, if a **Dictionary** is a labeled drawer, a **List** is a **Warehouse** (organized shelves where order matters).

In AI development, 80% of your code involves **Lists of Dictionaries**. This is THE fundamental pattern you'll see everywhere:
- Search results from RAG systems
- Conversation history in chatbots
- Multiple LLM responses
- Document metadata collections

### 1. The Simple Warehouse (list)
A list stores multiple items in order using square brackets `[]`.

```python
# Simple list
tools = ["search", "summarize", "translate"]
search_scores = [0.95, 0.88, 0.76]
```

| Symbol | Role |
| :--- | :--- |
| `[` `]` | "This is a warehouse of items in order" |
| `,` | Separates items on different shelves |
| `0, 1, 2` | Shelf numbers (called "index") - Python counts from 0 |

---

### 2. Accessing Items by Position
Use the shelf number (index) in square brackets:

```python
tools = ["search", "summarize", "translate"]

first_tool = tools[0]      # "search"
last_tool = tools[-1]      # "translate" (negative counts from end)
```

---

### 3. The AI Pattern: List of Dictionaries
This is what you'll see in EVERY AI system:

```python
search_results = [
    {"source": "Wikipedia", "score": 0.95, "text": "AI is..."},
    {"source": "ArXiv", "score": 0.88, "text": "Machine learning..."},
    {"source": "Blog", "score": 0.76, "text": "Neural networks..."}
]

# Access first result
print(search_results[0])
# Output: {"source": "Wikipedia", "score": 0.95, "text": "AI is..."}

# Access the score of first result
print(search_results[0]["score"])
# Output: 0.95
```

**Pattern Recognition:**
```
[                           ← List starts (warehouse door)
    {key: value, key: value},   ← Dictionary (labeled drawer)
    {key: value, key: value},   ← Another dictionary
    {key: value, key: value}    ← Another dictionary
]                           ← List ends
```

---

### 4. Growing Collections (.append)
Lists can grow dynamically - this is how chatbots build conversation history:

```python
conversation = []

# Round 1
conversation.append({"role": "user", "content": "What is AI?"})
conversation.append({"role": "assistant", "content": "AI is artificial intelligence..."})

# Round 2
conversation.append({"role": "user", "content": "Tell me more"})

# Now conversation has 3 items (user, assistant, user)
print(len(conversation))  # Output: 3
```

**The Chatbot Secret:** Each turn, the LLM receives the ENTIRE conversation list, giving it full context of what was said before.

---

### 5. Common List Operations

```python
# Create
results = []

# Add items
results.append({"score": 0.95})
results.append({"score": 0.88})

# Count items
total = len(results)  # 2

# Check if item exists
if {"score": 0.95} in results:
    print("Found it!")

# Remove item
results.remove({"score": 0.88})

# Access by position
first = results[0]
last = results[-1]
```

---

### 6. Pattern Recognition Guide

**When you see square brackets `[]`:**
- Empty list: `results = []`
- List with items: `tools = ["search", "summarize"]`
- Accessing by index: `tools[0]`

**When you see list of dicts (THE pattern):**
```python
[
    {"key": "value"},
    {"key": "value"},
    {"key": "value"}
]
```
This means: Multiple labeled items in order (search results, messages, documents)

---

### 7. Real-World AI Examples

**RAG Search Results:**
```python
retrieved_docs = [
    {"source": "KB", "score": 0.94, "chunk": "Text here..."},
    {"source": "KB", "score": 0.89, "chunk": "More text..."},
    {"source": "KB", "score": 0.82, "chunk": "Even more..."}
]
```

**Conversation History:**
```python
chat_history = [
    {"role": "user", "content": "Question 1"},
    {"role": "assistant", "content": "Answer 1"},
    {"role": "user", "content": "Question 2"},
    {"role": "assistant", "content": "Answer 2"}
]
```

**Multiple LLM Calls:**
```python
llm_responses = [
    {"model": "claude-opus-5-5", "tokens": 1500, "response": "..."},
    {"model": "claude-sonnet-5-5", "tokens": 1200, "response": "..."},
    {"model": "gpt-4", "tokens": 1800, "response": "..."}
]
```

---

### 8. Templates You've Created

You now have templates in this lesson folder ([./](./)):

- **CHEATSHEET_L02.py** - Quick reference for lists
- **template_list_operations.py** - 10 common patterns
- **template_conversation_history.py** - How chatbots work
- **VISUAL_conversation_flow.md** - Visual diagrams

**Your workflow:**
1. Copy the template that matches your need
2. Modify the values
3. Move on

---

### 9. The One Pattern to Master

If you understand this single pattern, you understand 80% of AI code:

```python
# List of dictionaries
collection = [
    {"label": "value", "label": "value"},
    {"label": "value", "label": "value"}
]

# Access: collection[0]["label"]
# Add: collection.append({"new": "item"})
# Count: len(collection)
```

That's it. This is the DNA of AI systems.

---

### 10. Next Steps

**Immediate:**
1. Open [CHEATSHEET_L02.py](CHEATSHEET_L02.py)
2. Try the conversation history template
3. Recognize the pattern in real AI code

**Soon:**
- Move to Lesson 03 (Logic Gates)
- Build systems that filter and route based on scores
- Combine everything you've learned

---

**Remember:** You're not memorizing syntax. You're recognizing patterns. Keep the cheatsheet open and reference templates when building.
