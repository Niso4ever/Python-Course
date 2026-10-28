"""
TEMPLATE: DSPy — Import Blocks
================================
Use: Declarative AI programming with automatic prompt optimization

pip install:
  pip install dspy python-dotenv

DSPy approach: define WHAT you want (Signature), not HOW to prompt.
DSPy optimizes the prompt automatically using your examples.

COPY the block that matches your use case.
"""

# ═══════════════════════════════════════════════════════════
# BLOCK 1: Basic DSPy Setup + Single Signature
# ═══════════════════════════════════════════════════════════
# Use when: single task, no optimization yet

import dspy
from dotenv import load_dotenv

load_dotenv()

# Configure the global LLM (do this once, at the top):
# lm = dspy.LM("anthropic/claude-sonnet-5-5")
# dspy.configure(lm=lm)
#
# Define a task as a Signature:
# class Summarize(dspy.Signature):
#     """Summarize the given text into one sentence."""
#     text:    str = dspy.InputField()
#     summary: str = dspy.OutputField()
#
# Create a runnable module:
# summarizer = dspy.Predict(Summarize)
#
# Use it:
# result = summarizer(text="Retrieval-Augmented Generation combines search with generation...")
# print(result.summary)


# ═══════════════════════════════════════════════════════════
# BLOCK 2: DSPy with Chain of Thought
# ═══════════════════════════════════════════════════════════
# Use when: task needs step-by-step reasoning

import dspy
from dotenv import load_dotenv

load_dotenv()

# lm = dspy.LM("anthropic/claude-sonnet-5-5")
# dspy.configure(lm=lm)
#
# class AnalyzeCode(dspy.Signature):
#     """Analyze Python code and explain what it does."""
#     code:        str = dspy.InputField(desc="Python code to analyze")
#     explanation: str = dspy.OutputField(desc="Plain English explanation")
#
# # ChainOfThought adds intermediate reasoning steps:
# analyzer = dspy.ChainOfThought(AnalyzeCode)
#
# result = analyzer(code="for i in range(5): print(i)")
# print(result.explanation)


# ═══════════════════════════════════════════════════════════
# BLOCK 3: DSPy with Optimizer (BootstrapFewShot)
# ═══════════════════════════════════════════════════════════
# Use when: improving quality with few-shot examples

import dspy
from dspy.teleprompt import BootstrapFewShot
from dspy.evaluate import Evaluate
from dotenv import load_dotenv

load_dotenv()

# lm = dspy.LM("anthropic/claude-sonnet-5-5")
# dspy.configure(lm=lm)
#
# # Define signature:
# class QA(dspy.Signature):
#     """Answer the question accurately."""
#     question: str = dspy.InputField()
#     answer:   str = dspy.OutputField()
#
# # Training examples:
# trainset = [
#     dspy.Example(question="What is RAG?", answer="Retrieval-Augmented Generation").with_inputs("question"),
#     dspy.Example(question="What is an LLM?", answer="Large Language Model").with_inputs("question"),
# ]
#
# # Define a metric (how to judge quality):
# def exact_match(example, pred, trace=None):
#     return example.answer.lower() in pred.answer.lower()
#
# # Optimize:
# optimizer   = BootstrapFewShot(metric=exact_match)
# base_module = dspy.Predict(QA)
# optimized   = optimizer.compile(base_module, trainset=trainset)
#
# # Use optimized version:
# result = optimized(question="What is a vector database?")
# print(result.answer)


# ═══════════════════════════════════════════════════════════
# BLOCK 4: DSPy RAG Module
# ═══════════════════════════════════════════════════════════
# Use when: RAG pipeline built with DSPy modules

import dspy
from dotenv import load_dotenv

load_dotenv()

# lm = dspy.LM("anthropic/claude-sonnet-5-5")
# dspy.configure(lm=lm)
#
# class GenerateAnswer(dspy.Signature):
#     """Answer question given retrieved context."""
#     context:  list[str] = dspy.InputField(desc="Retrieved passages")
#     question: str       = dspy.InputField()
#     answer:   str       = dspy.OutputField(desc="Concise answer")
#
# class RAGModule(dspy.Module):
#     def __init__(self, retriever, num_passages=3):
#         self.retriever = retriever
#         self.num_passages = num_passages
#         self.generate = dspy.ChainOfThought(GenerateAnswer)
#
#     def forward(self, question):
#         # Step 1: Retrieve
#         passages = self.retriever.forward(question, k=self.num_passages)
#         context  = [p.long_text for p in passages]
#         # Step 2: Generate
#         return self.generate(context=context, question=question)
#
# # Usage:
# rag = RAGModule(retriever=my_retriever)
# result = rag(question="What is DSPy?")
# print(result.answer)


# ═══════════════════════════════════════════════════════════
# QUICK REFERENCE: DSPy Components
# ═══════════════════════════════════════════════════════════
"""
COMPONENT              IMPORT                              WHAT IT DOES
───────────────────    ──────────────────────────────────   ──────────────────────────────
Configure LLM          import dspy / dspy.configure(lm=)   Set global LLM once
Signature              dspy.Signature                       Define task: inputs → outputs
InputField             dspy.InputField(desc="...")          Tag an input field
OutputField            dspy.OutputField(desc="...")         Tag an output field
Predict                dspy.Predict(Signature)              Simple task runner
ChainOfThought         dspy.ChainOfThought(Signature)       Add step-by-step reasoning
ReAct                  dspy.ReAct(Signature, tools=[...])   ReAct loop with tools
Example                dspy.Example(field=val)              Training data point
BootstrapFewShot       from dspy.teleprompt import ...      Optimize with examples
MIPROv2                from dspy.teleprompt import ...      Advanced optimizer
Evaluate               from dspy.evaluate import Evaluate   Evaluate module quality
Module                 dspy.Module                          Base class for custom modules
"""


# ═══════════════════════════════════════════════════════════
# DSPy vs LangChain — When to Use Each
# ═══════════════════════════════════════════════════════════
"""
DSPy:
✓ Want to optimize prompts automatically
✓ Have training examples (input/output pairs)
✓ Thinking declaratively: "what" not "how"
✓ Research / experimentation context

LangChain:
✓ Need specific chain structure (retriever | prompt | llm | parser)
✓ Using many third-party integrations (Chroma, Pinecone, etc.)
✓ Building production RAG pipelines
✓ Need streaming, async, callbacks
"""


# ═══════════════════════════════════════════════════════════
# DEMO (prints reference — no installs needed)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("DSPy Import Blocks — Reference")
    print("=" * 60)
    print()
    print("BLOCK 1: Basic setup")
    print("  dspy.configure(lm=dspy.LM('anthropic/claude-sonnet-5-5'))")
    print("  class MyTask(dspy.Signature): ...")
    print("  module = dspy.Predict(MyTask)")
    print()
    print("BLOCK 2: Chain of Thought")
    print("  module = dspy.ChainOfThought(MySignature)")
    print("  Adds reasoning steps before final answer")
    print()
    print("BLOCK 3: Optimizer")
    print("  from dspy.teleprompt import BootstrapFewShot")
    print("  optimizer.compile(module, trainset=examples)")
    print()
    print("BLOCK 4: RAG Module")
    print("  class RAGModule(dspy.Module):")
    print("      def forward(self, question): ...")
