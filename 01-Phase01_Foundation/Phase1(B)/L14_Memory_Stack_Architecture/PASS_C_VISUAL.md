# PASS C: Visual Memory Stack

---

## Diagram 1: The Four Memory Layers

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 4: EPISODIC (Persistent — survives restarts)             │
│  What: Past sessions, user profiles, long-term facts            │
│  Where: Database, JSON files, Redis                             │
│  Code: json.load() / json.dump() / db.save()                   │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 3: SEMANTIC (Knowledge — searchable facts)               │
│  What: Documents, wikis, product catalogs, FAQs                 │
│  Where: Chroma, FAISS, Pinecone vector databases                │
│  Code: vector_db.similarity_search(query, k=3)                 │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2: WORKING (Session — this conversation)                 │
│  What: Current chat history, session variables                  │
│  Where: Python list in memory (lost on restart)                 │
│  Code: self.history = [] → messages.append(...)                │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 1: CONTEXT WINDOW (Right now — what LLM sees)           │
│  What: The messages list sent to the API                        │
│  Where: The messages= parameter in client.messages.create()     │
│  Code: messages=[{"role":"user","content":"..."}]               │
└─────────────────────────────────────────────────────────────────┘

         ↑ Layers 2, 3, 4 all feed INTO Layer 1
         ↑ Only Layer 1 actually reaches the LLM
```

---

## Diagram 2: The Three Working Memory Strategies

```
STRATEGY A: Full History
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Turn 1: [msg1]              → sent: [msg1]
  Turn 2: [msg1, msg2]        → sent: [msg1, msg2]
  Turn 3: [msg1, msg2, msg3]  → sent: [msg1, msg2, msg3]
  Turn N: [msg1...msgN]       → sent: [msg1...msgN]  ← context fills!

  Code: messages=self.history

STRATEGY B: Sliding Window (k=3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Turn 1: [msg1]              → sent: [msg1]
  Turn 2: [msg1, msg2]        → sent: [msg1, msg2]
  Turn 3: [msg1, msg2, msg3]  → sent: [msg1, msg2, msg3]
  Turn 4: [msg1, msg2, msg3, msg4] → sent: [msg2, msg3, msg4]  ← msg1 dropped!
  Turn 5: ...                 → sent: [msg3, msg4, msg5]  ← window slides

  Code: messages=self.history[-3:]

STRATEGY C: Summarization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Turn 1-8:  accumulate normally
  Turn 9:    checkpoint → compress turns 1-6 → "summary paragraph"
             keep turns 7-8 raw
  Turn 10+:  sent = [summary, turn7, turn8, turn9, turn10]
  Turn 17:   checkpoint again → compress 7-14 → new summary

  Code: self.summary += compress(old_turns); self.history = recent[-3:]
```

---

## Diagram 3: RAG — How Layer 3 Feeds Layer 1

```
                    USER QUESTION
                         │
                         ▼
              ┌──────────────────┐
              │  EMBED QUESTION  │
              │  (convert to     │
              │   numbers)       │
              └────────┬─────────┘
                       │ embedding vector
                       ▼
              ┌──────────────────┐        ┌─────────────────────────┐
              │  SEARCH VECTOR   │        │  VECTOR DATABASE         │
              │  DATABASE        │◄───────│  (10,000 doc chunks)    │
              │  similarity_     │        │  each stored as numbers │
              │  search(q, k=3)  │        │  (embeddings)           │
              └────────┬─────────┘        └─────────────────────────┘
                       │ top 3 chunks
                       ▼
              ┌──────────────────┐
              │  INJECT INTO     │
              │  CONTEXT WINDOW  │
              │  "Context: ...   │
              │  Question: ..."  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │     LLM          │
              │  (only sees the  │
              │   3 chunks, not  │
              │   all 10,000)    │
              └────────┬─────────┘
                       │
                       ▼
                  FINAL ANSWER
```

---

## Diagram 4: LangChain Memory Class Family

```
langchain.memory
│
├── ConversationBufferMemory
│   └── Full history — grows without limit
│       Use: Short conversations, demos
│
├── ConversationBufferWindowMemory(k=N)
│   └── Last N turns only — fixed size
│       Use: Support bots, task-focused chats
│
├── ConversationSummaryMemory(llm=llm)
│   └── Auto-summarizes old turns — adaptive
│       Use: Long conversations where gist matters
│
├── ConversationSummaryBufferMemory(max_token_limit=N)
│   └── Summary + recent raw — best of both
│       Use: Production agents with cost awareness
│
└── VectorStoreRetrieverMemory(retriever=...)
    └── Stores turns in vector DB, retrieves relevant
        Use: Very long sessions, semantic recall needed
```

---

## Diagram 5: Persistent Memory Lifecycle

```
SESSION 1                        SESSION 2
─────────────────────────────    ─────────────────────────────
User: "I'm Alex"                 [new session]
  ↓                              PersistentAgent.__init__()
  agent.remember("name","Alex")     ↓
  → json.dump(profile)           json.load(filepath)
  → profile saved to disk           ↓
                                 profile = {"name": "Alex", ...}
                                    ↓
                                 User: "What's my name?"
                                    ↓
                                 Agent: "Your name is Alex!"
                                    ↑
                              (read from disk, not from LLM memory)
```

---

## Diagram 6: Memory = Filling the Bowl

```
Context Window = a bowl with limited capacity

FULL HISTORY STRATEGY:
┌────────────────────────────────┐
│msg1│msg2│msg3│msg4│msg5│msg6│  │ ← getting full
└────────────────────────────────┘

SLIDING WINDOW STRATEGY:
┌────────────────────────────────┐
│          │msg4│msg5│msg6│msg7│ │ ← always room
└────────────────────────────────┘

SUMMARIZATION STRATEGY:
┌────────────────────────────────┐
│[SUMMARY OF 1-4]│msg5│msg6│msg7│ ← compressed past, fresh recent
└────────────────────────────────┘

RAG STRATEGY:
┌────────────────────────────────┐
│[3 RELEVANT CHUNKS]│QUESTION    │ ← precision-fetched knowledge
└────────────────────────────────┘

HYBRID STRATEGY:
┌────────────────────────────────┐
│[PROFILE]│[2 CHUNKS]│last 5 msgs│ ← all layers combined
└────────────────────────────────┘

LESSON: Every memory pattern = a different way to fill the same bowl.
```

---

## Diagram 7: Reading Memory Code in 10 Seconds

```
Step 1: Find __init__ — what's stored at startup?
  self.history = []           → Layer 2 (working memory)
  json.load(filepath)         → Layer 4 (persistent memory)
  vector_db = Chroma(...)     → Layer 3 (semantic memory)

Step 2: Find the memory limit — how is it controlled?
  messages=self.history        → no limit (full history)
  messages=self.history[-N:]   → sliding window of N turns
  _summarize() when len > X   → summarization checkpoint

Step 3: Find what's sent to LLM — what ends up in context?
  messages=recent              → recent turns only
  system=build_system_prompt() → profile injected into system
  f"Context:\n{docs}\n..."    → RAG chunks injected into user message
```

---

## Diagram 8: Memory Choice Decision Tree

```
Is this a short demo / prototype?
  YES → Full History (ConversationBufferMemory)
  NO  →
    Does context grow over time?
      NO  → Full History still fine
      YES →
        Do users come back across sessions?
          YES → Add Layer 4 (persistent JSON / DB)
          NO  →
            Are turns long / does context overflow?
              YES → Summarization or Sliding Window
              NO  → Full History with 200K limit is OK

        Does the agent need to search knowledge?
          YES → Add Layer 3 (RAG / vector DB)
          NO  → Working memory alone is fine
```
