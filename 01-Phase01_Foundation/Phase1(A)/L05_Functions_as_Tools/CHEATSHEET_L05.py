"""
═══════════════════════════════════════════════════════════════════
LESSON 05 CHEATSHEET: Functions (def) as Tools
═══════════════════════════════════════════════════════════════════

Quick reference for function patterns in AI systems.
Keep this open while coding!

Python 3.13 / 2026 context:
  def fn(param):           → classic style (still valid)
  def fn(param: str) -> str: → 2026 style with TYPE HINTS on args + return

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. DEFINE A FUNCTION
# ═══════════════════════════════════════════════════════════

def function_name(parameter):
    # Logic here
    return result

# Example:
def summarize(text):
    return text[:50] + "..."


# ═══════════════════════════════════════════════════════════
# 1B. TYPE HINTS ON FUNCTIONS (2026 standard)
# ═══════════════════════════════════════════════════════════

# RECOGNIZE this shape:  def name(param: type) -> return_type:

# Old style (still valid):
def summarize(text):
    return text[:50] + "..."

# 2026 style (same logic — adds type labels on params and return):
def summarize(text: str) -> str:
    return text[:50] + "..."

# More real AI examples:
def count_tokens(text: str) -> int:
    return len(text) // 4

def calculate_cost(tokens: int, rate: float = 0.000015) -> float:
    return tokens * rate

def validate_query(query: str, min_length: int = 5) -> bool:
    return len(query) >= min_length

def search_docs(query: str, top_k: int = 3) -> list:
    return vector_db.search(query, k=top_k)

# HOW TO READ TYPE HINTS:
#   param: str    ← this input expects text
#   param: int    ← this input expects a whole number
#   param: float  ← this input expects a decimal
#   -> str        ← function outputs text
#   -> bool       ← function outputs True/False
#   -> list       ← function outputs a list
#   -> dict       ← function outputs a dictionary
#   -> None       ← function returns nothing

# You DO NOT need to write type hints. You just need to RECOGNIZE them.


# ═══════════════════════════════════════════════════════════
# 2. CALL A FUNCTION
# ═══════════════════════════════════════════════════════════

result = function_name(argument)

# Example:
short = summarize("The history of the world is...")


# ═══════════════════════════════════════════════════════════
# 3. MULTIPLE PARAMETERS
# ═══════════════════════════════════════════════════════════

def format_prompt(question, context):
    return f"Context: {context}\nQuestion: {question}"

# Call with multiple args:
prompt = format_prompt("What is AI?", "AI is artificial intelligence...")


# ═══════════════════════════════════════════════════════════
# 4. DEFAULT PARAMETERS (Optional inputs)
# ═══════════════════════════════════════════════════════════

def search(query, top_k=3, threshold=0.80):
    # top_k and threshold are optional
    pass

# Call options:
search("AI")                         # uses defaults (3, 0.80)
search("AI", top_k=5)               # custom top_k
search("AI", top_k=5, threshold=0.9)# override both


# ═══════════════════════════════════════════════════════════
# 5. RETURN VALUES
# ═══════════════════════════════════════════════════════════

# Return single value
def count_tokens(text):
    return len(text) / 4

# Return dictionary
def analyze(response):
    return {
        "length": len(response),
        "is_long": len(response) > 100
    }

# Use returned dict
analysis = analyze("Hello world")
print(analysis["is_long"])  # False


# ═══════════════════════════════════════════════════════════
# 6. FUNCTIONS CALLING FUNCTIONS (Pipeline)
# ═══════════════════════════════════════════════════════════

def step_one(input):
    return process(input)

def step_two(data):
    return transform(data)

def pipeline(user_input):
    result1 = step_one(user_input)  # Call step 1
    result2 = step_two(result1)     # Pass output to step 2
    return result2                   # Return final result


# ═══════════════════════════════════════════════════════════
# 7. NAMED ARGUMENTS (Explicit calling)
# ═══════════════════════════════════════════════════════════

def format_result(question, answer, confidence):
    return {"q": question, "a": answer, "c": confidence}

# Positional (order matters):
result = format_result("What?", "This.", 0.9)

# Named (order doesn't matter, more readable):
result = format_result(
    question="What?",
    answer="This.",
    confidence=0.9
)


# ═══════════════════════════════════════════════════════════
# 8. COMMON AI FUNCTION PATTERNS
# ═══════════════════════════════════════════════════════════

# Pattern: Formatter
def format_X(part1, part2):
    return f"Combined: {part1} + {part2}"

# Pattern: Validator (returns True/False)
def is_valid_X(input, min_len=5):
    return len(input) >= min_len

# Pattern: Calculator
def calculate_cost(tokens, rate=0.000015):
    return tokens * rate

# Pattern: Pipeline step
def process_docs(docs, threshold=0.80):
    return [d for d in docs if d["score"] >= threshold]

# Pattern: Packager (returns dict)
def package_result(question, answer, sources):
    return {"question": question, "answer": answer, "sources": sources}

# Pattern: Caller (wraps API)
def call_llm(prompt, model="claude-sonnet-5-5"):
    # ... API call here
    return response_text

# Pattern: Safe wrapper
def safe_search(query, fallback="Not found"):
    try:
        return search_database(query)
    except Exception as e:
        print(f"Error: {e}")
        return fallback


# ═══════════════════════════════════════════════════════════
# 9. RAG PIPELINE SKELETON
# ═══════════════════════════════════════════════════════════

def rag_pipeline(question, db, llm):
    docs     = db.search(question)           # Step 1: Retrieve
    context  = build_context(docs)           # Step 2: Format
    prompt   = format_rag_prompt(question, context)  # Step 3: Build prompt
    answer   = llm.invoke(prompt)            # Step 4: Generate
    return package_result(question, answer, docs)    # Step 5: Package


# ═══════════════════════════════════════════════════════════
# 10. FUNCTION ANATOMY QUICK REFERENCE
# ═══════════════════════════════════════════════════════════

"""
def name(required, optional=default):  ← DEFINE
    ← 4 SPACE INDENT (body belongs to function)
    logic here
    return output                      ← OUTPUT

result = name(arg, optional=value)    ← CALL
"""


# ═══════════════════════════════════════════════════════════
# 11. WHEN TO USE FUNCTIONS
# ═══════════════════════════════════════════════════════════

"""
Use def when:
✓ Same logic needed in 2+ places
✓ Want to name and organize logic
✓ Building a pipeline step
✓ Wrapping an API call
✓ Making code readable

Don't use def for:
✗ Logic used exactly once → inline is fine
✗ Extremely simple one-liners → use lambda
✗ Managing agent state → use class (Lesson 06)
"""


# ═══════════════════════════════════════════════════════════
# 12. INDENTATION RULES
# ═══════════════════════════════════════════════════════════

# ✓ CORRECT:
def my_function(input):
    step1 = process(input)   # 4 spaces
    step2 = transform(step1) # 4 spaces
    return step2              # 4 spaces

# ✗ WRONG:
def my_function(input):
step1 = process(input)  # No indent = ERROR!


# ═══════════════════════════════════════════════════════════
# 13. 3-SECOND FUNCTION READ
# ═══════════════════════════════════════════════════════════

"""
When you see a function:
1. READ the name        → tells you WHAT it does
2. CHECK parameters     → tells you WHAT goes IN
3. FIND return          → tells you WHAT comes OUT

That's all you need. Done.
"""


# ═══════════════════════════════════════════════════════════
# 14. TEMPLATE QUICK LINKS
# ═══════════════════════════════════════════════════════════

"""
Available templates in this folder:
- template_prompt_formatter.py  → Build LLM prompts
- template_rag_pipeline.py      → Full RAG flow
- template_llm_caller.py        → Call Claude API
"""


# ═══════════════════════════════════════════════════════════
# 15. PATTERNS COMBINED (L1-L3 Together)
# ═══════════════════════════════════════════════════════════

def process_rag_results(docs, threshold=0.80, max_results=3):
    # L04: Loop (inside L05 function)
    filtered = []
    for doc in docs:
        # L03: if/else (inside L05 function)
        if doc["score"] >= threshold:
            # L02: append to list
            filtered.append(doc)
            # L03: check limit
            if len(filtered) >= max_results:
                break

    # L01: return dict
    return {
        "results": filtered,
        "count": len(filtered),
        "top_score": filtered[0]["score"] if filtered else 0
    }


# ═══════════════════════════════════════════════════════════
# END OF CHEATSHEET
# ═══════════════════════════════════════════════════════════

print("Keep this cheatsheet open while coding!")
print("Copy patterns as needed - don't memorize!")
