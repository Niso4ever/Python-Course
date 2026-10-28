# Pass 1: Recognition — Import Patterns
## Read These 8 Examples — Don't Write Them

**Goal:** When you see import lines in real AI code, instantly know what's being pulled in and why.

**Your 3-Second Import Read:**
1. **Package name** → which library / framework?
2. **What's imported** → class, function, or tool?
3. **How it's used** → create instance, call function, or decorate?

---

## Example 1: Direct Anthropic API (Simplest Pattern)

```python
import anthropic
from anthropic import Anthropic

# Setup — happens once
client = Anthropic()    # Uses ANTHROPIC_API_KEY from environment

# Use — happens on every call
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What is RAG?"}]
)
print(response.content[0].text)
```

**What to notice:**
- `import anthropic` → whole library (rarely used directly)
- `from anthropic import Anthropic` → grab just the class
- `Anthropic()` → creates an instance (L4 pattern — class instantiation!)
- `client.messages.create(...)` → calling a method on that instance

---

## Example 2: LangChain with Claude

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# Create the LLM
llm = ChatAnthropic(model="claude-sonnet-5-5")

# Build messages
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Explain RAG in one sentence.")
]

# Call it
response = llm.invoke(messages)
print(response.content)
```

**What to notice:**
- `langchain_anthropic` → LangChain's wrapper package for Anthropic
- `langchain_core.messages` → message objects (HumanMessage, SystemMessage)
- These are classes — you create instances: `HumanMessage(content="...")`
- `llm.invoke(messages)` → LangChain's standard call pattern

---

## Example 3: LangChain RAG Stack

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Each import = one component of the RAG pipeline
embeddings = HuggingFaceEmbeddings()
db         = Chroma(persist_directory="./db", embedding_function=embeddings)
splitter   = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
prompt     = ChatPromptTemplate.from_template("Context: {context}\nQ: {question}")
parser     = StrOutputParser()
```

**What to notice:**
- `langchain_community` → third-party integrations (vector stores, embeddings)
- `langchain_text_splitters` → separate package just for document splitting
- `langchain_core` → core abstractions (prompts, parsers, messages)
- Every import is a class — every usage creates an instance

---

## Example 4: LangChain Agent (Tool Use)

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate

# Define a tool with the @tool decorator
@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

# Build the agent
llm    = ChatAnthropic(model="claude-sonnet-5-5")
tools  = [web_search]
agent  = create_react_agent(llm, tools, prompt)
runner = AgentExecutor(agent=agent, tools=tools)

result = runner.invoke({"input": "What is RAG?"})
```

**What to notice:**
- `AgentExecutor` → a class (L4 pattern — you recognize this now!)
- `create_react_agent` → a function (L3 pattern — takes args, returns agent)
- `@tool` → a decorator (wraps the function to register it as an LLM tool)
- `from langchain_core.tools import tool` → `tool` here is the decorator itself

---

## Example 5: Environment Variables (The Key Safety Pattern)

```python
import os
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()

# Read the keys
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
openai_key    = os.getenv("OPENAI_API_KEY", "not-set")   # with default

# Now use them
import anthropic
client = anthropic.Anthropic(api_key=anthropic_key)
```

**What to notice:**
- `os` → built-in Python module (no pip install needed)
- `dotenv` → third-party (`pip install python-dotenv`)
- `load_dotenv()` → reads the `.env` file, sets environment variables
- `os.getenv("KEY")` → reads a single variable (returns `None` if missing)
- `os.getenv("KEY", "default")` → returns `"default"` if key not found

---

## Example 6: DSPy Framework

```python
import dspy
from dspy import Signature, InputField, OutputField
from dspy.teleprompt import BootstrapFewShot

# Configure the global LLM
lm = dspy.LM("anthropic/claude-sonnet-5-5")
dspy.configure(lm=lm)

# Define a task signature
class SentimentAnalysis(Signature):
    """Analyze the sentiment of text."""
    text: str    = InputField()
    sentiment: str = OutputField()

# Create and use a module
classifier = dspy.Predict(SentimentAnalysis)
result     = classifier(text="This movie was amazing!")
print(result.sentiment)
```

**What to notice:**
- `import dspy` → the whole framework
- `from dspy import Signature, InputField, OutputField` → specific pieces
- `dspy.configure(lm=lm)` → global setup (sets LLM for all DSPy calls)
- `class SentimentAnalysis(Signature):` → a class that INHERITS from Signature (new pattern — lesson 4.5 territory)
- `dspy.Predict(SentimentAnalysis)` → creates a runnable module from the signature

---

## Example 7: CrewAI Multi-Agent

```python
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

# Tools
search_tool = SerperDevTool()

# Create agents (classes — L4!)
researcher = Agent(
    role="Researcher",
    goal="Find accurate information",
    tools=[search_tool],
    llm="claude-sonnet-5-5"
)

writer = Agent(
    role="Writer",
    goal="Write clear summaries",
    llm="claude-sonnet-5-5"
)

# Create tasks
task = Task(
    description="Research and summarize RAG techniques",
    agent=researcher
)

# Assemble crew and run
crew   = Crew(agents=[researcher, writer], tasks=[task])
result = crew.kickoff()
```

**What to notice:**
- `from crewai import Agent, Task, Crew` → three classes, one import line
- `Agent(role=..., goal=..., tools=...)` → class instantiation with named args (L3 + L4)
- `Crew(agents=[...], tasks=[...])` → a class that holds OTHER instances as lists (L1.5 inside L4)
- `crew.kickoff()` → runs the multi-agent workflow

---

## Example 8: Mixed Real-World File (What You'll Actually See)

```python
# This is what a real RAG chatbot file looks like at the top

import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

import anthropic
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment
load_dotenv()

# --- Everything below is L1–L5 patterns you already know ---

class RAGChatbot:
    def __init__(self, db_path="./chroma_db"):
        self.llm      = ChatAnthropic(model="claude-sonnet-5-5")
        self.db       = Chroma(persist_directory=db_path,
                               embedding_function=HuggingFaceEmbeddings())
        self.parser   = StrOutputParser()
        self.history  = []

    def chat(self, question: str) -> str:
        docs    = self.db.similarity_search(question, k=3)
        context = "\n".join([d.page_content for d in docs])
        prompt  = f"Context: {context}\nQ: {question}"
        return self.llm.invoke(prompt).content
```

**What to notice:**
- First block: `os`, `json`, `typing` → built-in Python (no pip needed)
- Second block: `anthropic`, `langchain_*` → third-party (pip install)
- Below imports: pure L1–L4 patterns you already know
- **The imports just give you the classes.** Everything after is familiar.

---

## Pattern Summary

| What you see | What it means |
|:-------------|:--------------|
| `import X` | Whole library, use as `X.thing` |
| `from X import Y` | One class/function, use as `Y` directly |
| `import X as Y` | Library with short alias `Y` |
| `from X import Y, Z` | Multiple pieces in one line |
| `from X.sub import Y` | From a sub-package (section of the library) |
| `@tool` | Decorator — registers function as a tool |
| `load_dotenv()` | Reads `.env` file into environment |
| `os.getenv("KEY")` | Reads an API key from environment |

---

**Next:** See [PASS_C_VISUAL.md](PASS_C_VISUAL.md) for diagrams showing where imports come from and how they flow into your code.
