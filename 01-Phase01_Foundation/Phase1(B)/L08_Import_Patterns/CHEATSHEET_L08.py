"""
═══════════════════════════════════════════════════════════════════
LESSON 6 CHEATSHEET: Import Patterns
═══════════════════════════════════════════════════════════════════

Quick reference for import patterns in AI projects.
Keep this open while reading code!

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. THREE IMPORT FORMS
# ═══════════════════════════════════════════════════════════

# Form 1: Whole library — use with prefix
import os
import json
# Usage: os.getenv("KEY"), json.loads(text)

# Form 2: One specific thing — use directly (no prefix)
from dotenv import load_dotenv
from anthropic import Anthropic
# Usage: load_dotenv(), Anthropic()

# Form 3: Alias — short nickname
import anthropic as ant
# Usage: ant.Anthropic(), ant.APIError

# Form 4: Multiple from one line
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# Usage: HumanMessage(content="...")


# ═══════════════════════════════════════════════════════════
# 2. BUILT-IN MODULES (no pip install needed)
# ═══════════════════════════════════════════════════════════

import os           # Environment variables, file paths
import json         # Parse and write JSON
import re           # Regular expressions
import sys          # System info (version, path)
import time         # Timing, sleep
import pathlib      # File path operations
import logging      # Logging output
from typing import List, Dict, Optional, Tuple, Any  # Type hints


# ═══════════════════════════════════════════════════════════
# 3. PIP NAME → IMPORT NAME MAPPING
# ═══════════════════════════════════════════════════════════

"""
pip install name              import name
─────────────────────────     ─────────────────────────────
anthropic                 →   import anthropic
langchain                 →   import langchain
langchain-anthropic       →   from langchain_anthropic import ...
langchain-community       →   from langchain_community import ...
langchain-core            →   from langchain_core import ...
langchain-text-splitters  →   from langchain_text_splitters import ...
python-dotenv             →   from dotenv import load_dotenv
chromadb                  →   import chromadb
dspy                      →   import dspy        (was dspy-ai)
crewai                    →   from crewai import ...
sentence-transformers     →   from sentence_transformers import ...
faiss-cpu                 →   import faiss

RULE: pip uses hyphens (-), Python uses underscores (_)
"""


# ═══════════════════════════════════════════════════════════
# 4. ENVIRONMENT VARIABLES (.env pattern)
# ═══════════════════════════════════════════════════════════

from dotenv import load_dotenv
import os

load_dotenv()   # Reads .env file from current directory

# Read a key (returns None if missing):
api_key = os.getenv("ANTHROPIC_API_KEY")

# Read with default value:
model = os.getenv("MODEL_NAME", "claude-sonnet-5-5")

# Check if key exists:
if not os.getenv("ANTHROPIC_API_KEY"):
    print("Warning: ANTHROPIC_API_KEY not set")


# ═══════════════════════════════════════════════════════════
# 5. ANTHROPIC DIRECT — IMPORT BLOCK
# ═══════════════════════════════════════════════════════════

# pip install anthropic python-dotenv
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic()   # Auto-reads ANTHROPIC_API_KEY


# ═══════════════════════════════════════════════════════════
# 6. LANGCHAIN RAG — IMPORT BLOCK
# ═══════════════════════════════════════════════════════════

# pip install langchain langchain-anthropic langchain-community
#             langchain-text-splitters chromadb sentence-transformers
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader


# ═══════════════════════════════════════════════════════════
# 7. LANGCHAIN AGENTS — IMPORT BLOCK
# ═══════════════════════════════════════════════════════════

# pip install langchain langchain-anthropic
from langchain.agents import create_agent               # LangChain 1.x agent builder
# Older (0.x) code wrote: from langchain.agents import AgentExecutor, create_react_agent
# In LangChain 1.x those live in: from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate


# ═══════════════════════════════════════════════════════════
# 8. CREWAI — IMPORT BLOCK
# ═══════════════════════════════════════════════════════════

# pip install crewai crewai-tools
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool


# ═══════════════════════════════════════════════════════════
# 9. DSPY — IMPORT BLOCK
# ═══════════════════════════════════════════════════════════

# pip install dspy        (old name dspy-ai is now only an alias)
import dspy
from dspy import Signature, InputField, OutputField
from dspy.teleprompt import BootstrapFewShot
from dspy.evaluate import Evaluate


# ═══════════════════════════════════════════════════════════
# 10. IMPORTERROR — HOW TO FIX
# ═══════════════════════════════════════════════════════════

"""
ERROR: ModuleNotFoundError: No module named 'X'
FIX:   pip install X  (check pip name from mapping above)

ERROR: ImportError: cannot import name 'Y' from 'X'
FIX:   Wrong package. Google "Y import python" to find correct package.

ERROR: ModuleNotFoundError: No module named 'dotenv'
FIX:   pip install python-dotenv  (not 'dotenv'!)

STEPS WHEN ANY IMPORT FAILS:
1. Read the error — what module/name is missing?
2. Check mapping table above for pip install name
3. Run: pip install <name>
4. If still failing: Google the exact import line
"""


# ═══════════════════════════════════════════════════════════
# 11. WHAT TYPE OF THING IS IMPORTED?
# ═══════════════════════════════════════════════════════════

"""
CLASS → create an instance to use it
  from langchain_anthropic import ChatAnthropic
  llm = ChatAnthropic(model="claude-sonnet-5-5")

FUNCTION → call it directly
  from langchain.agents import create_react_agent   # 0.x path; 1.x: langchain_classic.agents
  agent = create_react_agent(llm, tools, prompt)

DECORATOR → use with @ above a function
  from langchain_core.tools import tool
  @tool
  def my_tool(query: str) -> str: ...

MODULE-LEVEL CALL → configure globally
  import dspy
  dspy.configure(lm=dspy.LM("anthropic/claude-sonnet-5-5"))
"""


# ═══════════════════════════════════════════════════════════
# 12. 3-SECOND IMPORT BLOCK READ
# ═══════════════════════════════════════════════════════════

"""
When you see a block of imports:
1. SCAN for framework name → anthropic? langchain? dspy? crewai?
2. CHECK what's imported  → LLM class? vector store? tools?
3. VERDICT in one sentence → "This is a LangChain RAG project using Claude and Chroma"

That's all you need. Done.
"""


# ═══════════════════════════════════════════════════════════
# END OF CHEATSHEET
# ═══════════════════════════════════════════════════════════

print("Keep this cheatsheet open while reading AI project code!")
print("Identify framework → copy import block → pip install → done.")
