# Lesson 05: Functions (def) as Tools
## The Juicer Theory

> **2026 Note:** You will see two function definition styles in real AI code:
> Classic: `def fn(param):` — still valid, still common
> With type hints: `def fn(param: str) -> str:` — same function, adds type labels
> See Section 7 below for the recognition pattern. See CHEATSHEET_L05.py Section 1B for the full guide.

Architect, you can store data (L01, L02), route it (L03), and process collections (L04). Now you need to **package logic** into reusable tools.

In AI systems, you constantly reuse the same operations:
- Format a prompt → Use everywhere
- Count tokens → Call repeatedly
- Search the database → Trigger on every query
- Validate output → Run after every LLM call

Instead of writing the same code 10 times, you build it **once as a function** and call it anywhere.

---

## 1. The Juicer (def)

A function is a machine: put something in, get something out.

```python
def summarize_text(raw_input):
    summary = raw_input[:20] + "..."
    return summary
```

**Example call:**
```python
result = summarize_text("The history of the world is vast and complex.")
print(result)  # "The history of the wo..."
```

| Symbol | Role |
|:-------|:-----|
| `def` | "I am defining a tool" |
| `summarize_text` | Tool name |
| `(raw_input)` | Input slot (parameter) |
| `return` | Output (what comes out) |

**Pattern:** `def name(input): ... return output`

---

## 2. Calling the Tool

Build once, use anywhere:

```python
# Build the tool (once)
def summarize_text(raw_input):
    summary = raw_input[:20] + "..."
    return summary

# Call the tool (many times)
short = summarize_text("The history of the world is vast...")
print(short)  # "The history of the wor..."

# Call again with different input
another = summarize_text("Artificial intelligence is...")
```

**Pattern:** `result = function_name(input)`

---

## 3. Parameters (Input Slots)

Functions can take multiple inputs:

```python
def format_prompt(user_query, context):
    prompt = f"Context: {context}\n\nQuestion: {user_query}\n\nAnswer:"
    return prompt

# Call with two inputs
result = format_prompt("What is RAG?", "RAG combines retrieval...")
```

**Default parameters** (optional inputs):

```python
def search_database(query, top_k=3):  # top_k defaults to 3
    results = fetch_results(query, limit=top_k)
    return results

# Call without optional param
results = search_database("What is RAG?")  # uses top_k=3

# Call with custom value
results = search_database("What is RAG?", top_k=5)
```

---

## 4. Return Values

Functions give back a result you can store or use:

```python
def count_tokens(text):
    token_count = len(text) / 4
    return token_count

# Store the result
tokens = count_tokens("Hello world")

# Use directly
cost = count_tokens("Your prompt") * 0.00001

# Return a dictionary
def validate_response(response):
    return {
        "valid": len(response) > 10,
        "length": len(response),
        "word_count": len(response.split())
    }

validation = validate_response("This is a response")
print(validation["valid"])  # True
```

---

## 5. Real-World AI Examples

### Prompt Formatter
```python
def format_rag_prompt(question, docs):
    context = "\n".join([doc["text"] for doc in docs])
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    return prompt

# Use it
prompt = format_rag_prompt("What is RAG?", retrieved_docs)
response = llm.invoke(prompt)
```

### Token Counter
```python
def count_tokens(text):
    return len(text) / 4  # ~4 chars per token

def estimate_cost(text, cost_per_token=0.000015):
    tokens = count_tokens(text)
    return tokens * cost_per_token

cost = estimate_cost("Your long prompt here...")
```

### Confidence Checker
```python
def is_high_confidence(response, threshold=0.85):
    return response["confidence"] >= threshold

# Use in if statement
if is_high_confidence(llm_response):
    return_to_user(llm_response)
else:
    escalate_to_human(llm_response)
```

### Result Formatter
```python
def format_rag_result(question, answer, sources, confidence):
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "citation": f"Sources: {', '.join(sources)}"
    }

result = format_rag_result("What is AI?", "AI is...", ["Wikipedia"], 0.92)
```

---

## 6. Functions That Use Other Functions

This is how AI pipelines are built:

```python
def search(query):
    return fetch_from_db(query)

def format_context(docs):
    return "\n".join([d["text"] for d in docs])

def generate_answer(question, context):
    prompt = f"Context: {context}\nQuestion: {question}"
    return llm.invoke(prompt)

# Full RAG pipeline
def rag_pipeline(user_question):
    docs = search(user_question)          # Step 1: Retrieve
    context = format_context(docs)         # Step 2: Format
    answer = generate_answer(user_question, context)  # Step 3: Generate
    return answer

# One call, entire pipeline runs
response = rag_pipeline("What is RAG?")
```

---

## 7. Pattern Recognition Guide

**When you see:**
```python
def function_name(param):
    ...
    return result
```
**Translation:** "This is a reusable tool being defined"

**When you see:**
```python
result = function_name(argument)
```
**Translation:** "Calling the tool with input, storing output"

**When you see:**
```python
def function(param=default_value):
```
**Translation:** "Optional parameter with default"

**When you see:**
```python
def function(param1, param2, param3):
```
**Translation:** "Tool takes 3 inputs"

**When you see (2026 style):**
```python
def function_name(param: str) -> dict:
```
**Translation:** "Same tool — `: str` labels the input type, `-> dict` labels the output type"

```python
def search_docs(query: str, top_k: int = 3) -> list:
```
**Translation:** "query is text, top_k is a whole number with default 3, returns a list"

---

## 8. Common AI Function Patterns

### Pattern 1: Validator
```python
def validate_input(text, min_length=10):
    return len(text) >= min_length
```

**Example calls:**
```python
print(validate_input("Hello AI"))          # False  (8 chars < 10)
print(validate_input("Hello AI world!"))   # True   (15 chars >= 10)
```

### Pattern 2: Formatter
```python
def format_for_llm(data):
    return {"role": "user", "content": str(data)}
```

**Example call:**
```python
msg = format_for_llm("What is RAG?")
print(msg)  # {"role": "user", "content": "What is RAG?"}
```

### Pattern 3: Calculator
```python
def calculate_cost(tokens, rate=0.000015):
    return tokens * rate
```

**Example calls:**
```python
cost = calculate_cost(500)
print(cost)   # 0.0075  (500 tokens × default rate)

cost = calculate_cost(500, rate=0.00003)
print(cost)   # 0.015   (custom rate for expensive model)
```

### Pattern 4: Pipeline Step
```python
def process_step(input_data):
    processed = transform(input_data)
    return processed
```

**Example call:**
```python
# transform() is your custom logic — replace with the real operation
output = process_step("raw input text")
# → calls transform("raw input text") → returns processed result
```

### Pattern 5: Router
```python
def route_request(intent):
    if intent == "search":
        return search_tool
    elif intent == "calculate":
        return calc_tool
    else:
        return default_tool
```

**Example calls:**
```python
tool = route_request("search")
print(tool)    # <function search_tool>   — ready to call

tool = route_request("unknown")
print(tool)    # <function default_tool>  — fallback assigned
```

---

## 9. Key Takeaways

✓ **`def`** defines a reusable tool
✓ **Parameters** are the input slots
✓ **`return`** sends output back
✓ **Call** with `result = function(input)`
✓ **Default params** make inputs optional
✓ **Functions call functions** = pipelines

**Most common AI use:**
- Format prompts
- Count/estimate tokens
- Validate LLM outputs
- Build RAG pipelines
- Create reusable steps

---

## 10. Templates Available

See this lesson folder ([./](./)) for ready-to-use function patterns: `template_llm_caller.py`, `template_prompt_formatter.py`, `template_rag_pipeline.py`.

**Your workflow:**
1. Identify what you want to package
2. Find the matching template
3. Copy and modify
4. Use anywhere in your system

---

**Remember:** You're not memorizing function syntax. You're recognizing: "Oh, this is a prompt formatter" or "This is a token calculator." The template handles the rest.
