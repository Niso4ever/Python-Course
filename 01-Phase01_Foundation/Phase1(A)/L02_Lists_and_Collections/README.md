# Lesson 02 / L03_Logic_Gates Templates: Lists & Collections
## Your Reference Library for Managing Multiple Items

**Lesson:** 1.5 (Lists & Collections)
**Templates created:** 4 files
**Status:** ✅ Ready to use

---

## 📚 What's in This Folder

| File | Purpose | When to Use |
|:-----|:--------|:------------|
| **CHEATSHEET_L02.py** | One-page quick reference | Keep open while coding |
| **template_list_operations.py** | 10 common list patterns | Copy-paste for any list operation |
| **template_conversation_history.py** | Chatbot context management | Multi-turn conversations |
| **VISUAL_conversation_flow.md** | Visual diagrams | Understanding how chatbots work |

---

## 🎯 Quick Start Guide

### **1. Start with the Cheatsheet** ⭐
Open: [CHEATSHEET_L02.py](CHEATSHEET_L02.py)

**What it contains:**
- Creating lists (empty, with items)
- Accessing items (index, negative index)
- Adding/removing items
- List operations (len, max, min, sum, sort)
- List of dictionaries pattern
- Common AI patterns
- Red flag checklist

**How to use:**
- Keep it open in a second window
- Reference when you forget syntax
- Use the checklist to review code

---

### **2. Common Patterns Template**
Open: [template_list_operations.py](template_list_operations.py)

**Contains 10 patterns:**
1. Search Results Storage (list of dicts)
2. Conversation History (growing list)
3. Filtering Results (building new list)
4. Source Attribution (simple list)
5. Token Usage Tracking (list of numbers)
6. Error Collection (don't crash, collect)
7. Tool Call History (agent actions)
8. Batch Processing Results
9. Dynamic Prompt Building
10. Relevance Ranking

**Use when:**
- Building any AI system
- Need a starting pattern
- Want production-ready code

---

### **3. Conversation History Template**
Open: [template_conversation_history.py](template_conversation_history.py)

**What it contains:**
- How chatbots maintain context
- Growing conversation pattern
- Token limit management
- Conversation summarization
- Complete chatbot loop example

**Use when:**
- Building multi-turn chatbots
- Creating conversational AI
- Managing LLM context

---

### **4. Visual Guide**
Open: [VISUAL_conversation_flow.md](VISUAL_conversation_flow.md)

**What it shows:**
- Step-by-step conversation flow
- How lists grow over time
- Why full history is sent to LLM
- Visual diagrams

**Use when:**
- Learning how chatbots work
- Explaining to others
- Debugging conversation issues

---

## 🚀 Common Workflows

### **Workflow 1: Building a RAG System**

**Need:** Store search results

```python
# Copy from template_list_operations.py - PATTERN 1

search_results = [
    {"source": "Wikipedia", "score": 0.95, "content": "..."},
    {"source": "ArXiv", "score": 0.88, "content": "..."}
]

# Access top result
top_result = search_results[0]
top_score = search_results[0]["score"]
```

---

### **Workflow 2: Building a Chatbot**

**Need:** Manage conversation history

```python
# Copy from template_conversation_history.py

conversation = []

# User speaks
conversation.append({"role": "user", "content": "What is RAG?"})

# Send ENTIRE list to LLM
response = llm.generate(messages=conversation)

# Add LLM response
conversation.append({"role": "assistant", "content": response})
```

---

### **Workflow 3: Filtering Results**

**Need:** Keep only high-quality documents

```python
# Copy from template_list_operations.py - PATTERN 3

high_quality = []
for result in all_results:
    if result["score"] >= 0.85 and result["verified"]:
        high_quality.append(result)
```

---

## 📖 Key Concepts from Lesson 02

### **Lists (The Collection Type)**
```python
# Simple list
tools = ["search", "summarize", "translate"]

# Empty list (grows over time)
messages = []
messages.append("Hello")

# List of dictionaries (MOST COMMON IN AI!)
results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "ArXiv", "score": 0.88}
]
```

### **Accessing Items**
```python
tools = ["search", "summarize", "translate"]

first = tools[0]          # "search" (index 0)
last = tools[-1]          # "translate" (negative index)
second = tools[1]         # "summarize"

# Two-level access (list of dicts)
score = results[0]["score"]  # First result's score
```

### **Growing Lists**
```python
conversation = []                           # Start empty
conversation.append("User: Hello")          # Add items
conversation.append("Agent: Hi!")
print(len(conversation))                    # Count: 2
```

---

## ✅ Red Flag Checklist

When reviewing list code, check for:

**Index Issues:**
- [ ] Check if list is empty before accessing `[0]`
- [ ] Valid indices (0 to len-1)
- [ ] Negative indices used correctly (-1 = last)

**Modification Issues:**
- [ ] NOT modifying list while looping over it
- [ ] Safe removal (not during iteration)

**Access Issues:**
- [ ] Safe dict access in list of dicts (.get())
- [ ] Handle missing keys gracefully

**Common Patterns:**
- [ ] Using .append() to grow lists
- [ ] Using len() to count items
- [ ] Starting with empty list []

---

## 🎓 Skills You've Mastered

After completing Lesson 02, you can:
- ✅ Create and initialize lists
- ✅ Access items by index (positive and negative)
- ✅ Add items with .append()
- ✅ Remove items with .remove() and .pop()
- ✅ Work with list of dictionaries (THE AI pattern)
- ✅ Build conversation history
- ✅ Filter and sort results
- ✅ Use list operations (len, max, min, sum)

---

## 🔗 Related Resources

**Back to:** [Phase 1 overview](../../README.md)
**Lesson Materials:** [L02_Lists_and_Collections.md](L02_Lists_and_Collections.md)
**Practice:** the `template_*.py` files in this folder

---

## 💡 Most Important Patterns

### **#1: List of Dictionaries (RAG Results)**
```python
search_results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "ArXiv", "score": 0.88}
]
# Access: search_results[0]["score"]
```

### **#2: Conversation History**
```python
conversation = []
conversation.append({"role": "user", "content": "..."})
conversation.append({"role": "assistant", "content": "..."})
# Send entire list to LLM each turn!
```

### **#3: Growing/Filtering Pattern**
```python
filtered = []
for item in all_items:
    if item["score"] >= threshold:
        filtered.append(item)
```

---

## 📊 Template Usage Stats

| Pattern | Frequency in AI Code | Importance |
|:--------|:---------------------|:-----------|
| List of dicts | ⭐⭐⭐⭐⭐ | Critical - 80% of APIs |
| Conversation history | ⭐⭐⭐⭐⭐ | Critical - Every chatbot |
| Filtering | ⭐⭐⭐⭐ | Very High - Every RAG system |
| Simple lists | ⭐⭐⭐⭐ | High - Common everywhere |
| Number lists | ⭐⭐⭐ | Medium - Metrics tracking |

---

## 🚀 Next Steps

**Practice:**
1. Try each pattern with a real use case
2. Build a simple chatbot using conversation template
3. Implement RAG filtering

**Advance:**
1. Move to Lesson 03 (Logic Gates)
2. Move to Lesson 04 (Loops) - Learn to process lists efficiently
3. Combine with Lesson 01 patterns (dicts + lists)

---

**Remember:** Lists are THE fundamental collection type in Python. Master these patterns and you can build any AI system! 🚀
