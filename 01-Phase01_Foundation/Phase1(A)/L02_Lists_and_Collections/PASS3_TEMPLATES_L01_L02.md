# Pass 3: TEMPLATES — L01 & L02
## Copy, Modify, Build. Make These Patterns Yours.

**Goal:** Take the patterns you recognized in Pass 1 and practice using them. Every template below is a real AI pattern. Your job: copy it, change it, break it on purpose, fix it.

---

# PART A — L01: Variables & Dictionaries

---

## Template 1: LLM Config Variables

**The starter pattern — copy this exactly first:**
```python
model_name: str = "claude-sonnet-5-5"
temperature: float = 0.7
max_tokens: int = 1000
streaming: bool = True
```

### Your Turn — Modify It:
Change this config to set up a **GPT-4 call** that is:
- Non-streaming
- Very creative (high temperature)
- Short responses (low token limit)

```python
# Fill in the blanks:
model_name: str = "___"
temperature: float = ___
max_tokens: int = ___
streaming: bool = ___
```

<details>
<summary>One possible answer</summary>

```python
model_name: str = "gpt-4"
temperature: float = 1.0
max_tokens: int = 200
streaming: bool = False
```
</details>

---

## Template 2: Result Dictionary

**The starter pattern:**
```python
llm_result = {
    "content": "RAG combines retrieval with generation...",
    "confidence": 0.94,
    "model": "claude-sonnet-5-5",
    "success": True
}
```

### Your Turn — Build a New One:
Create a result dictionary for a **failed** LLM call. It should have:
- Empty content (the call failed)
- Zero confidence
- The model that failed
- Success should reflect the failure

```python
# Build it:
llm_result = {
    "content": ___,
    "confidence": ___,
    "model": ___,
    "success": ___
}
```

<details>
<summary>One possible answer</summary>

```python
llm_result = {
    "content": "",
    "confidence": 0.0,
    "model": "gpt-4",
    "success": False
}
```
</details>

---

## Template 3: Nested Config Dictionary

**The starter pattern:**
```python
rag_config = {
    "model": "claude-sonnet-5-5",
    "relevance_threshold": 0.85,
    "max_context_docs": 3,
    "metadata": {
        "project": "enterprise_kb",
        "version": "2.1",
        "deployed": True
    }
}

# Access the project name:
project = rag_config["metadata"]["project"]
```

### Your Turn — Access Values:
Using the dictionary above, write the access line for each:

```python
# 1. Get the model name:
model = rag_config[___]

# 2. Get the version from metadata:
ver = rag_config[___][___]

# 3. Get the relevance threshold:
threshold = rag_config[___]
```

<details>
<summary>Answers</summary>

```python
model = rag_config["model"]
ver = rag_config["metadata"]["version"]
threshold = rag_config["relevance_threshold"]
```
</details>

---

## Template 4: Safe Access with .get()

**The starter pattern:**
```python
result = {
    "answer": "RAG is retrieval-augmented generation.",
    "confidence": 0.94
}

# Direct access — crashes if key missing:
answer = result["answer"]

# Safe access — returns default if key missing:
source = result.get("source", "unknown")
```

### Your Turn — Predict the Output:
```python
config = {
    "model": "claude-sonnet-5-5",
    "temperature": 0.7
}

# What does each line produce?
a = config["model"]              # → ???
b = config.get("max_tokens", 500)  # → ???
c = config.get("temperature", 0.0) # → ???
```

<details>
<summary>Answers</summary>

```
a → "claude-sonnet-5-5"    (key exists, returns value)
b → 500                     (key MISSING, returns the default)
c → 0.7                     (key EXISTS, returns 0.7 — ignores the default)
```
</details>

---

# PART B — L02: Lists & Collections

---

## Template 5: Simple Tool List

**The starter pattern:**
```python
available_tools = ["web_search", "calculator", "read_document"]

first_tool = available_tools[0]     # "web_search"
last_tool = available_tools[-1]     # "read_document"
tool_count = len(available_tools)   # 3
```

### Your Turn — Build and Access:
Create a list of 4 LLM model names, then access:

```python
# Build the list:
models = [___, ___, ___, ___]

# Get the second model:
second = models[___]

# Get the last model:
last = models[___]

# How many models?
count = ___(models)
```

<details>
<summary>One possible answer</summary>

```python
models = ["claude-sonnet-5-5", "gpt-4", "gemini-pro", "llama-3"]

second = models[1]
last = models[-1]
count = len(models)
```
</details>

---

## Template 6: Conversation History (THE Pattern)

**The starter pattern:**
```python
messages = [
    {"role": "user",      "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG stands for Retrieval-Augmented Generation..."}
]
```

### Your Turn — Extend the Conversation:
Add two more messages — the user asks a follow-up, and the assistant replies:

```python
messages = [
    {"role": "user",      "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG stands for Retrieval-Augmented Generation..."},
    {"role": "___",       "content": "___"},
    {"role": "___",       "content": "___"}
]
```

<details>
<summary>One possible answer</summary>

```python
messages = [
    {"role": "user",      "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG stands for Retrieval-Augmented Generation..."},
    {"role": "user",      "content": "How does the retrieval step work?"},
    {"role": "assistant", "content": "It searches a vector database for relevant documents..."}
]
```
</details>

---

## Template 7: Growing a List with .append()

**The starter pattern:**
```python
conversation = []

conversation.append({"role": "user",      "content": "Hello!"})
conversation.append({"role": "assistant", "content": "Hi! How can I help?"})

print(len(conversation))  # → 2
```

### Your Turn — Build a 3-Turn Conversation:
Start with an empty list and use `.append()` to add 3 messages:

```python
chat_history = []

chat_history.append({___})
chat_history.append({___})
chat_history.append({___})

# How many messages now?
print(len(chat_history))  # → ???
```

<details>
<summary>One possible answer</summary>

```python
chat_history = []

chat_history.append({"role": "user",      "content": "Summarize this document."})
chat_history.append({"role": "assistant", "content": "The document discusses..."})
chat_history.append({"role": "user",      "content": "What are the key points?"})

print(len(chat_history))  # → 3
```
</details>

---

## Template 8: RAG Search Results — Access Drill

**The starter pattern:**
```python
retrieved_docs = [
    {"source": "KB",    "score": 0.94, "text": "RAG combines retrieval..."},
    {"source": "ArXiv", "score": 0.89, "text": "Vector databases store..."},
    {"source": "Blog",  "score": 0.76, "text": "Semantic search finds..."}
]
```

### Your Turn — Access These Values:
```python
# 1. Get the entire first document:
first_doc = retrieved_docs[___]

# 2. Get the score of the second document:
second_score = retrieved_docs[___][___]

# 3. Get the text of the last document:
last_text = retrieved_docs[___][___]

# 4. How many documents were retrieved?
doc_count = ___(retrieved_docs)

# 5. Get just the first 2 results:
top_2 = retrieved_docs[___]
```

<details>
<summary>Answers</summary>

```python
first_doc = retrieved_docs[0]
second_score = retrieved_docs[1]["score"]       # → 0.89
last_text = retrieved_docs[-1]["text"]          # → "Semantic search finds..."
doc_count = len(retrieved_docs)                 # → 3
top_2 = retrieved_docs[:2]
```
</details>

---

## Template 9: Full Agent Config — Putting It All Together

This template combines **L01 variables + L01 dicts + L02 lists**. Read it, then answer the questions below.

```python
agent_config = {
    "name": "research_agent",
    "model": "claude-sonnet-5-5",
    "temperature": 0.3,
    "max_tokens": 2000,
    "tools": ["web_search", "read_document", "summarize"],
    "metadata": {
        "version": "1.0",
        "deployed": True
    }
}
```

### Your Turn — Access Everything:
```python
# 1. Get the agent's name:
name = agent_config[___]

# 2. Get the list of tools:
tools = agent_config[___]

# 3. Get the second tool from the list:
second_tool = agent_config[___][___]

# 4. Get the version from metadata:
version = agent_config[___][___]

# 5. How many tools does the agent have?
tool_count = len(agent_config[___])
```

<details>
<summary>Answers</summary>

```python
name = agent_config["name"]                    # → "research_agent"
tools = agent_config["tools"]                  # → ["web_search", "read_document", "summarize"]
second_tool = agent_config["tools"][1]         # → "read_document"
version = agent_config["metadata"]["version"]  # → "1.0"
tool_count = len(agent_config["tools"])        # → 3
```
</details>

---

# FINAL CHALLENGE: Build From Scratch

Create a complete agent configuration from scratch. It must include:
- A string variable for the agent name
- A dictionary with model settings (model, temperature, max_tokens)
- A list of at least 3 tools
- A nested metadata dictionary with project name and a boolean for deployment status
- A list of 2 conversation messages (user + assistant)

No blanks this time — write the whole thing yourself, then check against the pattern in Template 9.

---

## You've Completed Pass 3!

You can now:
✅ **Copy** variable and dict templates and modify them for new configs
✅ **Build** dictionaries from scratch with all 4 types (str, int, float, bool)
✅ **Access** nested values using `dict["key"]["inner_key"]`
✅ **Use** `.get()` for safe access with defaults
✅ **Create** lists and access items by index
✅ **Build** conversation histories using the list-of-dicts pattern
✅ **Grow** lists with `.append()`
✅ **Slice** lists to keep first N or last N items
✅ **Combine** L01 + L02 patterns in a real agent config

**Next:** L03 — Logic Gates (`if / elif / else`)

> **This is the L01 + L02 pattern — Variables, Dictionaries, Lists, and the List-of-Dicts.**
