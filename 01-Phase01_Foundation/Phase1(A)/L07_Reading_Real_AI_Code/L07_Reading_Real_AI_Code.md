# Lesson 07: Reading Real AI Code (The Rosetta Stone)
## The Revelation

Architect, you now know the 6 fundamental patterns:
- **L01:** Labels & Types — variables, dictionaries, type hints (`name: str`)
- **L02:** Lists & Collections — lists, list of dicts (the core pattern)
- **L03:** Logic Gates — `if/elif/else` for threshold checks, `match/case` for name routing
- **L04:** Loops & Iteration — `for` loops, `while`, `enumerate`
- **L05:** Functions as Tools — `def fn(param: str) -> dict:`, `return`
- **L06:** Classes as Blueprints — standard class, `@dataclass`, Pydantic `BaseModel`

> **2026 NOTE:** Three class styles exist. Standard `class` = agent with memory. `@dataclass` = config container. Pydantic `BaseModel` = validated LLM output. You'll see all three in real AI code.

**Here's the secret nobody tells you:** Real AI code is just these 6 patterns dressed up with fancy names.

When you see professional LangChain, CrewAI, or DSPy code, **80% of it is list manipulation**. The other 20% is imports and function calls.

This lesson is your **decoder ring** — you'll see real AI code and recognize: "Oh, that's just a dictionary from L01!"

---

## Example 1: LangChain Chatbot (Annotated)

Here's a complete chatbot in 10 lines. Let me show you it's just your L01–L06 patterns:

```python
# ═══════════════════════════════════════════════════════════
# IMPORTS (Just copy-paste, covered in L08)
# ═══════════════════════════════════════════════════════════
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage

# ═══════════════════════════════════════════════════════════
# L01: DICTIONARY — Store configuration (labeled drawer!)
# ═══════════════════════════════════════════════════════════
config = {
    "model": "claude-sonnet-5-5",
    "temperature": 0.7,
    "max_tokens": 1000
}

# ═══════════════════════════════════════════════════════════
# L06: CLASS — Create agent instance (blueprint from L06!)
# ═══════════════════════════════════════════════════════════
model = ChatAnthropic(
    model=config["model"],           # ← Access dict value (L01!)
    temperature=config["temperature"]
)

# ═══════════════════════════════════════════════════════════
# L02: LIST OF DICTS — Conversation history (THE PATTERN!)
# ═══════════════════════════════════════════════════════════
conversation = [
    HumanMessage(content="What is RAG?"),
    # HumanMessage is just a fancy dict: {"role": "user", "content": "..."}
]

# ═══════════════════════════════════════════════════════════
# L05: FUNCTION CALL — Use the tool (invoke = juicer from L05!)
# ═══════════════════════════════════════════════════════════
response = model.invoke(conversation)  # Input → Processing → Output

# ═══════════════════════════════════════════════════════════
# L02: APPEND — Add to conversation list (just like L02!)
# ═══════════════════════════════════════════════════════════
conversation.append(AIMessage(content=response.content))

print(response.content)
```

---

## What You Just Saw

| Fancy Code | What It Really Is | Lesson |
|:-----------|:------------------|:-------|
| `config = {"model": "claude-sonnet-5-5"}` | Dictionary with labels | **L01** |
| `model = ChatAnthropic(...)` | Create instance from blueprint | **L06** |
| `conversation = [HumanMessage(...)]` | List of dicts | **L02** |
| `response = model.invoke(conversation)` | Call method with input | **L05 + L06** |
| `conversation.append(AIMessage(...))` | Add to list | **L02** |

**The shocking truth:** This is a professional LangChain chatbot, and it's ONLY using your L01–L06 patterns!

---

## Example 2: RAG System (Annotated)

Now let's decode a Retrieval-Augmented Generation system:

```python
# ═══════════════════════════════════════════════════════════
# IMPORTS (Copy-paste territory — covered in L08)
# ═══════════════════════════════════════════════════════════
from langchain_anthropic import ChatAnthropic
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# ═══════════════════════════════════════════════════════════
# L02: LIST OF DICTS — Your knowledge base documents
# ═══════════════════════════════════════════════════════════
documents = [
    {"text": "RAG combines retrieval with generation...", "source": "Wikipedia"},
    {"text": "Vector databases store embeddings...", "source": "ArXiv"},
    {"text": "Semantic search finds similar meaning...", "source": "Blog"}
]

# ═══════════════════════════════════════════════════════════
# L06: CLASS — Create vector database (blueprint!)
# ═══════════════════════════════════════════════════════════
vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(),
    collection_name="my_knowledge_base"
)

# ═══════════════════════════════════════════════════════════
# L05: FUNCTION — Search function with TYPE HINTS (L01 + L05!)
# ═══════════════════════════════════════════════════════════
def search_knowledge(query: str) -> list:       # ← type hints from L01/L05
    # This returns a LIST of DICTS (L02!)
    results = vectorstore.similarity_search(query, k=3)
    return results

# ═══════════════════════════════════════════════════════════
# L01: DICTIONARY — User query metadata
# ═══════════════════════════════════════════════════════════
user_query = {
    "question": "What is RAG?",
    "user_id": "user_123",
    "timestamp": "2026-03-06"
}

# ═══════════════════════════════════════════════════════════
# STEP 1: RETRIEVE (Function call from L05!)
# ═══════════════════════════════════════════════════════════
retrieved_docs = search_knowledge(user_query["question"])
# Returns: [{"text": "...", "score": 0.95}, {"text": "...", "score": 0.88}]

# ═══════════════════════════════════════════════════════════
# L05: FUNCTION — Format prompt with TYPE HINTS
# ═══════════════════════════════════════════════════════════
def format_rag_prompt(question: str, docs: list) -> str:
    context = "\n".join([doc["text"] for doc in docs])  # ← L04: Loop through list!
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    return prompt

# ═══════════════════════════════════════════════════════════
# STEP 2: GENERATE (Use LLM with context)
# ═══════════════════════════════════════════════════════════
model = ChatAnthropic(model="claude-sonnet-5-5")
prompt = format_rag_prompt(user_query["question"], retrieved_docs)
answer = model.invoke(prompt)

# ═══════════════════════════════════════════════════════════
# L01: DICTIONARY — Store complete result
# ═══════════════════════════════════════════════════════════
result = {
    "question": user_query["question"],
    "answer": answer.content,
    "sources": [doc["source"] for doc in retrieved_docs],  # ← L04: Extract from list!
    "confidence": 0.94
}

print(result)
```

---

## What You Just Saw

| Fancy Code | What It Really Is | Lesson |
|:-----------|:------------------|:-------|
| `documents = [{"text": "...", "source": "..."}]` | List of dicts | **L02** |
| `vectorstore = Chroma(...)` | Create instance from blueprint | **L06** |
| `def search_knowledge(query: str) -> list:` | Function with type hints | **L01 + L05** |
| `results = vectorstore.similarity_search(...)` | Method returns list of dicts | **L05 + L02** |
| `[doc["text"] for doc in docs]` | Loop through list, extract values | **L04 + L02** |
| `result = {"question": ..., "answer": ...}` | Dictionary to organize output | **L01** |

**Again:** This is a professional RAG system, and it's just your L01–L06 patterns orchestrated together!

---

## Example 3: Function Calling Agent (Annotated)

The "advanced" pattern — an agent that picks tools using `match/case`:

```python
# ═══════════════════════════════════════════════════════════
# L02: LIST OF DICTS — Available tools (THE PATTERN!)
# ═══════════════════════════════════════════════════════════
available_tools = [
    {
        "name": "search_database",
        "description": "Search internal knowledge base",
        "function": search_knowledge  # ← Reference to L05 function!
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "function": do_math
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "function": fetch_weather
    }
]

# ═══════════════════════════════════════════════════════════
# L05: FUNCTION — Agent decision maker with type hints
# ═══════════════════════════════════════════════════════════
def agent_decide(user_input: str, tools: list) -> dict:
    # Ask LLM: "Which tool should I use?"
    # LLM returns a DICTIONARY (L01!)
    decision = {
        "tool_name": "search_database",
        "reasoning": "User asked a knowledge question"
    }
    return decision

# ═══════════════════════════════════════════════════════════
# L05: FUNCTION — Execute the chosen tool
# L03: match/case — routing by TOOL NAME (not a score check!)
# ═══════════════════════════════════════════════════════════
def execute_tool(tool_name: str, user_input: str) -> str:
    match tool_name:                          # ← L03: route by name
        case "search_database":
            return search_knowledge(user_input)
        case "calculate":
            return do_math(user_input)
        case "get_weather":
            return fetch_weather(user_input)
        case _:
            return "Tool not found"

# ═══════════════════════════════════════════════════════════
# FULL AGENT EXECUTION
# ═══════════════════════════════════════════════════════════
user_input = "What is RAG?"

# Step 1: Decide which tool (L05 function)
decision = agent_decide(user_input, available_tools)

# Step 2: Execute that tool (match/case routing from L03)
result = execute_tool(decision["tool_name"], user_input)

# Step 3: Store complete interaction (L01 dictionary)
interaction_log = {
    "user_input": user_input,
    "tool_used": decision["tool_name"],
    "result": result,
    "timestamp": "2026-03-06"
}

print(interaction_log)
```

---

## What You Just Saw

| Fancy Code | What It Really Is | Lesson |
|:-----------|:------------------|:-------|
| `available_tools = [{"name": "...", "function": ...}]` | List of dicts with function refs | **L02 + L05** |
| `def agent_decide(...) -> dict:` | Function with type hints | **L01 + L05** |
| `match tool_name: case "search_database":` | Route by name (not score) | **L03** |
| `tool["function"](user_input)` | Call function stored in dict | **L05** |
| `interaction_log = {...}` | Store result as dictionary | **L01** |

**The revelation:** Even "advanced" function-calling agents are just your L01–L06 patterns!

---

## Example 4: The Three Class Styles in the Wild (L06)

When you open real AI code, you'll see all three styles. Here's how to recognize them:

```python
# ═══════════════════════════════════════════════════════════
# STYLE 1: Standard class — Agent with memory and methods
# ═══════════════════════════════════════════════════════════
class ResearchAgent:                          # ← L06: blueprint
    def __init__(self, model: str):
        self.model = model                    # ← L01: stored attribute
        self.history: list = []              # ← L02: empty list
    def ask(self, question: str) -> str:     # ← L05: method with type hints
        self.history.append(question)
        return call_llm(question)

# ═══════════════════════════════════════════════════════════
# STYLE 2: @dataclass — Config container (no methods needed)
# ═══════════════════════════════════════════════════════════
from dataclasses import dataclass

@dataclass
class PipelineConfig:                        # ← L06: @dataclass style
    model: str = "claude-sonnet-5-5"        # ← L01: type hint + default
    max_tokens: int = 1000
    temperature: float = 0.7

config = PipelineConfig()                    # ← Python writes __init__ for you
# config.model  → "claude-sonnet-5-5"

# ═══════════════════════════════════════════════════════════
# STYLE 3: Pydantic BaseModel — Validates LLM output
# ═══════════════════════════════════════════════════════════
from pydantic import BaseModel

class SearchResult(BaseModel):               # ← L06: Pydantic style
    answer: str                              # ← L01: required field
    confidence: float                        # ← L01: must be a float
    sources: list                            # ← L02: must be a list

result = SearchResult(answer="RAG is...", confidence=0.94, sources=["wiki"])
# Pydantic checks types automatically — if confidence="high", it raises an error
```

**The Rule (from L06):**

| You See | It Means | Lesson |
|:--------|:---------|:-------|
| `class Agent:` with methods | Does things, holds memory | **L06 standard** |
| `@dataclass class Config:` | Holds settings, no methods | **L06 @dataclass** |
| `class Output(BaseModel):` | Validates data from LLM/API | **L06 Pydantic** |

---

## The Pattern Recognition Test

Look at this code and identify the lessons:

```python
# Mystery code from a real AI project
conversation_history = []

system_prompt = {
    "role": "system",
    "content": "You are a helpful AI assistant"
}

conversation_history.append(system_prompt)

user_message = {"role": "user", "content": "Hello!"}
conversation_history.append(user_message)

if len(conversation_history) > 10:
    conversation_history = conversation_history[-10:]
```

**Answers:**
- `conversation_history = []` → **L02** (create empty list)
- `system_prompt = {...}` → **L01** (dictionary)
- `.append(system_prompt)` → **L02** (add to list)
- `if len(conversation_history) > 10:` → **L03** (logic gate — score/threshold check)
- `conversation_history[-10:]` → **L02** (list slicing — keep last 10)

---

## The Decoder Ring

When you see professional AI code, use this decoder:

| You See This | It's Really This | From Lesson |
|:-------------|:----------------|:------------|
| `config = {...}` | Dictionary | **L01** |
| `name: str = "claude"` | Type hint on variable | **L01** |
| `results = [...]` | List | **L02** |
| `[{...}, {...}]` | List of dicts (THE PATTERN) | **L02** |
| `if score > 0.8:` | Logic gate — threshold check | **L03** |
| `match intent: case "search":` | Route by name | **L03** |
| `for item in list:` | Loop | **L04** |
| `[x for x in list]` | List comprehension (compact loop) | **L04** |
| `def process(q: str) -> dict:` | Function with type hints | **L01 + L05** |
| `model.invoke(...)` | Method call (function on class) | **L05 + L06** |
| `class Agent:` | Standard class blueprint | **L06** |
| `@dataclass class Config:` | Config container | **L06** |
| `class Output(BaseModel):` | Validated LLM output | **L06** |
| `.append(item)` | Add to list | **L02** |
| `data["key"]` | Access dict value | **L01** |

---

## Your New Superpower

You can now:
1. **Read** professional AI code
2. **Recognize** the L01–L06 patterns inside
3. **Understand** what it's doing (even if you can't write it)
4. **Direct** an AI to modify it ("Add error handling to the search function")

**Next up:**
- **L08:** Import patterns — how `from langchain import ChatAnthropic` actually works
- **L09:** Error reading — when it breaks, what does the traceback mean?

---

## Practice Exercise

Open any LangChain or CrewAI example online. With a highlighter:
- **Yellow:** Circle all dictionaries `{}`
- **Blue:** Circle all lists `[]`
- **Green:** Circle all function definitions `def`
- **Red:** Circle all class instances `ClassName(...)`

You'll see: It's 90% yellow and blue (dicts and lists). You already know this!

---

**The truth:** You're not learning a new language. You're learning to read the language you already know when it's dressed up with fancy framework names.

Welcome to real AI development, Architect.
