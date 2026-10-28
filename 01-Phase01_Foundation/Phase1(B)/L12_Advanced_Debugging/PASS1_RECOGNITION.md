# Lesson 12 - Pass 1: RECOGNITION
## Learn to SEE Debugging Patterns in AI Code

**Goal:** By the end of this pass, you'll recognize the 4 bug categories, print audit patterns, retry patterns, and token audit patterns — WITHOUT writing any code.

---

## The Shape Recognition Method

Debugging code has distinctive VISUAL SHAPES. Learn to recognize them by sight.

> **Key insight:** Most AI bugs are NOT hard crashes. They're silent failures — code runs fine but returns wrong output. The patterns in this lesson are your tools for finding those invisible problems.

### Shape 1: The Print Audit Chain

```python
def process(input):
    print(f"STEP 1 INPUT: {input}")
    result_a = do_thing_a(input)
    print(f"STEP 2 RESULT: {result_a}")
    result_b = do_thing_b(result_a)
    print(f"STEP 3 RESULT: {result_b}")
    return result_b
```

**Visual Pattern:**
```
step = do_something()
print(f"LABEL: {step}")   ← audit print after every step
```

### Shape 2: The Retry Loop

```python
for attempt in range(max_retries):
    try:
        result = call_api()
        return result
    except SomeError:
        wait = 2 ** attempt
        time.sleep(wait)
```

**Visual Pattern:**
```
for attempt in range(N):
    try:
        ...
    except Error:
        time.sleep(2 ** attempt)   ← exponential backoff
```

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: The 4 Bug Categories

```
CATEGORY 1: Hard Errors
  → Code crashes, traceback appears
  → Easy to find and fix
  → Example: KeyError, AttributeError

CATEGORY 2: Silent Failures (most common)
  → Code runs fine, output is WRONG
  → "My RAG always returns the same generic answer"
  → "Confidence score is always 0.5"

CATEGORY 3: Intermittent Failures (hardest)
  → Works sometimes, fails sometimes
  → Rate limits, timeouts, empty results
  → "Fails on 1 in 10 queries"

CATEGORY 4: Performance Bugs (invisible)
  → Works correctly but costs too much
  → "Each query costs $0.50"
  → "Response takes 45 seconds"
```

**RECOGNIZE THIS:**
- Category 1 = has a traceback → use error decoder (L09)
- Categories 2–4 = no traceback → need debugging patterns from THIS lesson

---

### Example 2: Print Audit — Before and After

```python
# BEFORE (no visibility):
def answer(self, question):
    docs    = self.db.search(question)
    context = "\n".join([d["text"] for d in docs])
    prompt  = f"Context: {context}\nQ: {question}"
    return self.llm.invoke(prompt)

# AFTER (full audit trail):
def answer(self, question):
    print(f"\n{'='*50}")
    print(f"QUERY: {question}")

    docs = self.db.search(question)
    print(f"DOCS RETRIEVED: {len(docs)}")               # ← Is it finding docs?

    for i, d in enumerate(docs):
        print(f"  Doc {i}: score={d.get('score'):.3f}") # ← What are the scores?

    context = "\n".join([d["text"] for d in docs])
    print(f"CONTEXT LENGTH: {len(context)} chars")      # ← Is context empty?

    prompt = f"Context: {context}\nQ: {question}"
    print(f"PROMPT PREVIEW: {prompt[:200]}")            # ← What's sent to LLM?

    response = self.llm.invoke(prompt)
    print(f"RESPONSE: {response[:200]}")                # ← What did LLM return?
    return response
```

**RECOGNIZE THIS:**
- Print after EVERY major step
- Each print has a label (DOCS RETRIEVED, CONTEXT LENGTH, etc.)
- `[:200]` ← truncate long values so output stays readable
- `.get('score')` ← safe access in case key is missing

**What it does:** "Turn a black-box pipeline into a transparent pipeline."

---

### Example 3: What Print Audits Reveal

```
Common findings when you add print audits:

DOCS RETRIEVED: 0   → database is empty, or threshold too high
CONTEXT LENGTH: 0   → docs found but text extraction is wrong
PROMPT PREVIEW: "Context: \nQ: ..."  → context not included in prompt
RESPONSE: "I don't have information..." → LLM didn't receive context

Each finding points to one specific step that failed.
```

**RECOGNIZE THIS pattern:**
- Output is wrong → add prints → find which step breaks → fix that step
- Narrows from "something is broken" to "step 2 returns empty list"

---

### Example 4: LangChain verbose=True (Instant X-Ray)

```python
from langchain.agents import AgentExecutor

# Without verbose: silent — you see nothing
runner = AgentExecutor(agent=agent, tools=tools)

# With verbose=True: full trace
runner = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Output shows every step automatically:
# > Entering new AgentExecutor chain...
# > Thought: I need to search for X
# > Action: web_search
# > Action Input: "X"
# > Observation: [results]
# > Final Answer: ...
```

**RECOGNIZE THIS:**
- `verbose=True` ← one parameter to see everything
- Works on any LangChain chain or AgentExecutor
- No extra print statements needed

**What it does:** "Built-in debug mode for LangChain — flip one switch."

---

### Example 5: Rate Limit Retry Pattern

```python
import time
import anthropic

client = anthropic.Anthropic()

def call_with_retry(prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-5-5",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            wait = 2 ** attempt     # ← 1s, 2s, 4s (exponential)
            print(f"Rate limited. Waiting {wait}s... ({attempt+1}/{max_retries})")
            time.sleep(wait)

        except anthropic.APIStatusError as e:
            if e.status_code == 529:    # ← overloaded
                time.sleep(5)
            else:
                raise                   # ← re-raise unexpected errors

    raise Exception("Max retries exceeded")
```

**RECOGNIZE THIS:**
- `for attempt in range(max_retries):` ← retry loop (L04 pattern)
- `try/except` ← catches specific error types
- `2 ** attempt` ← exponential backoff: 1, 2, 4, 8 seconds
- `raise` alone ← re-raises current exception (keeps original traceback)
- Different `except` blocks ← handle rate limit and overload separately

**What it does:** "Automatic retry with increasing wait — handles rate limits in production."

---

### Example 6: Token Budget Audit

```python
def audit_token_usage(agent, test_queries: list):
    total_cost = 0

    for q in test_queries:
        response = agent.client.messages.create(
            model=agent.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": q}]
        )
        input_tokens  = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost          = input_tokens * 0.000002 + output_tokens * 0.00001
        total_cost   += cost

        print(f"Query: {q[:40]}")
        print(f"  Tokens: {input_tokens} in / {output_tokens} out")
        print(f"  Cost: ${cost:.4f}")

    print(f"\nTotal ({len(test_queries)} queries): ${total_cost:.4f}")
    print(f"Projected (1000 queries):  ${total_cost / len(test_queries) * 1000:.2f}")
```

**RECOGNIZE THIS:**
- `response.usage.input_tokens` ← token count from API response
- `response.usage.output_tokens` ← output token count
- Running total accumulated in a loop (L04)
- Projection math at the end: cost per query × volume

**What it does:** "Know your costs BEFORE deploying — run 10 queries, project to 10,000."

---

### Example 7: RAG Pipeline Stage Isolation

```python
def debug_rag_stages(agent, question: str):
    print(f"DEBUGGING: '{question}'")

    # Stage 1: Retrieval
    docs = agent.db.search(question)
    print(f"STAGE 1 — Found: {len(docs)} docs")
    if not docs:
        print("  PROBLEM: No documents found!")
        return        # ← stop here, no point checking further stages

    # Stage 2: Context
    context = "\n".join([d.get("text", "") for d in docs])
    print(f"STAGE 2 — Context: {len(context)} chars")
    if len(context) < 50:
        print("  PROBLEM: Context almost empty!")

    # Stage 3: Prompt
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    print(f"STAGE 3 — Prompt tokens: ~{len(prompt)//4}")

    # Stage 4: Generation
    answer = agent.llm.invoke(prompt)
    print(f"STAGE 4 — Answer: {answer[:200]}")
    return answer
```

**RECOGNIZE THIS:**
- 4 stages printed with explicit labels
- `if not docs: return` ← stop early if stage 1 already broken
- `len(context) < 50` ← detect near-empty context (L03 logic gate)
- `len(prompt)//4` ← rough token estimate (characters ÷ 4)

**What it does:** "Isolate which of the 4 RAG stages is failing — retrieval, context, prompt, or generation."

---

### Example 8: Silent Failure Pattern Library

```python
# Pattern 1: Agent always gives same generic answer
# Root cause: context not reaching LLM
# Debug: print the prompt before calling LLM
print(f"PROMPT:\n{prompt}")

# Pattern 2: Confidence score always 0.5
# Root cause: LLM output not parsed correctly
# Debug: print raw LLM response before parsing
print(f"RAW LLM OUTPUT: {raw_response}")

# Pattern 3: Agent loops forever
# Root cause: LLM not producing a stop signal
# Fix: add max_iterations
runner = AgentExecutor(agent=agent, tools=tools, max_iterations=5)

# Pattern 4: Costs 10x expected
# Root cause: sending full history every call
# Debug: print length of messages list each call
print(f"MESSAGES IN CONTEXT: {len(messages)}")

# Pattern 5: Agent ignores tools
# Root cause: tool description too vague
# Fix: improve description with when-to-use and when-NOT-to-use
```

**RECOGNIZE THIS:**
- Each symptom has a specific root cause
- Each root cause has a specific print statement to diagnose it
- Silent failures all have a "print the thing before it changes" fix

**What it does:** "Pattern matching for AI bugs — symptom → diagnosis → fix."

---

## Recognition Summary

When you see debugging code, ask:

### 1. What type of debug is it?
- Print statements after every step → print audit (silent failure)
- `try/except` with `time.sleep(2 ** attempt)` → retry with backoff (rate limits)
- `response.usage.input_tokens` → token cost tracking
- Stage labels with early `return` → RAG pipeline isolation

### 2. What problem is it solving?
- `len(docs) == 0` → retrieval problem
- `len(context) < 50` → context building problem
- `RateLimitError` → too many API calls
- `status_code == 529` → API overloaded
- `len(messages) > 20` → context window growing too large

### 3. What's the output for?
- `print(f"QUERY: {question}")` → trace input
- `print(f"DOCS: {len(docs)}")` → trace volume
- `print(f"PREVIEW: {thing[:200]}")` → trace content (truncated)

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** the 4 categories of AI bugs
✓ **Identify** print audit patterns by sight
✓ **Spot** retry with exponential backoff
✓ **Read** token cost audit code
✓ **Understand** RAG stage isolation
✓ **Match** symptoms to root causes

**Next:**
- **Pass C (Visual):** See debugging as a pipeline with checkpoints
- **Pass 3 (Templates):** Drop-in debug functions for any AI project

**Remember:** You're not memorizing. You're training your eyes to SEE patterns.

---

## Pro Tip: The 3-Second Rule

When you see unfamiliar debugging code:
1. **Second 1:** Is it print audits, retry logic, or cost tracking?
2. **Second 2:** What problem is it designed to catch?
3. **Second 3:** Which stage of the pipeline is it checking?

That's it. Debugging patterns are just checkpoints — find which checkpoint catches the problem.
