"""
═══════════════════════════════════════════════════════════════════
LESSON 10 CHEATSHEET: Advanced Debugging
═══════════════════════════════════════════════════════════════════
Debugging silent failures, performance issues, and LangChain-specific patterns.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. THE 4 CATEGORIES OF AI BUGS
# ═══════════════════════════════════════════════════════════
"""
Category 1: Hard Errors (traceback)    → error_decoder.md (L7)
Category 2: Silent Failures            → print audits (this lesson)
Category 3: Intermittent Failures      → retry + logging
Category 4: Performance Bugs           → token audit + timing
"""

# ═══════════════════════════════════════════════════════════
# 2. THE PRINT AUDIT TEMPLATE
# ═══════════════════════════════════════════════════════════
"""
Paste this INTO your failing function to trace every step:

def answer(self, question):
    print(f"INPUT: '{question}'")

    docs = self.db.search(question)
    print(f"DOCS: {len(docs)} found | first: {docs[0] if docs else 'EMPTY'}")

    context = "\\n".join([d["text"] for d in docs])
    print(f"CONTEXT: {len(context)} chars")

    prompt = f"Context: {context}\\nQ: {question}"
    print(f"PROMPT: {prompt[:200]}")

    response = self.llm.invoke(prompt)
    print(f"RESPONSE: {response[:200]}")

    return response

REMOVE prints when debugging is done.
"""

# ═══════════════════════════════════════════════════════════
# 3. LANGCHAIN DEBUG SWITCHES
# ═══════════════════════════════════════════════════════════
"""
SWITCH 1: verbose=True (instant, no setup)
  runner = AgentExecutor(agent=agent, tools=tools, verbose=True)
  → Shows every Thought/Action/Observation

SWITCH 2: return_intermediate_steps=True
  runner = AgentExecutor(..., return_intermediate_steps=True)
  result = runner.invoke({"input": "..."})
  for action, observation in result["intermediate_steps"]:
      print(f"Tool: {action.tool} | Input: {action.tool_input}")
      print(f"Result: {observation[:200]}")

SWITCH 3: LangSmith tracing (production)
  import os
  os.environ["LANGCHAIN_TRACING_V2"] = "true"
  os.environ["LANGCHAIN_API_KEY"] = "your-key"
  os.environ["LANGCHAIN_PROJECT"] = "my-project"
  → All LangChain calls traced at smith.langchain.com
"""

# ═══════════════════════════════════════════════════════════
# 4. SILENT FAILURE CAUSES (QUICK TABLE)
# ═══════════════════════════════════════════════════════════
"""
Symptom                          Root Cause                   Fix
────────────────────             ───────────────────────────  ─────────────────────
Always same generic answer       Context not in prompt        Print the prompt
RAG finds wrong docs             Embedding model mismatch     Use same model for ingest+query
Confidence always 0.5            LLM output not parsed        Print raw LLM response
Agent loops endlessly            Missing stop condition       Add max_iterations=5
Costs 10x expected               Full history sent each call  Use sliding window memory
Tools ignored                    Descriptions too vague        Rewrite tool descriptions
Streaming cuts off               max_tokens too low            Increase max_tokens
Embeddings slow on first call    Model loading each time       Load embedding model once in __init__
"""

# ═══════════════════════════════════════════════════════════
# 5. RATE LIMIT RETRY PATTERN
# ═══════════════════════════════════════════════════════════
import time
import anthropic

def call_with_retry(prompt: str, max_retries: int = 3) -> str:
    client = anthropic.Anthropic()
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-5-5",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except anthropic.RateLimitError:
            wait = 2 ** attempt   # 1s, 2s, 4s
            print(f"Rate limited. Waiting {wait}s...")
            time.sleep(wait)
        except anthropic.APIStatusError as e:
            if e.status_code == 529:
                time.sleep(5)
            else:
                raise
    raise RuntimeError("Max retries exceeded")

# ═══════════════════════════════════════════════════════════
# 6. STAGE ISOLATION — WHICH PART BROKE?
# ═══════════════════════════════════════════════════════════
"""
RAG PIPELINE STAGES — test each independently:

Stage 1: Retrieval
  docs = db.search("your question")
  print(f"Found: {len(docs)} docs")
  print(f"Scores: {[d.get('score') for d in docs]}")
  → if 0 docs: threshold too high, db empty, or bad embedding

Stage 2: Context
  context = "\\n".join([d["text"] for d in docs])
  print(f"Context: {len(context)} chars")
  → if empty: wrong key ("text" vs "page_content" vs "content")

Stage 3: Prompt
  prompt = f"Context: {context}\\nQ: {question}"
  print(prompt)
  → read it — does it make sense? Is context actually there?

Stage 4: Generation
  response = llm.invoke(prompt)
  print(response)
  → is it answering the question or being generic?
"""

# ═══════════════════════════════════════════════════════════
# 7. TYPE DIAGNOSTIC TOOLKIT
# ═══════════════════════════════════════════════════════════
def diagnose(var, label="?"):
    """Quick type + value check for any variable."""
    t = type(var).__name__
    if isinstance(var, dict):
        print(f"[{label}] dict with keys: {list(var.keys())}")
    elif isinstance(var, list):
        print(f"[{label}] list len={len(var)}, first={repr(var[0])[:60] if var else 'EMPTY'}")
    elif isinstance(var, str):
        print(f"[{label}] str len={len(var)}: {repr(var[:80])}")
    else:
        print(f"[{label}] {t}: {repr(var)[:80]}")

# Usage (paste before failing line):
# diagnose(response, "llm response")
# diagnose(docs, "search results")

# ═══════════════════════════════════════════════════════════
# END
# ═══════════════════════════════════════════════════════════
print("Debug cheatsheet loaded!")
print("Rule: Silent failure → print every stage → find where it breaks.")
