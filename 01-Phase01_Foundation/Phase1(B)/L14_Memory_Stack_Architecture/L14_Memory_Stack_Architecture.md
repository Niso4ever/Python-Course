# Lesson 14: Memory Stack Architecture

**Estimated time: 45 minutes**

---

## The Goldfish vs Elephant Theory

Every AI conversation is, by default, a **goldfish** — it lives entirely in short-term memory and forgets everything when you close the tab.

```
Default behavior (no memory):
  Turn 1: "My name is Alex."    → LLM: "Nice to meet you, Alex!"
  [new session]
  Turn 1: "What's my name?"     → LLM: "I don't know your name."
```

The goldfish has no past. Memory systems give AI an **elephant's memory** — the ability to remember across sessions, across documents, across time.

The memory *stack* is the engineering decision of which type of elephant you build.

---

## The Four Layers of Memory

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 4: EPISODIC (Long-term, Persistent)               │
│  "What happened in previous sessions"                    │
│  → Database, files, user profiles                        │
├──────────────────────────────────────────────────────────┤
│  LAYER 3: SEMANTIC (Knowledge, Facts)                    │
│  "Things the agent was told to know forever"             │
│  → Vector database, RAG, knowledge graph                 │
├──────────────────────────────────────────────────────────┤
│  LAYER 2: WORKING (Current conversation)                 │
│  "What happened in this session"                         │
│  → Message history list, summarization                   │
├──────────────────────────────────────────────────────────┤
│  LAYER 1: CONTEXT WINDOW (Right now)                     │
│  "What the LLM can see at this exact moment"             │
│  → The messages list sent to the API                     │
└──────────────────────────────────────────────────────────┘
```

Most AI systems only use Layer 1. Production AI systems stack all four.

---

## Layer 1: The Context Window

This is the **only memory the LLM actually has**. Everything else is your code shipping information into this window.

```python
# This IS the LLM's memory. All of it.
messages = [
    {"role": "user",      "content": "My name is Alex."},
    {"role": "assistant", "content": "Nice to meet you, Alex!"},
    {"role": "user",      "content": "What's my name?"},
    # ↑ LLM sees all 3 turns and answers correctly
]
```

**The limit:** Context windows have token limits.
- Claude Haiku 5.5: 1M tokens ≈ 555,000 words (models overview, retrieved 2026-10-28)
- Claude Sonnet 5.5: 1M tokens
- Claude Opus 5.5: 1M tokens

**The problem:** Even 200K fills up in long agent sessions. When it fills up, the oldest messages fall off — the goldfish returns.

---

## Layer 2: Working Memory Patterns

### Pattern A: Full History (Simple)

```python
# Accumulate every turn — simple but fills up eventually
class SimpleMemoryAgent:
    def __init__(self):
        self.history = []   # ← working memory

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        response = client.messages.create(
            model="claude-sonnet-5-5",
            messages=self.history   # ← entire history sent every time
        )
        self.history.append({"role": "assistant", "content": response_text})
        return response_text
```

**When to use:** Short conversations, demos, prototypes.
**When it breaks:** Long agent sessions (100+ turns) or large documents in history.

---

### Pattern B: Sliding Window (Fixed Size)

```python
# Keep only the last N turns in context
class SlidingWindowAgent:
    def __init__(self, window_size=10):
        self.history     = []   # full history (for logging)
        self.window_size = window_size

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        # Only send last N turns to LLM ← the "sliding window"
        recent = self.history[-self.window_size:]

        response = client.messages.create(
            model="claude-sonnet-5-5",
            messages=recent   # ← truncated window, not full history
        )
        self.history.append({"role": "assistant", "content": response_text})
        return response_text
```

**The tradeoff:** LLM only sees the last 10 turns. Things said in turn 1 are forgotten by turn 11.
**When to use:** Customer support bots, task-focused sessions where early context doesn't matter.

---

### Pattern C: Summarization Memory (Compress + Keep)

```python
# When history gets long → summarize old turns → keep recent ones
class SummarizationAgent:
    def __init__(self, max_turns=20, summary_every=10):
        self.history      = []
        self.summary      = ""   # ← compressed old history
        self.max_turns    = max_turns
        self.summary_every = summary_every

    def _summarize(self):
        """Compress old turns into a summary paragraph."""
        old_turns = self.history[:-5]  # keep last 5 turns raw
        text = "\n".join(f"{m['role']}: {m['content']}" for m in old_turns)

        summary_response = client.messages.create(
            model="claude-haiku-5-5",   # cheap model for summarizing
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation in 3 sentences:\n{text}"
            }]
        )
        self.summary  = summary_response.content[0].text
        self.history  = self.history[-5:]   # discard old, keep last 5

    def chat(self, user_input):
        if len(self.history) >= self.summary_every:
            self._summarize()

        # Build context: summary + recent turns
        messages = []
        if self.summary:
            messages.append({
                "role": "user",
                "content": f"[Conversation so far: {self.summary}]"
            })
            messages.append({
                "role": "assistant",
                "content": "Understood, I have that context."
            })
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})
        # ... make API call
```

**The tradeoff:** Some detail is lost in the summary. Recent turns stay sharp.
**When to use:** Long conversations where gist matters more than exact wording.

---

## Layer 3: Semantic Memory (Vector Database)

This is where **RAG** (Retrieval-Augmented Generation) lives. Instead of putting 500 documents in context, you:

1. **Store** documents as vector embeddings in a database
2. **Retrieve** only the relevant passages at query time
3. **Inject** those passages into the context window

```python
# The memory lookup pattern (reads like: "search → inject → answer")
def answer_with_knowledge(user_question: str) -> str:
    # Step 1: Search semantic memory
    relevant_docs = vector_db.similarity_search(
        user_question,
        k=3   # top 3 most relevant chunks
    )

    # Step 2: Build context with retrieved knowledge
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    # Step 3: LLM answers using retrieved knowledge
    response = client.messages.create(
        model="claude-sonnet-5-5",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {user_question}"
        }]
    )
    return response.content[0].text
```

**Why this matters:** A company's entire documentation library can be "remembered" — but only the relevant parts are fetched. The LLM gets a targeted slice, not the whole library.

---

## Layer 4: Episodic Memory (Persistent Across Sessions)

```python
# Save and load user history between sessions
import json, os

class PersistentAgent:
    def __init__(self, user_id: str):
        self.user_id  = user_id
        self.filepath = f"memory_{user_id}.json"
        self.profile  = self._load()

    def _load(self) -> dict:
        """Load memory from disk. Returns empty dict if new user."""
        if os.path.exists(self.filepath):
            with open(self.filepath) as f:
                return json.load(f)
        return {"name": None, "preferences": {}, "past_topics": []}

    def _save(self):
        """Persist memory to disk after every turn."""
        with open(self.filepath, "w") as f:
            json.dump(self.profile, f)

    def remember(self, key: str, value):
        self.profile[key] = value
        self._save()   # ← immediate persistence

    def recall(self, key: str):
        return self.profile.get(key)
```

**Real-world use:** Users who come back next week are greeted by name, their preferences are remembered, their history is retrievable.

---

## Reading Memory Code in the Wild

When you open a production AI codebase, look for these signals:

```
You see this                          It means this
────────────────────────────────────  ────────────────────────────────────────
self.history = []                     Working memory (Layer 2)
messages[-N:]                         Sliding window pattern
_summarize() method                   Summarization memory pattern
vector_db.similarity_search()         Semantic memory (RAG)
json.load() / json.dump()             Episodic memory (persistent storage)
ConversationBufferMemory()            LangChain: full history
ConversationSummaryMemory()           LangChain: auto-summarization
ConversationBufferWindowMemory(k=10)  LangChain: sliding window
VectorStoreRetrieverMemory()          LangChain: RAG-based memory
system_prompt with {memory}           Injecting memory into prompt
```

---

## LangChain Memory Shortcuts

LangChain wraps these patterns into drop-in classes:

> **Version note (checked 2026-10-28):** `langchain.memory` does not exist in LangChain 1.x. These classes now import from the separate `langchain-classic` package, e.g. `from langchain_classic.memory import ConversationBufferMemory`. The imports below are the LangChain 0.x form you will see in older code.

```python
from langchain.memory import ConversationBufferMemory        # full history
from langchain.memory import ConversationSummaryMemory       # auto-summarize
from langchain.memory import ConversationBufferWindowMemory  # sliding window
from langchain.memory import VectorStoreRetrieverMemory      # RAG memory

# Usage:
memory = ConversationBufferWindowMemory(k=10)   # last 10 turns
chain  = ConversationChain(llm=llm, memory=memory)

# After 10 turns, turn 1 automatically drops off
# No code changes needed — LangChain handles it
```

---

## The Key Insight

**The context window is the only truth.** All memory systems are just clever ways of deciding *what information to put in the context window* before calling the LLM.

```
Vector DB:    "search 10,000 docs → pick top 3 → put in context"
Sliding Window: "keep only last 10 turns → put in context"
Summarization:  "compress 50 turns → put summary in context"
Episodic:       "load user profile from disk → put in context"
```

Every memory system = a strategy for filling the goldfish bowl with the right water.

---

## Pattern Recognition Summary

| What you see | What it means |
|:-------------|:--------------|
| `self.history.append(...)` | Working memory accumulation |
| `self.history[-10:]` | Sliding window (last 10) |
| `_summarize()` before appending | Compression checkpoint |
| `vector_db.similarity_search()` | Semantic retrieval (RAG) |
| `json.load(filepath)` at `__init__` | Episodic/persistent load |
| `ConversationSummaryMemory` | LangChain auto-summary |
| `memory_key="chat_history"` | LangChain memory injection into prompt |

**Next: L13 — ReAct Reasoning Pattern**
How does the agent decide *when* to search memory vs when to use a tool vs when to just answer?
