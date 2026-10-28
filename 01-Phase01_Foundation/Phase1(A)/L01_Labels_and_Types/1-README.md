# Lesson 01 Templates: Variables & Dictionaries
## Your Reference Library for Labeled Data Storage

**Lesson completed:** All 3 passes (Recognition, Evaluation, Template)
**Templates created:** 5 files
**Status:** ✅ Ready to use

> **2026 Note:** You will see type hints in real AI code: `name: str = "value"`.
> This is the same variable — just with a type label added. See Section 1B in CHEATSHEET_L01.py.

---

## 📚 What's in This Folder

| File | Purpose | When to Use |
|:-----|:--------|:------------|
| **CHEATSHEET_L01.py** | One-page quick reference | Keep open while coding |
| **template_llm_metadata.py** | Track LLM API calls | Every LLM interaction |
| **template_document_metadata.py** | Store RAG search results | Vector DB queries |
| **template_agent_config.py** | Configure AI agents | Agent settings & state |
| **template_structured_output.py** ⭐ NEW | Force LLM to return specific format | When you need JSON output |
| **example_structured_output_demo.py** | Try it now demo | Learning structured output |

---

## 🎯 Quick Start Guide

### **1. Start with the Cheatsheet** ⭐
Open: [CHEATSHEET_L01.py](CHEATSHEET_L01.py)

**What it contains:**
- All variable types (string, number, boolean)
- Dictionary syntax (simple & nested)
- Common patterns in AI code
- Red flag checklist
- Visual shape recognition guide

**How to use:**
- Keep it open in a second window
- Reference when you forget syntax
- Use the checklist to review code

---

### **2. Copy-Paste Templates**

#### **For LLM Call Tracking:**
→ [template_llm_metadata.py](template_llm_metadata.py)

**Contains:**
```python
llm_call_metadata = {
    "model": "claude-opus-5-5",
    "tokens_total": 1523,
    "cost_usd": 0.0234,
    # ... and more
}
```

**Use when:**
- Calling Claude, GPT, or any LLM
- Tracking costs
- Monitoring performance
- Debugging API issues

---

#### **For Document Storage:**
→ [template_document_metadata.py](template_document_metadata.py)

**Contains:**
```python
document_metadata = {
    "doc_id": "doc_12345",
    "source": "Wikipedia",
    "relevance_score": 0.947,
    # ... and more
}
```

**Use when:**
- Building RAG systems
- Storing vector search results
- Managing knowledge bases
- Source attribution

---

#### **For Agent Configuration:**
→ [template_agent_config.py](template_agent_config.py)

**Contains:**
```python
rag_config = {
    "relevance_threshold": 0.85,
    "max_context_docs": 3,
    # ... and more
}
```

**Use when:**
- Configuring RAG systems
- Setting up chatbots
- Managing agent state
- Tracking token budgets

---

## 🚀 Common Workflows

### **Workflow 1: Working with AI**
1. Ask Claude to generate code
2. Open `CHEATSHEET_L01.py`
3. Compare AI output to patterns
4. Check red flag list
5. Direct AI to fix issues

---

### **Workflow 2: Building Something New**
1. Pick the relevant template
2. Copy the entire file
3. Tell AI: "Modify this template for [use case]"
4. Review changes
5. Use in your project

---

### **Workflow 3: Quick Reference**
1. Forgot syntax?
2. Open cheatsheet
3. Find the pattern
4. Copy-paste
5. Done!

---

## 📖 Key Concepts from Lesson 1

### **Variables (Labels)**
```python
# Classic style (still valid):
user_query = "What is Python?"    # String (text)
token_count = 1500                 # Integer (number)
relevance_score = 0.95             # Float (decimal)
is_verified = True                 # Boolean (yes/no)

# 2026 style — same thing, with type hints:
user_query: str   = "What is Python?"   # str = text
token_count: int  = 1500                # int = whole number
relevance_score: float = 0.95          # float = decimal
is_verified: bool = True               # bool = True/False
```

### **Simple Dictionary**
```python
metadata = {
    "key": "value",
    "count": 42,
    "active": True
}
```

### **Nested Dictionary**
```python
rag_data = {
    "request": {
        "query": "...",
        "temperature": 0.7
    },
    "response": {
        "content": "...",
        "tokens": 234
    }
}
```

### **Accessing Values**
```python
# Direct access
value = metadata["key"]

# Safe access (won't crash)
value = metadata.get("key", default)

# Nested access
value = rag_data["request"]["query"]

# Safe nested
value = rag_data.get("request", {}).get("query", "")
```

---

## ✅ Red Flag Checklist

When reviewing code, check for:

**Syntax Issues:**
- [ ] Quotes are matched (" " or ' ')
- [ ] Commas separate dict items
- [ ] Colons (:) used in dicts, not equals (=)
- [ ] Opening { has closing }

**Type Issues:**
- [ ] Numbers WITHOUT quotes
- [ ] Text WITH quotes
- [ ] Booleans capitalized (True/False)

**Safety Issues:**
- [ ] No hardcoded API keys
- [ ] Safe dict access (.get() or if check)
- [ ] Magic numbers explained

---

## 🎓 Skills You've Mastered

After completing Lesson 01, you can:
- ✅ Recognize dictionary patterns instantly
- ✅ Spot type errors (string vs number)
- ✅ Catch syntax bugs in 5 seconds
- ✅ Use safe dictionary access patterns
- ✅ Identify security issues (hardcoded secrets)
- ✅ Have production-ready templates

---

## 🔗 Related Resources

**Back to:** [Phase 1 overview](../../README.md)
**Lesson Materials:** [L01_Labels_and_Types.md](L01_Labels_and_Types.md)
**Practice:** the `template_*.py` files in this folder

---

## 📊 Template Usage Examples

### **Example 1: Track LLM Call**
```python
# Copy template_llm_metadata.py pattern
call_data = {
    "model": "claude-opus-5-5",
    "tokens": 1500,
    "cost": 0.02
}
print(f"Call cost: ${call_data['cost']}")
```

### **Example 2: Store Search Result**
```python
# Copy template_document_metadata.py pattern
doc = {
    "source": "Wikipedia",
    "score": 0.95,
    "verified": True
}
if doc["verified"] and doc["score"] > 0.90:
    print("High quality source!")
```

### **Example 3: Configure Agent**
```python
# Copy template_agent_config.py pattern
config = {
    "threshold": 0.85,
    "max_docs": 3
}
# Use config values
if result["score"] >= config["threshold"]:
    print("Above threshold")
```

---

## 💡 Next Steps

**Practice:**
1. Try each template with a real use case
2. Modify values for your needs
3. Build muscle memory for patterns

**Advance:**
1. Move to Lesson 02 (Lists)
2. Create more templates
3. Combine patterns from multiple lessons

---

**Remember:** These templates are your foundation. You'll use dictionary patterns in EVERY AI system you build. Master these, and you're set for everything that follows. 🚀
