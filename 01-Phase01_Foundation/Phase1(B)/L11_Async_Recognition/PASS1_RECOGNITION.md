# Pass 1: Recognition — Async Patterns
## Read These 8 Examples — Don't Write Them

**Goal:** See `async/await` in AI code and immediately know what it's doing and why.

---

## Example 1: Sync vs Async Side by Side

```python
# SYNCHRONOUS (normal Python):
def get_answer(question: str) -> str:
    response = client.messages.create(   # ← blocks here until API responds
        model="claude-sonnet-5-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# ASYNCHRONOUS (async Python):
async def get_answer(question: str) -> str:
    response = await client.messages.create(  # ← pauses here, lets other work run
        model="claude-sonnet-5-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text
```

**What changes:** `def` → `async def`, call → `await call`. That's literally it.
**Why it matters:** The sync version freezes your program. The async version lets other tasks run during the wait.

---

## Example 2: asyncio.gather — The Speed Multiplier

```python
import asyncio
import anthropic

client = anthropic.AsyncAnthropic()

async def summarize(doc: str) -> str:
    response = await client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Summarize: {doc}"}]
    )
    return response.content[0].text

async def summarize_all(documents: list[str]) -> list[str]:
    tasks = [summarize(doc) for doc in documents]   # ← create list of coroutines
    results = await asyncio.gather(*tasks)           # ← run ALL simultaneously
    return list(results)                             # ← list of results in same order

# Entry point:
summaries = asyncio.run(summarize_all(["Doc A...", "Doc B...", "Doc C..."]))
```

**What to notice:**
- `tasks = [func(x) for x in items]` → creates a list of "pending" coroutines
- `*tasks` → the `*` unpacks the list into separate arguments
- `asyncio.gather(*tasks)` → runs all coroutines simultaneously
- Results come back in the SAME ORDER as inputs (even if they finish out of order)

---

## Example 3: LangChain Async Methods (the `a` prefix)

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
import asyncio

llm = ChatAnthropic(model="claude-sonnet-5-5")

# SYNC version (one at a time):
response = llm.invoke([HumanMessage(content="What is RAG?")])

# ASYNC version (can run in parallel):
async def ask_parallel(questions: list[str]):
    tasks = [
        llm.ainvoke([HumanMessage(content=q)])   # .ainvoke = async invoke
        for q in questions
    ]
    responses = await asyncio.gather(*tasks)
    return [r.content for r in responses]

asyncio.run(ask_parallel(["What is RAG?", "What is DSPy?", "What is CrewAI?"]))
```

**The LangChain async naming pattern:**
- `.invoke()` → `.ainvoke()`
- `.stream()` → `.astream()`
- `.batch()` → `.abatch()`
- `.embed_documents()` → `.aembed_documents()`

---

## Example 4: Streaming — async for

```python
import anthropic
import asyncio

client = anthropic.AsyncAnthropic()

async def stream_to_terminal(prompt: str):
    async with client.messages.stream(         # ← async context manager
        model="claude-sonnet-5-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for chunk in stream.text_stream:  # ← async loop (new token each iteration)
            print(chunk, end="", flush=True)    # print each token as it arrives
    print()  # newline at end

asyncio.run(stream_to_terminal("Explain async/await in 3 sentences."))
```

**What to notice:**
- `async with` → async context manager (streaming connection stays open)
- `async for chunk in stream` → loop that waits for each token
- `flush=True` → immediately displays each character (no buffering)

---

## Example 5: FastAPI — Async in Production Web Services

```python
# FastAPI uses async by default — you'll see this in production AI APIs:
from fastapi import FastAPI
from langchain_anthropic import ChatAnthropic

app = FastAPI()
llm = ChatAnthropic(model="claude-sonnet-5-5")

@app.post("/chat")
async def chat_endpoint(question: str) -> dict:   # ← async def for web handler
    response = await llm.ainvoke([               # ← await inside async endpoint
        {"role": "user", "content": question}
    ])
    return {"answer": response.content}
```

**What to notice:** FastAPI web handlers are `async def` — this lets the server handle many requests simultaneously without blocking. When you review production AI APIs, expect `async def` everywhere.

---

## Example 6: Async with Error Handling

```python
import asyncio
import anthropic

client = anthropic.AsyncAnthropic()

async def safe_call(prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            response = await client.messages.create(
                model="claude-sonnet-5-5",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limited. Waiting {wait}s...")
            await asyncio.sleep(wait)   # ← async sleep (non-blocking!)

        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    return "Max retries reached"
```

**What to notice:** `await asyncio.sleep(wait)` — even sleeping is async. Regular `time.sleep()` in async code would block everything; `asyncio.sleep()` allows other tasks to run during the wait.

---

## Example 7: Parallel RAG — Real Production Pattern

```python
import asyncio
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

async def parallel_rag(questions: list[str], db, llm) -> list[str]:
    """Answer multiple RAG questions in parallel."""

    async def single_rag(question: str) -> str:
        # Search is often sync — wrap with asyncio.to_thread for true async:
        docs    = await asyncio.to_thread(db.similarity_search, question, k=3)
        context = "\n".join([d.page_content for d in docs])
        prompt  = f"Context: {context}\nQ: {question}"
        response = await llm.ainvoke([{"role": "user", "content": prompt}])
        return response.content

    # All questions run simultaneously:
    results = await asyncio.gather(*[single_rag(q) for q in questions])
    return list(results)
```

**Insight:** `asyncio.to_thread()` wraps sync functions to run them in async code without blocking. This is how you use sync libraries (like many vector stores) in an async pipeline.

---

## Example 8: DSPy Async (Recognizing the Pattern)

```python
import dspy
import asyncio

# DSPy 2.x has async support:
lm = dspy.LM("anthropic/claude-sonnet-5-5")
dspy.configure(lm=lm)

class QA(dspy.Signature):
    question: str = dspy.InputField()
    answer:   str = dspy.OutputField()

predictor = dspy.Predict(QA)

async def batch_qa(questions: list[str]) -> list[str]:
    # Create async tasks for all questions:
    tasks = [
        asyncio.to_thread(predictor, question=q)
        for q in questions
    ]
    results = await asyncio.gather(*tasks)
    return [r.answer for r in results]

answers = asyncio.run(batch_qa(["What is RAG?", "What is DSPy?", "What is a vector?"]))
```

---

## Pattern Summary

| What you see | What it means |
|:-------------|:--------------|
| `async def func()` | Function can pause/resume — must be awaited or gathered |
| `await operation()` | Pause here, let other work run, continue when done |
| `asyncio.gather(*tasks)` | Run all tasks simultaneously — the speed multiplier |
| `asyncio.run(main())` | Start the async engine — called once at the top level |
| `async for item in stream` | Streaming loop — process each token/chunk as it arrives |
| `async with context:` | Async context manager (streaming connections) |
| `.ainvoke()` / `.astream()` | LangChain async method (the `a` prefix) |
| `asyncio.sleep(n)` | Non-blocking sleep — use this instead of time.sleep() in async code |
| `asyncio.to_thread(func, args)` | Run a sync function without blocking async code |
