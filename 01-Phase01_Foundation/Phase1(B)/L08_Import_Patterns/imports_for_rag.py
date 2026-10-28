"""
TEMPLATE: LangChain RAG — Import Blocks
=========================================
Use: Retrieval-Augmented Generation with LangChain + Claude

pip install:
  pip install langchain langchain-anthropic langchain-community
              langchain-text-splitters chromadb sentence-transformers
              python-dotenv

  For PDF loading: pip install pypdf
  For web loading: pip install beautifulsoup4

COPY the block that matches your use case.
"""

# ═══════════════════════════════════════════════════════════
# BLOCK 1: Chroma RAG Stack (Local, Persistent)
# ═══════════════════════════════════════════════════════════
# Use when: storing docs locally, survives restarts

from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Component setup pattern:
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# db         = Chroma(persist_directory="./chroma_db",
#                     embedding_function=embeddings)
# llm        = ChatAnthropic(model="claude-sonnet-5-5")
# splitter   = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# parser     = StrOutputParser()


# ═══════════════════════════════════════════════════════════
# BLOCK 2: FAISS RAG Stack (In-Memory, Fast)
# ═══════════════════════════════════════════════════════════
# Use when: temporary index, speed priority, no persistence needed
# pip install faiss-cpu

from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Component setup:
# embeddings = HuggingFaceEmbeddings()
# db         = FAISS.from_documents(docs, embeddings)  # Built from docs
# llm        = ChatAnthropic(model="claude-sonnet-5-5")


# ═══════════════════════════════════════════════════════════
# BLOCK 3: Document Loading
# ═══════════════════════════════════════════════════════════
# Use when: ingesting documents into your RAG pipeline

from langchain_community.document_loaders import (
    PyPDFLoader,        # Load PDF files
    WebBaseLoader,      # Load web pages
    TextLoader,         # Load .txt files
    DirectoryLoader,    # Load all files in a folder
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# PDF loading pattern:
# loader   = PyPDFLoader("my_document.pdf")
# pages    = loader.load()                         # List of Document objects
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# chunks   = splitter.split_documents(pages)       # List of smaller chunks

# Web loading pattern:
# loader = WebBaseLoader("https://example.com/article")
# docs   = loader.load()

# Directory loading pattern:
# loader = DirectoryLoader("./docs/", glob="**/*.pdf", loader_cls=PyPDFLoader)
# docs   = loader.load()


# ═══════════════════════════════════════════════════════════
# BLOCK 4: Full LCEL Chain (LangChain Expression Language)
# ═══════════════════════════════════════════════════════════
# Use when: building a composable retrieval chain

from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# LCEL chain pattern:
# retriever = db.as_retriever(search_kwargs={"k": 3})
# prompt    = ChatPromptTemplate.from_template(
#     "Context: {context}\nQuestion: {question}"
# )
# llm       = ChatAnthropic(model="claude-sonnet-5-5")
# parser    = StrOutputParser()
#
# chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | parser
# )
# result = chain.invoke("What is RAG?")


# ═══════════════════════════════════════════════════════════
# QUICK REFERENCE: All RAG Components
# ═══════════════════════════════════════════════════════════
"""
COMPONENT          IMPORT                                           WHAT IT DOES
──────────────     ──────────────────────────────────────────       ─────────────────
LLM                from langchain_anthropic import ChatAnthropic    Claude LLM wrapper
Vector Store       from langchain_community.vectorstores import Chroma  Store embeddings
                   from langchain_community.vectorstores import FAISS   In-memory store
Embeddings         from langchain_community.embeddings import HuggingFaceEmbeddings  Convert text→vectors
Text Splitter      from langchain_text_splitters import RecursiveCharacterTextSplitter  Split docs
Prompt             from langchain_core.prompts import ChatPromptTemplate  Format prompts
Output Parser      from langchain_core.output_parsers import StrOutputParser  Parse LLM output
Document Loaders   from langchain_community.document_loaders import PyPDFLoader  Load PDFs
                   from langchain_community.document_loaders import WebBaseLoader  Load web pages
"""


# ═══════════════════════════════════════════════════════════
# DEMO (prints the import blocks — no installs needed)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("LangChain RAG Import Blocks — Reference")
    print("=" * 60)
    print()
    print("BLOCK 1: Chroma (persistent, local)")
    print("  langchain_anthropic → ChatAnthropic")
    print("  langchain_community.vectorstores → Chroma")
    print("  langchain_community.embeddings → HuggingFaceEmbeddings")
    print("  langchain_text_splitters → RecursiveCharacterTextSplitter")
    print()
    print("BLOCK 2: FAISS (in-memory, fast)")
    print("  Same as Block 1 but Chroma → FAISS")
    print("  Built from docs: FAISS.from_documents(docs, embeddings)")
    print()
    print("BLOCK 3: Document Loading")
    print("  PyPDFLoader → load PDF files")
    print("  WebBaseLoader → load web pages")
    print("  DirectoryLoader → load entire folder")
    print()
    print("BLOCK 4: LCEL Chain")
    print("  retriever | prompt | llm | parser")
    print("  chain.invoke('question') → answer")
