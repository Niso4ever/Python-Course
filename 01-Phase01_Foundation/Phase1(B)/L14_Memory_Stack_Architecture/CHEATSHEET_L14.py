"""
═══════════════════════════════════════════════════════════════════
LESSON 12 CHEATSHEET: Memory Stack Architecture
═══════════════════════════════════════════════════════════════════
The 4 layers, 3 working memory strategies, and LangChain shortcuts.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. THE FOUR MEMORY LAYERS (What to look for in code)
# ═══════════════════════════════════════════════════════════
"""
Layer 1: Context Window  → messages= parameter in API call
Layer 2: Working Memory  → self.history = [] (current session)
Layer 3: Semantic Memory → vector_db.similarity_search()
Layer 4: Episodic Memory → json.load(filepath) / db.execute()

All memory = strategies for filling Layer 1 (context window).
"""

# ═══════════════════════════════════════════════════════════
# 2. PATTERN RECOGNITION GUIDE
# ═══════════════════════════════════════════════════════════
"""
You see                              You understand
──────────────────────────────────   ──────────────────────────────────────
self.history = []                    Working memory (Layer 2)
messages=self.history                Full history — all turns sent
messages=self.history[-N:]           Sliding window — last N turns
self.summary = "" + _compress()      Summarization checkpoint
vector_db.similarity_search()        RAG / semantic memory (Layer 3)
json.load(filepath) in __init__      Episodic memory load (Layer 4)
json.dump(profile) after update      Episodic memory persist (Layer 4)
ConversationBufferMemory()           LangChain: full history
ConversationBufferWindowMemory(k=N)  LangChain: last N turns
ConversationSummaryMemory(llm=llm)   LangChain: auto-summarize
VectorStoreRetrieverMemory()         LangChain: semantic memory
system=build_system_prompt(user_id)  Profile injected into system prompt
f"Context:\n{docs}\nQuestion: {q}"  RAG injection into user message
"""

# ═══════════════════════════════════════════════════════════
# 3. THREE WORKING MEMORY PATTERNS (Quick Reference)
# ═══════════════════════════════════════════════════════════

# PATTERN A: Full History (simplest)
def full_history_pattern(client, history, user_input, model="claude-sonnet-5-5"):
    history.append({"role": "user", "content": user_input})
    response = client.messages.create(model=model, messages=history, max_tokens=1000)
    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply
    # Use when: short sessions, demos, prototypes

# PATTERN B: Sliding Window
def sliding_window_pattern(client, history, user_input, window=10, model="claude-sonnet-5-5"):
    history.append({"role": "user", "content": user_input})
    recent = history[-window:]   # ← THE KEY LINE
    response = client.messages.create(model=model, messages=recent, max_tokens=1000)
    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply
    # Use when: support bots, task-focused sessions

# PATTERN C: RAG Injection
def rag_injection_pattern(client, vector_db, question, model="claude-sonnet-5-5"):
    docs    = vector_db.similarity_search(question, k=3)     # Layer 3 search
    context = "\n".join(doc.page_content for doc in docs)   # format
    messages = [{"role": "user", "content": f"Context:\n{context}\n\nQ: {question}"}]
    response = client.messages.create(model=model, messages=messages, max_tokens=1000)
    return response.content[0].text
    # Use when: knowledge base Q&A, document search

# ═══════════════════════════════════════════════════════════
# 4. LANGCHAIN MEMORY SHORTCUTS
# ═══════════════════════════════════════════════════════════
"""
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationSummaryMemory

# Full history:
memory = ConversationBufferMemory()

# Last 10 turns:
memory = ConversationBufferWindowMemory(k=10)

# Auto-summarize (uses LLM to compress old turns):
memory = ConversationSummaryMemory(llm=llm)

# Plug into a chain:
chain = ConversationChain(llm=llm, memory=memory)
chain.predict(input="Your question here")
"""

# ═══════════════════════════════════════════════════════════
# 5. PERSISTENT MEMORY SKELETON
# ═══════════════════════════════════════════════════════════
import json, os

class EpisodicMemoryMixin:
    """Copy this into any agent class to add Layer 4 memory."""
    def _load_profile(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return {}   # new user

    def _save_profile(self, path: str, profile: dict):
        with open(path, "w") as f:
            json.dump(profile, f, indent=2)

    def remember(self, key: str, value, path: str, profile: dict):
        profile[key] = value
        self._save_profile(path, profile)   # immediate persistence

# ═══════════════════════════════════════════════════════════
# 6. COMMON MEMORY MISTAKES
# ═══════════════════════════════════════════════════════════
"""
MISTAKE 1: Appending after sliding window
  recent = self.history[-10:]
  recent.append(...)               ← WRONG: appending to a slice copy!
  FIX: self.history.append(...)    ← append to full history BEFORE slicing

MISTAKE 2: Not stringifying before storing
  profile["last_response"] = response   ← might be an API object
  FIX: profile["last_response"] = str(response.content[0].text)

MISTAKE 3: Forgetting to save after update
  self.profile["name"] = "Alex"    ← changed in memory
  # missing: json.dump(self.profile, f)  ← NOT saved to disk!

MISTAKE 4: RAG context too large
  context = "\n".join(doc.page_content for doc in all_docs)  ← 50 docs!
  FIX: k=3 in similarity_search → only top 3 chunks

MISTAKE 5: No sliding window → context overflow
  messages=self.history   ← fine for 10 turns, breaks at 200
  FIX: messages=self.history[-20:] for long-running agents
"""

print("Memory cheatsheet loaded!")
print("Key: All memory = filling the context window with the right information.")
