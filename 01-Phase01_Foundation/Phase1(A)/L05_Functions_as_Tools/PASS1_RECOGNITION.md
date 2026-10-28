# Lesson 05 - Pass 1: RECOGNITION
## Learn to SEE Functions in AI Code

**Goal:** By the end of this pass, you'll instantly recognize function patterns and understand what they do WITHOUT writing any code.

> **2026 Note:** You will see TWO function definition styles in real AI code.
> Classic style: `def fn(param):` — still valid, still common
> 2026 style: `def fn(param: str) -> str:` — same function + type labels added
> Shape 3 below covers the 2026 style. You do NOT need to write type hints. Just recognize them.

---

## The Shape Recognition Method

Functions have distinctive VISUAL SHAPES. Learn to recognize them by sight.

### Shape 1: Function Definition (Classic)

```python
def function_name(parameter):
    ← INDENT (logic here)
    return result
```

**Visual Pattern:**
- `def` keyword
- Function name
- Parentheses `()` with parameters
- Colon `:`
- Indented body
- `return` statement

---

### Shape 2: Function Call

```python
result = function_name(argument)
```

**Visual Pattern:**
- Name followed by `()`
- Arguments inside parentheses
- Often stored in variable

---

### Shape 3: Type-Hinted Function (2026 standard)

```python
def function_name(param: str) -> str:
    ← INDENT (same logic as before)
    return result
```

**Visual Pattern:**
```
def name(param: type, param2: type = default) -> return_type:
              ↑              ↑                  ↑
         input type    optional default      output type
```

**What to recognize:**
- `param: str` ← colon + type after the parameter name
- `-> str` ← arrow + type after the closing parenthesis, before the colon
- Same function body, same logic — just labeled

**Type labels you'll see:**
| Label | Meaning | Example |
|:------|:--------|:--------|
| `: str` | text input | `query: str` |
| `: int` | whole number | `top_k: int = 3` |
| `: float` | decimal | `threshold: float = 0.80` |
| `: bool` | True/False | `strict: bool = False` |
| `: list` | collection | `docs: list` |
| `: dict` | labeled box | `config: dict` |
| `-> str` | outputs text | |
| `-> bool` | outputs True/False | |
| `-> list` | outputs a list | |
| `-> None` | returns nothing | |

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Prompt Formatter

```python
def format_rag_prompt(question, context):
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    return prompt

# Using it
my_prompt = format_rag_prompt("What is AI?", "AI is artificial intelligence...")
```

**RECOGNIZE THIS:**
- Line 1: `def format_rag_prompt(question, context):` ← Define tool with 2 inputs
- Line 2-3: Indented ← Tool logic
- Line 4: `return prompt` ← What comes out
- Line 7: `format_rag_prompt(...)` ← Calling the tool

**What it does:** "Takes a question and context, combines them into an LLM prompt."

---

### Example 2: Token Counter

```python
def count_tokens(text):
    return len(text) / 4

def estimate_cost(text, cost_per_token=0.000015):
    tokens = count_tokens(text)
    return tokens * cost_per_token

# Using them
tokens = count_tokens("Hello world")        # 2.75
cost = estimate_cost("Hello world")         # 0.0000004125
```

**RECOGNIZE THIS:**
- Two separate functions (tools)
- `estimate_cost` calls `count_tokens` inside it
- `cost_per_token=0.000015` ← Default parameter (optional input)

**What it does:** "Count tokens, then calculate cost. Second tool uses first tool."

---

### Example 2B: Token Counter — with Type Hints (2026 style)

```python
# Same logic as Example 2 — just adds type labels
def count_tokens(text: str) -> int:
    return len(text) // 4

def estimate_cost(text: str, cost_per_token: float = 0.000015) -> float:
    tokens = count_tokens(text)
    return tokens * cost_per_token
```

**Example calls — identical to Example 2:**
```python
tokens = count_tokens("Hello world")
print(tokens)   # 2

cost = estimate_cost("Hello world")
print(cost)     # 0.00000003
```

**RECOGNIZE THIS:**
- `text: str` ← input expects text
- `-> int` ← outputs a whole number
- `cost_per_token: float = 0.000015` ← optional decimal input with default
- `-> float` ← outputs a decimal
- Everything else is identical to Example 2

**What it does:** Exactly the same as Example 2. The `: str`, `: float`, `-> int` labels are just documentation for humans and editors. The code runs identically.

---

### Example 3: Input Validator

```python
def validate_query(query, min_length=5, max_length=500):
    if len(query) < min_length:
        return False
    if len(query) > max_length:
        return False
    return True

# Using it
if validate_query(user_input):
    process_query(user_input)
else:
    print("Invalid query length")
```

**RECOGNIZE THIS:**
- Three parameters: one required, two optional (with defaults)
- Returns `True` or `False` (boolean)
- Used in an `if` statement

**What it does:** "Check if query length is valid. Returns True/False."

---

### Example 4: Result Formatter

```python
def format_rag_result(question, answer, sources, confidence):
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "citation": f"Sources: {', '.join(sources)}"
    }

result = format_rag_result(
    question="What is RAG?",
    answer="RAG combines retrieval...",
    sources=["Wikipedia", "ArXiv"],
    confidence=0.92
)
```

**RECOGNIZE THIS:**
- Returns a **dictionary** (L1 pattern inside L3!)
- Named arguments: `question="What is RAG?"` ← More readable calls
- Packages multiple values into structured output

**What it does:** "Takes separate values, packages them into structured dict."

---

### Example 5: Pipeline Function

```python
def rag_pipeline(user_question):
    # Step 1: Retrieve
    docs = search_database(user_question)

    # Step 2: Format context
    context = "\n".join([doc["text"] for doc in docs])

    # Step 3: Generate
    prompt = format_rag_prompt(user_question, context)
    answer = llm.invoke(prompt)

    return answer

# One call runs the whole pipeline
response = rag_pipeline("What is RAG?")
```

**RECOGNIZE THIS:**
- Function calls OTHER functions inside it
- Sequential steps (1, 2, 3)
- One entry point, one exit (`return`)

**What it does:** "Orchestrates the full RAG flow. One call = entire pipeline."

---

#### WHERE IS `docs` DEFINED? — Your sharp question answered

`docs` is never defined as a literal list in this example. It is the **return value** of `search_database()`.
That function runs and hands back a list of dictionaries. Here is what it looks like in memory:

```python
# What search_database() RETURNS (the list that becomes "docs")
docs = [
    {"text": "RAG stands for Retrieval-Augmented Generation...", "score": 0.95},
    {"text": "RAG combines a retrieval system with an LLM...",   "score": 0.88},
    {"text": "The retrieval step fetches relevant documents...", "score": 0.81},
]
# docs is a LIST  ← square brackets [ ]
# each item is a DICT  ← curly braces { }
# each dict has a "text" key  ← that is what doc["text"] reads
```

This list is the **hidden contract** between `search_database()` and the rest of the pipeline.
The function promised: "I will always return a list of dicts, each with a `text` key."
Example 5 trusts that promise.

---

#### BREAKING DOWN THE MYSTERY LINE

```python
context = "\n".join([doc["text"] for doc in docs])
```

Read it in three pieces:

| Piece | What it does |
|:------|:-------------|
| `for doc in docs` | Loop: grab each dictionary, one at a time, call it `doc` |
| `doc["text"]` | From that dictionary, read the value stored under the key `"text"` |
| `"\n".join(...)` | Glue all the text strings together with a newline between each |

**What `context` looks like after this line:**

```
RAG stands for Retrieval-Augmented Generation...
RAG combines a retrieval system with an LLM...
The retrieval step fetches relevant documents...
```

Three separate text values, now one long string, ready to hand to the LLM.

---

#### WHERE IS `prompt` DEFINED?

`prompt` is assigned on the very next line:

```python
prompt = format_rag_prompt(user_question, context)
```

`format_rag_prompt` is defined back in **Example 1** of this lesson:

```python
def format_rag_prompt(question, context):
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    return prompt
```

So after that call, `prompt` looks like this in memory:

```
Context: RAG stands for Retrieval-Augmented Generation...
RAG combines a retrieval system with an LLM...
The retrieval step fetches relevant documents...

Question: What is RAG?

Answer:
```

That full string is what gets sent to `llm.invoke(prompt)`.

---

#### THE FULL DATA FLOW (what moves between each step)

```
user_question (str)
      │
      ▼
search_database(user_question)
      │ returns: list of dicts  ← docs
      ▼
"\n".join([doc["text"] for doc in docs])
      │ returns: one long string  ← context
      ▼
format_rag_prompt(user_question, context)
      │ returns: formatted string  ← prompt
      ▼
llm.invoke(prompt)
      │ returns: LLM answer string  ← answer
      ▼
return answer
```

---

### Example 6: Filter Function

```python
def filter_by_score(results, threshold=0.80):
    filtered = []
    for result in results:
        if result["score"] >= threshold:
            filtered.append(result)
    return filtered

# Using it
high_quality = filter_by_score(search_results)
strict = filter_by_score(search_results, threshold=0.95)
```

**RECOGNIZE THIS:**
- L2.5 loop **inside** L3 function (patterns combine!)
- Default threshold: `threshold=0.80`
- Returns new filtered list

**What it does:** "Wrap the filter loop into a reusable tool."

---

### Example 7: LLM Caller

```python
def call_llm(prompt, model="claude-sonnet-5-5", max_tokens=1000):
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# Basic call
answer = call_llm("What is RAG?")

# Custom model
answer = call_llm("Summarize this", model="claude-opus-5-5")
```

**RECOGNIZE THIS:**
- Three parameters, two with defaults
- No `temperature`: the Claude API removed it in API version 2026-10-21 and returns a 400 error if you send it (model-deprecations page, retrieved 2026-10-28). Older code you read will still have it.
- Wraps API call into simple interface
- Returns extracted text

**What it does:** "Simplify LLM calls to one line."

---

### Example 8: Error Handler

```python
def safe_search(query, fallback_response="No results found"):
    try:
        results = search_database(query)
        if not results:
            return fallback_response
        return results
    except Exception as error:
        print(f"Search failed: {error}")
        return fallback_response

# Using it - same call, handles errors inside
results = safe_search("What is RAG?")
```

**RECOGNIZE THIS:**
- `try/except` ← Error handling inside function
- Returns fallback if something goes wrong
- Caller doesn't need to worry about errors

**What it does:** "Protect search calls from crashing. Always returns something."

---

## Function Anatomy Reference

RECOGNIZE these parts:

| Part | Syntax | Role |
|:-----|:-------|:-----|
| Define | `def name():` | Build the tool |
| Parameters | `(param1, param2)` | Input slots |
| Default param | `(param=value)` | Optional input |
| Body | Indented lines | Tool logic |
| Return | `return result` | Output |
| Call | `name(argument)` | Use the tool |
| Named args | `name(key=value)` | Explicit inputs |

---

## Recognition Exercise: Read These Code Blocks

### Block 1
```python
def get_top_result(results, n=1):
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return sorted_results[:n]

top = get_top_result(search_results)
best_three = get_top_result(search_results, n=3)
```

**Questions:**
1. How many parameters? → 2 (one required, one optional)
2. What does it return? → List of top N results sorted by score
3. What does `n=3` do in second call? → Override default, get top 3

---

### Block 2
```python
def build_system_prompt(agent_name, role, guidelines):
    return f"""You are {agent_name}, a {role}.

Guidelines:
{guidelines}

Always respond clearly and concisely."""

prompt = build_system_prompt(
    agent_name="ResearchBot",
    role="research assistant",
    guidelines="- Cite sources\n- Be objective"
)
```

**Questions:**
1. Number of parameters? → 3
2. What does it return? → Formatted string (system prompt)
3. How is it called? → With named arguments

---

### Block 3
```python
def process_conversation_turn(history, user_message, llm_client):
    history.append({"role": "user", "content": user_message})
    response = llm_client.invoke(history)
    history.append({"role": "assistant", "content": response})
    return history, response
```

**Questions:**
1. What goes in? → history (list), user_message (string), llm_client (object)
2. What comes out? → Two values: updated history AND response
3. Pattern spotted? → Updates list, calls LLM, returns both

---

## Common AI Patterns (Recognition Cheat Sheet)

### Pattern: Formatter
```python
def format_X(input1, input2):
    result = combine(input1, input2)
    return result
```
**Recognize:** Takes separate pieces, returns combined string/dict

**Example call:**
```python
output = format_X("Hello", "World")
# → calls combine("Hello", "World") → returns combined result
```

---

### Pattern: Validator
```python
def is_valid_X(input):
    return condition is True/False
```
**Recognize:** Returns boolean, used in `if` statements

**Example call:**
```python
if is_valid_X(user_input):
    process(user_input)    # runs when True
else:
    print("Invalid input") # runs when False
```

---

### Pattern: Calculator
```python
def calculate_X(value, rate=default):
    return value * rate
```
**Recognize:** Math operation, optional rate/multiplier

**Example calls:**
```python
result = calculate_X(100)           # uses default rate
result = calculate_X(100, rate=2.5) # custom rate → 250
```

---

### Pattern: Pipeline Step
```python
def run_step(input):
    result = transform(input)
    return result
```
**Recognize:** One transformation, input → output

**Example call:**
```python
output = run_step("raw text")
# → calls transform("raw text") → returns processed result
```

---

### Pattern: Pipeline Orchestrator
```python
def full_pipeline(user_input):
    step1 = do_A(user_input)
    step2 = do_B(step1)
    step3 = do_C(step2)
    return step3
```
**Recognize:** Multiple steps chained, one entry + one exit

**Example call:**
```python
final = full_pipeline("What is RAG?")
# A("What is RAG?") → step1 result → B(step1) → step2 result → C(step2) → final answer
print(final)  # end result after all 3 steps ran
```

---

## Final Recognition Test

Look at this real AI code and identify the pattern:

```python
def create_rag_agent(model_name, vector_db, system_prompt, top_k=3, threshold=0.75):
    def agent(user_question):
        docs = vector_db.search(user_question, top_k=top_k)
        filtered = [d for d in docs if d["score"] >= threshold]

        if not filtered:
            return "I don't have enough information to answer that."

        context = "\n".join([d["text"] for d in filtered])
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_question}"}
        ]

        response = call_llm(messages, model=model_name)
        return response

    return agent

# Create and use
my_agent = create_rag_agent("claude-sonnet-5-5", my_db, "You are helpful.")
answer = my_agent("What is RAG?")
```

**RECOGNIZE:**
1. Outer function parameters? → 5 (2 optional)
2. Inner function? → `agent` is defined INSIDE `create_rag_agent`
3. `return agent` → Returns a FUNCTION (advanced pattern!)
4. Patterns combined? → L2 (if), L2.5 (filter loop), L1.5 (list), L3 (function)
5. Purpose? → Factory that creates customized agent functions

**This is:** Function factory + Full RAG pipeline inside a function

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** `def` definitions by sight (classic and type-hinted)
✓ **Identify** parameters and return values
✓ **Spot** default parameters
✓ **Understand** functions calling functions (pipelines)
✓ **See** L01-L04 patterns combined inside functions
✓ **Read** type hints (`param: str`, `-> list`) without confusion (2026 addition)

**Next:**
- **Pass C (Visual):** See functions as machines and pipelines
- **Pass 3 (Templates):** Copy and modify function patterns

**Remember:** When you read AI code, you'll think: "Oh, that's a prompt formatter" or "That's a full RAG pipeline function." If you see `-> list` after the parentheses — that just tells you what type comes out.

---

## Pro Tip: The 3-Second Rule

When you see a function:
1. **Second 1:** Read the name (tells you what it does)
2. **Second 2:** Check the parameters (inputs)
3. **Second 3:** Find the `return` (output)

Name + Inputs + Output = You understand the function. Done.
