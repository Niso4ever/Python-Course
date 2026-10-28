# PASS 1: Memory Pattern Recognition

**Rule:** Don't write anything. Just read. Find the memory pattern in each example.

---

## Example 1: Full History (Layer 2 — Working Memory)

```python
class ConversationAgent:
    def __init__(self):
        self.history = []               # ← MEMORY: accumulates every turn

    def chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-5-5",
            messages=self.history       # ← SENT: entire history to LLM
        )
        reply = response.content[0].text
        self.history.append({"role": "assistant", "content": reply})
        return reply
```

**What memory layer?** Layer 2 (Working)
**What pattern?** Full history — all turns kept, all sent every time
**When does it break?** When history grows too large for context window

---

## Example 2: Sliding Window (Layer 2 — Capped)

```python
class SlidingWindowAgent:
    def __init__(self, window_size: int = 10):
        self.all_history = []
        self.window_size = window_size

    def chat(self, user_input: str) -> str:
        self.all_history.append({"role": "user", "content": user_input})

        recent = self.all_history[-self.window_size:]    # ← WINDOW: last N only

        response = client.messages.create(
            model="claude-sonnet-5-5",
            messages=recent             # ← SENT: only recent turns, not all
        )
        reply = response.content[0].text
        self.all_history.append({"role": "assistant", "content": reply})
        return reply
```

**What memory layer?** Layer 2 (Working, capped)
**What pattern?** Sliding window — last 10 turns only
**The tradeoff?** Turn 1 is forgotten after turn 11

---

## Example 3: Summarization (Layer 2 — Compressed)

```python
class SummarizationAgent:
    def __init__(self):
        self.recent  = []    # ← MEMORY: last few turns (high resolution)
        self.summary = ""    # ← MEMORY: compressed old history

    def _compress(self):
        old_text = "\n".join(f"{m['role']}: {m['content']}" for m in self.recent[:-3])
        response = client.messages.create(
            model="claude-haiku-5-5",    # cheap model for compression
            messages=[{"role": "user",
                        "content": f"Summarize this in 2 sentences:\n{old_text}"}]
        )
        self.summary = response.content[0].text   # ← compressed
        self.recent  = self.recent[-3:]           # keep last 3 turns raw

    def chat(self, user_input):
        if len(self.recent) > 10:
            self._compress()    # ← CHECKPOINT: compress when too long
        ...
```

**What memory layer?** Layer 2 (Working, compressed)
**Key method?** `_compress()` — converts old turns into summary text
**The tradeoff?** Some detail lost, but context never overflows

---

## Example 4: Vector Memory (Layer 3 — Semantic)

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# This is semantic memory (RAG pattern)
def answer_from_knowledge_base(question: str) -> str:
    # Step 1: Query Layer 3 semantic memory
    db      = Chroma(persist_directory="./vectordb", embedding_function=OpenAIEmbeddings())
    results = db.similarity_search(question, k=3)   # ← RETRIEVE: top 3 chunks

    # Step 2: Put retrieved knowledge into Layer 1 (context window)
    context = "\n".join(doc.page_content for doc in results)

    response = client.messages.create(
        model="claude-sonnet-5-5",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )
    return response.content[0].text
```

**What memory layer?** Layer 3 (Semantic — vector database)
**How it works?** Search 10,000 docs → find top 3 → inject into context window
**Real-world use?** Company documentation, product catalogs, legal databases

---

## Example 5: Persistent Memory (Layer 4 — Episodic)

```python
import json, os

class PersistentAgent:
    def __init__(self, user_id: str):
        self.path    = f"user_{user_id}.json"
        self.profile = self._load()    # ← LOAD from disk at startup

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)   # ← RECALL: load from disk
        return {"name": None, "history": [], "preferences": {}}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.profile, f)   # ← PERSIST: save to disk

    def remember(self, key: str, value):
        self.profile[key] = value
        self._save()    # ← IMMEDIATELY persist after every change
```

**What memory layer?** Layer 4 (Episodic — persistent across sessions)
**Key signals?** `json.load()` + `json.dump()` + user_id-based filepath
**When is it loaded?** At `__init__` — every new conversation picks up where user left off

---

## Example 6: LangChain Memory Classes

```python
from langchain.memory import ConversationBufferMemory        # full history
from langchain.memory import ConversationSummaryMemory       # auto-summarize
from langchain.memory import ConversationBufferWindowMemory  # sliding window

# Buffer: full history (equivalent to Example 1)
memory1 = ConversationBufferMemory()

# Window: last 5 turns only (equivalent to Example 2)
memory2 = ConversationBufferWindowMemory(k=5)

# Summary: compress automatically (equivalent to Example 3)
memory3 = ConversationSummaryMemory(llm=llm)

# Usage — same for all three:
chain = ConversationChain(llm=llm, memory=memory2)
chain.predict(input="What is quantum computing?")
chain.predict(input="How does it compare to classical computing?")
# ↑ memory2 automatically keeps only last 5 turns
```

**What are these?** LangChain wrappers around the patterns from Examples 1-3
**Key insight?** All three implement the same 4 layers, just with different strategies

---

## Example 7: System Prompt Memory Injection

```python
def build_system_prompt(user_id: str) -> str:
    """Inject user memory into the system prompt."""
    profile = load_user_profile(user_id)   # Layer 4 load

    memory_section = ""
    if profile["name"]:
        memory_section += f"User's name: {profile['name']}\n"
    if profile["preferences"]:
        memory_section += f"Preferences: {profile['preferences']}\n"
    if profile["recent_topics"]:
        memory_section += f"Recent topics: {', '.join(profile['recent_topics'])}\n"

    return f"""You are a helpful assistant.
{memory_section}
Use the above context about the user to personalize your responses."""

# Called once per session — memory injected at start
response = client.messages.create(
    model="claude-sonnet-5-5",
    system=build_system_prompt(user_id="alex_123"),   # ← memory injected here
    messages=messages
)
```

**What memory layer?** Layer 4 → injected into Layer 1 (context)
**Key pattern?** Memory from disk formatted as text and put in system prompt
**Real-world use?** Personalized assistants, customer support with history

---

## Example 8: Hybrid Memory (All 4 Layers)

```python
class ProductionAgent:
    """Real production pattern — all 4 memory layers combined."""
    def __init__(self, user_id: str):
        self.user_id  = user_id
        self.profile  = load_profile(user_id)      # Layer 4: load from DB
        self.history  = []                          # Layer 2: session history
        self.rag      = RAGRetriever()              # Layer 3: knowledge base

    def answer(self, question: str) -> str:
        # Layer 3: Find relevant knowledge
        knowledge = self.rag.search(question, k=2)

        # Layer 4: Get user memory
        user_context = f"User: {self.profile['name']}, Tier: {self.profile['tier']}"

        # Layer 2: Last 5 turns (sliding window)
        recent = self.history[-10:]

        # Layer 1: Build context window = all the above combined
        system = f"You are a helpful assistant.\n{user_context}\nKnowledge:\n{knowledge}"
        response = client.messages.create(
            model="claude-sonnet-5-5",
            system=system,        # ← Layer 4 + 3 injected here
            messages=recent + [{"role": "user", "content": question}]  # ← Layer 2
        )
        reply = response.content[0].text
        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": reply})
        save_profile(self.user_id, self.profile)   # Layer 4: persist changes
        return reply
```

**What memory layers?** ALL FOUR — this is a production-grade agent
**Key pattern?** Each layer fills a specific slot in the context window
**When to use?** Customer-facing AI products that need to remember users

---

## Pattern Summary Table

| Code signal | Memory layer | Pattern name |
|:-----------|:-------------|:-------------|
| `self.history = []` | Layer 2 | Full history |
| `self.history[-N:]` | Layer 2 | Sliding window |
| `self.summary = ""` + `_compress()` | Layer 2 | Summarization |
| `vector_db.similarity_search()` | Layer 3 | Semantic/RAG |
| `json.load(filepath)` in `__init__` | Layer 4 | Episodic/persistent |
| `ConversationBufferMemory` | Layer 2 | LangChain full history |
| `ConversationBufferWindowMemory(k=N)` | Layer 2 | LangChain sliding window |
| `ConversationSummaryMemory(llm=llm)` | Layer 2 | LangChain auto-summarize |
| `system=build_system_prompt(user_id)` | 4→1 injection | Profile → system prompt |
