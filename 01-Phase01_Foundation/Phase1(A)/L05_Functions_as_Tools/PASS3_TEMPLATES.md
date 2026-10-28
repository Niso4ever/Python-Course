# Lesson 05 - Pass 3: TEMPLATES
## Your Copy-Paste Function Library

**Goal:** Build your reference library of reusable function patterns. Copy, modify, use.

> **2026 Note:** All templates are shown in 2026 style with type hints.
> If you see `-> str` or `param: int` — that's just a label. The function works identically without them.
> Classic style (no type hints) is still valid everywhere.

---

## How to Use These Templates

1. **Identify** what you want to package as a reusable tool
2. **Find** the matching template
3. **Copy** the code
4. **Modify** the names and logic
5. **Call** it anywhere in your system

---

## Template Library

### Template 1: Prompt Formatter
**Use when:** Need to build LLM prompts from parts

```python
def format_rag_prompt(question: str, context: str, max_length: int = 2000) -> str:
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    return prompt[:max_length]
```

**Example call:**
```python
result = format_rag_prompt("What is RAG?", "RAG combines retrieval with generation.")
print(result)
# Context:
# RAG combines retrieval with generation.
#
# Question: What is RAG?
#
# Answer:
```

---

### Template 2: Token Counter / Cost Estimator
**Use when:** Need to track usage and cost

```python
def count_tokens(text: str) -> int:
    return len(text) // 4

def estimate_cost(text: str, cost_per_token: float = 0.000015) -> float:
    return count_tokens(text) * cost_per_token
```

**Example calls:**
```python
tokens = count_tokens("Hello world, how are you today?")
print(tokens)   # 7

cost = estimate_cost("Hello world, how are you today?")
print(cost)     # 0.000000105
```

---

### Template 3: Input Validator
**Use when:** Need to validate before processing

```python
def validate_query(query: str, min_length: int = 5, max_length: int = 500) -> bool:
    if not query or not isinstance(query, str):
        return False
    return min_length <= len(query) <= max_length
```

**Example calls:**
```python
print(validate_query("Hi"))               # False  (too short — only 2 chars)
print(validate_query("What is RAG?"))     # True   (12 chars, within range)
print(validate_query(""))                 # False  (empty string)
```

---

### Template 4: Result Packager
**Use when:** Need to return structured output

```python
def package_rag_result(question: str, answer: str, sources: list, confidence: float) -> dict:
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "citation": f"Sources: {', '.join(sources)}"
    }
```

**Example call:**
```python
result = package_rag_result(
    question="What is RAG?",
    answer="RAG combines retrieval with generation.",
    sources=["Wikipedia", "ArXiv"],
    confidence=0.92
)
print(result["answer"])    # RAG combines retrieval with generation.
print(result["citation"])  # Sources: Wikipedia, ArXiv
print(result["confidence"])# 0.92
```

---

### Template 5: RAG Pipeline
**Use when:** Need end-to-end retrieval + generation

```python
def rag_pipeline(user_question: str, vector_db, llm_client, top_k: int = 3) -> dict:
    docs     = vector_db.search(user_question, top_k=top_k)
    context  = "\n".join([d["text"] for d in docs])
    prompt   = format_rag_prompt(user_question, context)
    answer   = llm_client.invoke(prompt)
    sources  = [d["source"] for d in docs]
    return package_rag_result(user_question, answer, sources, docs[0]["score"])
```

**Example call:**
```python
# Requires a real vector_db and llm_client (see template_rag_pipeline.py for runnable demo)
result = rag_pipeline("What is RAG?", my_vector_db, my_llm_client)
print(result["answer"])     # LLM-generated answer
print(result["sources"])    # ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
print(result["confidence"]) # 0.95  (score of top retrieved doc)
```

---

### Template 6: Filter Function
**Use when:** Need reusable filtering of collections

```python
def filter_by_score(results: list, threshold: float = 0.80, max_results: int = 5) -> list:
    filtered = [r for r in results if r["score"] >= threshold]
    return filtered[:max_results]
```

**Example call:**
```python
results = [
    {"text": "RAG is...",        "score": 0.95},
    {"text": "LLMs are...",      "score": 0.72},
    {"text": "Retrieval means..","score": 0.88},
]
top = filter_by_score(results)
print(len(top))          # 2  (score 0.72 dropped, didn't meet 0.80 threshold)
print(top[0]["score"])   # 0.95

strict = filter_by_score(results, threshold=0.90)
print(len(strict))       # 1  (only 0.95 passes)
```

---

### Template 7: LLM Caller
**Use when:** Need to call the LLM API

```python
def call_llm(prompt: str, model: str = "claude-sonnet-5-5", max_tokens: int = 1000) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

**Example calls:**
```python
# Basic call — uses default model and max_tokens
answer = call_llm("What is RAG?")
print(answer)  # "RAG stands for Retrieval-Augmented Generation..."

# Custom model
answer = call_llm("Summarize this in one sentence.", model="claude-opus-5-5")
print(answer)  # "RAG enhances LLMs by retrieving relevant documents before generating."

# Shorter response limit
answer = call_llm("What is AI?", max_tokens=50)
print(answer)  # truncated to ~50 tokens
```

---

### Template 8: Safe Wrapper
**Use when:** Need error handling around risky operations

```python
def safe_execute(func, *args, fallback=None, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error in {func.__name__}: {e}")
        return fallback
```

**Example calls:**
```python
# Normal call — works fine
result = safe_execute(count_tokens, "Hello world")
print(result)  # 2

# Broken call — integer has no len(), exception is caught
result = safe_execute(count_tokens, 12345, fallback="error")
# Error in count_tokens: object of type 'int' has no len()
print(result)  # "error"  (fallback returned instead of crash)
```

---

### Template 9: Agent Factory
**Use when:** Need to create multiple similar agents

```python
def create_agent(model: str, system_prompt: str, temperature: float = 0.7):
    def agent(user_input: str, history: list = None) -> str:
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_input})
        return call_llm(messages, model=model)
    return agent
```

**Example calls:**
```python
# Factory creates two different agents from one template
research_agent = create_agent("claude-sonnet-5-5", "You are a research assistant. Be thorough.")
code_agent     = create_agent("claude-sonnet-5-5", "You are a coding assistant. Be concise.")

# Each agent behaves differently based on its system prompt
answer = research_agent("What is RAG?")
print(answer)  # Long, detailed research answer

code = code_agent("Write a Python function to count tokens.")
print(code)    # Short, direct code block
```

---

### Template 10: Conversation Manager
**Use when:** Need to manage multi-turn chat

```python
def add_turn(history: list, user_message: str, assistant_response: str) -> list:
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_response})
    return history

def trim_history(history: list, max_turns: int = 10) -> list:
    max_messages = max_turns * 2
    return history[-max_messages:] if len(history) > max_messages else history
```

**Example calls:**
```python
history = []
history = add_turn(history, "What is RAG?", "RAG combines retrieval with generation.")
history = add_turn(history, "How does it work?", "It retrieves docs, then generates an answer.")
print(len(history))  # 4  (2 turns = 4 messages: user+assistant each time)

history = trim_history(history, max_turns=1)
print(len(history))  # 2  (only the last 1 turn kept)
print(history[0]["content"])  # "How does it work?"
```

---

## Quick Selection Guide

| Need | Template |
|:-----|:---------|
| Build LLM prompt | Template 1: Prompt Formatter |
| Track tokens/cost | Template 2: Token Counter |
| Validate input | Template 3: Input Validator |
| Structured output | Template 4: Result Packager |
| Full RAG flow | Template 5: RAG Pipeline |
| Filter results | Template 6: Filter Function |
| Call Claude API | Template 7: LLM Caller |
| Safe execution | Template 8: Safe Wrapper |
| Multiple agents | Template 9: Agent Factory |
| Multi-turn chat | Template 10: Conversation Manager |

---

## Common Combinations

### Validate → Process → Package
```python
def handle_query(query, db, llm):
    if not validate_query(query):
        return {"error": "Invalid query"}
    docs = db.search(query)
    answer = llm.invoke(format_rag_prompt(query, docs))
    return package_rag_result(query, answer, docs)
```

**Example calls:**
```python
result = handle_query("Hi", my_db, my_llm)
print(result)  # {"error": "Invalid query"}  (too short, caught by validate_query)

result = handle_query("What is RAG?", my_db, my_llm)
print(result["answer"])  # LLM answer about RAG
```

### Build + Call + Return
```python
def one_shot_answer(question, context):
    prompt  = format_rag_prompt(question, context)
    answer  = call_llm(prompt)
    return answer
```

**Example call:**
```python
answer = one_shot_answer("What is RAG?", "RAG combines retrieval with generation.")
print(answer)  # LLM-generated answer string
```

---

## Modification Guide

Every template has **← MODIFY** markers in the full files. Change:
- **Names** to match your domain
- **Default values** to your requirements
- **Logic** to your specific rules
- **Return format** to what your system needs
