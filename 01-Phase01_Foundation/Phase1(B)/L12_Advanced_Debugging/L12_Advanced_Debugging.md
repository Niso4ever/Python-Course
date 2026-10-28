# Lesson 12: Advanced Debugging
## The Detective Theory

> **Version note (checked 2026-10-28):** The LangChain agent code in this lesson is LangChain 0.x style (`from langchain.agents import AgentExecutor, create_react_agent`). You will still meet it in older repos. In LangChain 1.x those legacy pieces live in the separate `langchain-classic` package (`from langchain_classic.agents import AgentExecutor, create_react_agent`), and new code builds agents with `from langchain.agents import create_agent`. The loop you are learning to read is the same.

In L09 you learned to read a fire alarm (error type → fix). Now you become a **detective** — debugging problems that *don't* have a clear error message. The code runs, nothing crashes, but the output is wrong. Or it works sometimes and fails silently others.

This is where 80% of real AI debugging happens. Errors are easy. Subtle failures are hard.

---

## 1. The 4 Categories of AI Bugs

```
CATEGORY 1: Hard Errors (L7 territory)
  → Traceback appears, code crashes
  → Easy to find, fix with error_decoder.md

CATEGORY 2: Silent Failures (most common in AI)
  → Code runs fine, output is wrong or empty
  → "My RAG agent always returns the same answer"
  → "The confidence score is always 0.5"

CATEGORY 3: Intermittent Failures (hardest)
  → Works sometimes, fails sometimes
  → Rate limits, network timeouts, empty search results
  → "My agent fails on 1 in 10 queries"

CATEGORY 4: Performance Bugs (invisible)
  → Works correctly but too slow or too expensive
  → "Each query costs $0.50 — budget explodes overnight"
  → "The chatbot takes 45 seconds to respond"
```

---

## 2. Debugging Silent Failures — The Print Audit

When code runs without error but gives wrong output, insert print statements at every step:

```python
# BEFORE DEBUG — broken but no error:
def answer(self, question):
    docs    = self.db.search(question)
    context = "\n".join([d["text"] for d in docs])
    prompt  = f"Context: {context}\nQ: {question}"
    return self.llm.invoke(prompt)

# AFTER DEBUG — full audit trail:
def answer(self, question):
    print(f"\n{'='*50}")
    print(f"QUERY: {question}")

    docs = self.db.search(question)
    print(f"DOCS RETRIEVED: {len(docs)}")          # ← Is it finding docs?
    for i, d in enumerate(docs):
        print(f"  Doc {i}: score={d.get('score', '?'):.3f} | text={d['text'][:60]}")

    context = "\n".join([d["text"] for d in docs])
    print(f"CONTEXT LENGTH: {len(context)} chars")  # ← Is context empty?

    prompt = f"Context: {context}\nQ: {question}"
    print(f"PROMPT PREVIEW: {prompt[:200]}")        # ← What's actually sent?

    response = self.llm.invoke(prompt)
    print(f"RESPONSE: {response[:200]}")            # ← What did LLM return?
    return response
```

**The insight:** Print audits reveal WHERE the pipeline breaks. Usually one of:
- `docs = 0` → search returning nothing (threshold too high, empty db)
- `context = ""` → docs found but text extraction is wrong
- `prompt` looks wrong → formatting issue
- `response` is generic → prompt didn't include context properly

---

## 3. LangChain-Specific Debugging Patterns

### Enable verbose mode (instant X-ray):
```python
from langchain.agents import AgentExecutor

# Add verbose=True to see EVERY step:
runner = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Output will show:
# > Entering new AgentExecutor chain...
# > Thought: I need to search for X
# > Action: web_search
# > Action Input: "X"
# > Observation: [search results]
# > Final Answer: ...
```

### Use LangSmith for tracing (production-grade):
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"]    = "your-langsmith-key"
os.environ["LANGCHAIN_PROJECT"]    = "my-rag-project"

# Now EVERY LangChain call is traced in the LangSmith dashboard
# You see: inputs, outputs, latency, token counts, errors
# URL: smith.langchain.com
```

### Inspect the chain's intermediate steps:
```python
runner = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True   # ← captures all reasoning steps
)
result = runner.invoke({"input": "What is RAG?"})

# Now you can inspect each step:
for step in result["intermediate_steps"]:
    action, observation = step
    print(f"Tool: {action.tool}")
    print(f"Input: {action.tool_input}")
    print(f"Output: {observation[:200]}")
```

---

## 4. Rate Limits & Retry Patterns

The most common intermittent failure in AI projects:

```
anthropic.RateLimitError: 429 Too Many Requests
→ You're sending too many API calls per minute
→ Happens during batch processing or parallel calls

anthropic.APIStatusError: 529 Overloaded
→ Anthropic's servers are under heavy load
→ Retry with exponential backoff
```

**The retry pattern — recognize this in production code:**
```python
import anthropic
import time

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
            wait = 2 ** attempt   # exponential backoff: 1s, 2s, 4s
            print(f"Rate limited. Waiting {wait}s... (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)

        except anthropic.APIStatusError as e:
            if e.status_code == 529:   # overloaded
                time.sleep(5)
            else:
                raise   # re-raise unexpected errors

    raise Exception("Max retries exceeded")
```

**What to notice:**
- `2 ** attempt` = exponential backoff (1, 2, 4, 8 seconds between retries)
- `raise` alone re-raises the current exception (keeps the original traceback)
- Specific error types caught separately — `RateLimitError` vs `APIStatusError`

---

## 5. The Token Budget Audit

Your RAG agent works in testing (5 queries) then breaks in production (500 queries):

```python
def audit_token_usage(agent, test_queries: list):
    """Run a batch and report cost + performance."""
    results = []
    total_input  = 0
    total_output = 0

    for q in test_queries:
        response = agent.client.messages.create(
            model=agent.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": q}]
        )
        input_tokens  = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_input  += input_tokens
        total_output += output_tokens

        results.append({
            "query":         q[:50],
            "input_tokens":  input_tokens,
            "output_tokens": output_tokens,
            "cost_usd":      input_tokens * 0.000002 + output_tokens * 0.00001
        })

    print(f"\nToken Audit ({len(test_queries)} queries):")
    print(f"  Total input:  {total_input:,} tokens")
    print(f"  Total output: {total_output:,} tokens")
    print(f"  Total cost:   ${(total_input * 0.000002 + total_output * 0.00001):.4f}")
    print(f"  Avg per query: ${(total_input * 0.000002 + total_output * 0.00001) / len(test_queries):.4f}")
    return results
```

**Insight:** Run this on 10 test queries, multiply by your expected volume. If 10 queries cost $0.05, 10,000 queries cost $50/day. Know before you deploy.

---

## 6. Debugging the RAG Pipeline — Stage by Stage

When a RAG answer is wrong, isolate WHICH stage failed:

```python
def debug_rag_stages(agent, question: str):
    print(f"\n{'='*60}")
    print(f"DEBUGGING: '{question}'")
    print('='*60)

    # Stage 1: Retrieval
    docs = agent.db.search(question, top_k=agent.top_k)
    print(f"\nSTAGE 1 — RETRIEVAL:")
    print(f"  Found: {len(docs)} documents")
    if not docs:
        print("  ⚠ PROBLEM: No documents found!")
        print("  → Check: Is the database populated?")
        print("  → Check: Is the query too specific?")
        print("  → Check: Is the embedding model the same as ingestion?")
        return

    for i, d in enumerate(docs):
        score = d.get("score", d.get("distance", "?"))
        print(f"  Doc {i+1}: score={score} | {str(d.get('text', d))[:80]}")

    # Stage 2: Context Building
    context = "\n".join([d.get("text", str(d)) for d in docs])
    print(f"\nSTAGE 2 — CONTEXT:")
    print(f"  Length: {len(context)} chars / ~{len(context)//4} tokens")
    if len(context) < 50:
        print("  ⚠ PROBLEM: Context is almost empty!")
    print(f"  Preview: {context[:200]}")

    # Stage 3: Prompt
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    print(f"\nSTAGE 3 — PROMPT:")
    print(f"  Total length: ~{len(prompt)//4} tokens")
    print(f"  Full prompt:\n{prompt[:500]}")

    # Stage 4: Generation
    print(f"\nSTAGE 4 — GENERATION:")
    answer = agent.llm.invoke(prompt)
    print(f"  Answer: {answer}")

    return answer
```

---

## 7. Common Silent Failures in AI — Pattern Library

| Symptom | Root Cause | Fix |
|:--------|:-----------|:----|
| Agent always gives same generic answer | Context not reaching LLM (prompt format wrong) | Print the prompt before sending |
| RAG returns irrelevant docs | Embedding model mismatch (different model used to ingest vs query) | Use same embedding model everywhere |
| Confidence scores always 0.5 | LLM output not parsed correctly | Print raw LLM response before parsing |
| Agent loops forever | LLM not calling stop token / tool not returning properly | Add `max_iterations` to AgentExecutor |
| Costs 10x expected | Sending full conversation history on every call | Trim history, use sliding window |
| Agent ignores tools | Tool description too vague | Improve tool description — LLM decides by reading it |
| Streaming cuts off | `max_tokens` too low | Increase `max_tokens` |
| Embeddings are slow | Embedding model downloading on every startup | Cache the model, load once |

---

## 8. Key Takeaways

✓ **Print audits** = your main tool for silent failures — trace every stage
✓ **`verbose=True`** = instant X-ray for any LangChain chain or agent
✓ **Rate limits** = expected in production — always add retry with backoff
✓ **Token audits** = run before deploying at scale — know your costs
✓ **Stage isolation** = debug RAG by checking retrieval, context, prompt, generation separately
✓ **Most AI "bugs"** are actually data problems: wrong keys, empty lists, bad prompt format
✓ Remove debug prints when done — production code should be clean

**Phase 1B Insight:** The best AI engineers don't write perfect code — they build systems that *show their work* through logging and observability. A RAG agent that prints its retrieval scores is far easier to debug than one that returns a black-box answer.

---

## Templates Available

See this lesson folder ([./](./)) for:
- `CHEATSHEET_L12.py` — debugging toolkit: print audits, retry, token tracking
- `template_debug_toolkit.py` — drop-in debug functions for any AI project
