# Lesson 05 - Pass C: VISUAL PATTERNS
## See Functions as Machines and Pipelines

**Goal:** Understand function logic through visual diagrams, not just code.

---

## Visual 1: The Basic Function Machine

### Code:
```python
def count_tokens(text):
    tokens = len(text) / 4
    return tokens
```

**Example call:**
```python
result = count_tokens("Hello world")
print(result)  # 2.75  (11 chars ÷ 4)
```

### Visual Machine:
```
           INPUT
             |
             ↓
    ┌─────────────────┐
    │   count_tokens  │
    │                 │
    │  len(text) / 4  │
    │                 │
    └─────────────────┘
             |
             ↓
           OUTPUT
          (tokens)
```

**Pattern:** One entry, one exit, logic inside

---

## Visual 1B: Same Machine — with Type Labels (2026 style)

### Code (classic):
```python
def count_tokens(text):
    return len(text) / 4
```

### Code (2026 — type hints added):
```python
def count_tokens(text: str) -> int:
    return len(text) // 4
```

**Example call — works the same either way:**
```python
result = count_tokens("Hello world")
print(result)  # 2  (same input, same output — type hints change nothing)
```

### Visual — what the labels mean:
```
    def  count_tokens ( text: str ) -> int :
     │         │          │    │       │
     │         │          │    │       └── output type: whole number
     │         │          │    └────────── input type: text
     │         │          └─────────────── parameter name
     │         └────────────────────────── function name
     └──────────────────────────────────── "defining a tool"
```

**Pattern:** Same machine — just has type labels on the door

**The machine is IDENTICAL.** Type hints don't change what the function does.
They just tell you (and your editor) what goes in and what comes out.

---

## Visual 2: Multi-Parameter Function

### Code:
```python
def format_rag_prompt(question, context, max_length=500):
    prompt = f"Context: {context}\n\nQuestion: {question}"
    return prompt[:max_length]
```

**Example call:**
```python
result = format_rag_prompt("What is RAG?", "RAG combines retrieval with generation.")
print(result)
# Context: RAG combines retrieval with generation.
#
# Question: What is RAG?
```

### Visual Machine:
```
  question ──┐
             │
  context ───┼──→ ┌─────────────────────┐
             │    │  format_rag_prompt   │
 max_length ─┘    │                     │
(optional)        │  Combine + truncate │
                  │                     │
                  └─────────────────────┘
                           │
                           ↓
                     formatted prompt
                        (string)
```

**Pattern:** Multiple inputs → one combined output

---

## Visual 3: Function Calling Function

### Code:
```python
def count_tokens(text):
    return len(text) / 4

def estimate_cost(text, rate=0.000015):
    tokens = count_tokens(text)   # ← calls other function
    return tokens * rate
```

**Example calls:**
```python
tokens = count_tokens("Hello world")
print(tokens)   # 2.75

cost = estimate_cost("Hello world")
print(cost)     # 0.00000004125  (2.75 tokens × 0.000015)
```

### Visual:
```
    text ──→ ┌──────────────┐
             │ count_tokens │ ──→ tokens
             └──────────────┘
                                    |
    text ──→ ┌───────────────────────────────┐
             │      estimate_cost            │
             │                               │
             │  tokens = count_tokens(text)  │
             │  cost = tokens * rate         │
             │                               │
             └───────────────────────────────┘
                           │
                           ↓
                          cost
```

**Pattern:** Functions are building blocks — use one inside another

---

## Visual 4: RAG Pipeline (Functions Chained)

### Code:
```python
def search(query):
    return fetch_from_db(query)

def format_context(docs):
    return "\n".join([d["text"] for d in docs])

def generate_answer(question, context):
    prompt = f"Context: {context}\nQ: {question}"
    return llm.invoke(prompt)

def rag_pipeline(user_question):
    docs    = search(user_question)
    context = format_context(docs)
    answer  = generate_answer(user_question, context)
    return answer
```

### Visual Pipeline:
```
User Question
     │
     ↓
┌──────────┐
│  search  │ ──→ docs (list of dicts)
└──────────┘
     │
     ↓
┌────────────────┐
│ format_context │ ──→ context (string)
└────────────────┘
     │
     ↓
┌─────────────────┐
│ generate_answer │ ──→ answer (string)
└─────────────────┘
     │
     ↓
Final Answer
```

**Pattern:** Assembly line — output of each step feeds next step

---

## Visual 5: Validator Function

### Code:
```python
def validate_query(query, min_len=5, max_len=500):
    if len(query) < min_len:
        return False
    if len(query) > max_len:
        return False
    return True
```

**Example calls:**
```python
print(validate_query("Hi"))              # False  (2 chars < min 5)
print(validate_query("What is RAG?"))    # True   (12 chars, in range)
print(validate_query("x" * 600))        # False  (600 chars > max 500)
```

### Visual Flowchart Inside Function:
```
         query enters
              │
              ↓
    ┌─────────────────┐
    │ Too short?      │
    │ len < min_len?  │
    └─────────────────┘
          /      \
        YES       NO
        /           \
       ↓             ↓
  return False  ┌─────────────────┐
                │ Too long?       │
                │ len > max_len?  │
                └─────────────────┘
                     /      \
                   YES       NO
                   /           \
                  ↓             ↓
             return False   return True
```

**Pattern:** Function contains L2 logic gates

---

## Visual 6: Default Parameters

### Code:
```python
def search_database(query, top_k=3, threshold=0.80):
    results = fetch(query)
    return [r for r in results if r["score"] >= threshold][:top_k]
```

### Visual Parameter Slots:
```
┌──────────────────────────────────────────┐
│          search_database(...)            │
│                                          │
│  REQUIRED:    query  ← Must provide      │
│  OPTIONAL:    top_k  ← Default = 3       │
│  OPTIONAL: threshold ← Default = 0.80    │
│                                          │
└──────────────────────────────────────────┘

Calling options:
  search_database("AI")               → uses defaults
  search_database("AI", top_k=5)      → change top_k
  search_database("AI", threshold=0.9) → change threshold
  search_database("AI", 5, 0.9)       → change both
```

**Pattern:** Required inputs first, optional with defaults after

---

## Visual 7: Function That Returns Dict

### Code:
```python
def analyze_response(response, question):
    return {
        "answer": response,
        "length": len(response),
        "question": question,
        "is_detailed": len(response) > 100
    }
```

**Example call:**
```python
result = analyze_response("RAG combines retrieval with generation.", "What is RAG?")
print(result["length"])      # 38
print(result["is_detailed"]) # False  (38 chars < 100)
print(result["question"])    # "What is RAG?"
```

### Visual:
```
  response ──┐
             ├──→ ┌──────────────────┐     ┌─────────────────────┐
  question ──┘    │ analyze_response │ ──→ │ {"answer": ...,     │
                  └──────────────────┘     │  "length": ...,     │
                                           │  "question": ...,   │
                                           │  "is_detailed": ... │
                                           └─────────────────────┘
```

**Pattern:** Multiple inputs → structured dictionary output (L1 pattern inside L3!)

---

## Visual 8: Named Arguments at Call Site

### Code:
```python
def format_result(question, answer, confidence, sources):
    ...

# Two ways to call:
format_result("What is AI?", "AI is...", 0.92, ["Wiki"])  # positional
format_result(
    question="What is AI?",           # named
    answer="AI is...",
    confidence=0.92,
    sources=["Wiki"]
)
```

### Visual Comparison:
```
POSITIONAL (must be in order):
  ┌─────────┬──────────┬────────────┬─────────┐
  │"What is │"AI is..."│    0.92    │["Wiki"] │
  └────┬────┴─────┬────┴──────┬─────┴────┬────┘
       ↓          ↓           ↓          ↓
   question    answer    confidence   sources

NAMED (any order):
  question="What is AI?"  ──→ question
  answer="AI is..."       ──→ answer
  confidence=0.92         ──→ confidence
  sources=["Wiki"]        ──→ sources
```

**Pattern:** Named args = self-documenting code

---

## Visual 9: Complete AI Tool

### Code:
```python
def call_llm(prompt, model="claude-sonnet-5-5", max_tokens=1000):
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages
    )
    return response.content[0].text
```

**Example calls:**
```python
# One line from the outside — all complexity hidden inside
answer = call_llm("What is RAG?")
print(answer)  # "RAG stands for Retrieval-Augmented Generation..."

# Override model for a specific call
answer = call_llm("Explain briefly.", model="claude-haiku-5-5", max_tokens=100)
print(answer)  # short answer from faster model
```

### Visual:
```
                            ┌────────────────────────────┐
   prompt ──────────────────┤                            │
   model (optional) ────────┤        call_llm()          │
   max_tokens (optional) ───┤                            │
                            │  1. Build messages list    │
                            │  2. Call Anthropic API     │
                            │  3. Extract text           │
                            │                            │
                            └────────────────────────────┘
                                          │
                                          ↓
                                    response text
                                      (string)
```

**Pattern:** Wraps complex API into simple one-liner

---

## Visual 10: Function Factory (Advanced)

### Code:
```python
def create_agent(model, system_prompt):
    def agent(user_input):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        return call_llm(messages, model=model)
    return agent  # ← Returns a function!

# Create different agents
research_agent = create_agent("claude-opus-5-5", "You are a researcher")
code_agent = create_agent("claude-sonnet-5-5", "You are a coder")

# Use them
answer = research_agent("What is RAG?")
code = code_agent("Write a Python function")
```

### Visual Factory:
```
create_agent() ←─── FACTORY
      │
      ├── model = "claude-opus-5-5"
      ├── system_prompt = "researcher"
      │
      │  ┌────────────────────────────────┐
      └──┤  Creates & returns:            │
         │                               │
         │  def agent(user_input):       │
         │      ... uses model +         │
         │          system_prompt        │
         │      return llm_response      │
         │                               │
         └────────────────────────────────┘
                         │
                         ↓
              research_agent (customized function)
              code_agent (different customization)
```

**Pattern:** Factory produces customized, pre-configured tools

---

## Shape Comparison Chart

### Simple Tool
```
input → [process] → output
```
Takes input, returns output

---

### Multi-Input Tool
```
input1 ┐
input2 ┼→ [process] → output
input3 ┘
```
Combines inputs into one output

---

### Pipeline
```
input → [step1] → [step2] → [step3] → output
```
Output of each step feeds next

---

### Validator
```
input → [check] → True/False
```
Returns boolean decision

---

### Factory
```
config → [create] → custom_function
                         │
                         ↓
                    input → output
```
Creates and returns other functions

---

## Color Coding Method

When reading function code, mentally color:

- **🔵 Blue** = Function structure (`def`, `return`)
- **🟢 Green** = Parameters (inputs)
- **🟡 Yellow** = Function body (logic)
- **🟠 Orange** = Function calls inside

```python
🔵def format_rag_prompt(🟢question, 🟢context, 🟢max_length=500🟢):
    🟡prompt = f"Context: {context}\n\nQuestion: {question}"
    🟡truncated = prompt[:max_length]
    🔵return truncated
```

---

## Visual Recognition Exercise

Look at this code and draw the shape in your mind:

```python
def build_rag_response(
    question,
    retrieved_docs,
    min_confidence=0.75,
    max_sources=3
):
    filtered = [d for d in retrieved_docs if d["score"] >= min_confidence]
    top_docs = filtered[:max_sources]

    if not top_docs:
        return {"answer": "Insufficient information", "sources": []}

    context = "\n".join([d["text"] for d in top_docs])
    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": [d["source"] for d in top_docs],
        "confidence": top_docs[0]["score"]
    }
```

**Example calls:**
```python
docs = [
    {"text": "RAG combines retrieval with generation.", "source": "Wikipedia", "score": 0.95},
    {"text": "It retrieves relevant documents first.",   "source": "ArXiv",     "score": 0.82},
    {"text": "Low quality match.",                       "source": "Blog",       "score": 0.60},
]

# Normal call — score 0.60 doc filtered out, top 2 pass
result = build_rag_response("What is RAG?", docs)
print(result["answer"])      # LLM-generated answer using top 2 docs
print(result["sources"])     # ["Wikipedia", "ArXiv"]
print(result["confidence"])  # 0.95

# No docs pass threshold → early return
result = build_rag_response("What is RAG?", docs, min_confidence=0.99)
print(result)  # {"answer": "Insufficient information", "sources": []}
```

**Mental Image:**
```
INPUTS: question + docs (required)
        min_confidence + max_sources (optional)
         │
         ↓
    Filter docs → Check if any left → Generate answer
         │                  │
         ↓                  ↓
    [continue]         return early (empty)
         │
         ↓
    Return dict with answer + sources + confidence
```

**Pattern:** Filter → Guard clause → Generate → Return structured dict

---

## You've Completed Pass C!

You can now:
✓ **Visualize** functions as machines
✓ **See** data flow through pipelines
✓ **Understand** function factories
✓ **Map** parameters to input slots
✓ **Recognize** patterns by visual structure

**Next:**
- **Pass 3 (Templates):** Copy and modify function patterns for your AI systems

**Remember:** When you see a function, visualize the machine. Inputs go in, logic runs, output comes out. That's all it is.

---

## Pro Tip: The Machine Blueprint

For any function:
1. **What goes in?** (parameters)
2. **What happens inside?** (logic)
3. **What comes out?** (return value)

Answer these three → you understand the function completely.
