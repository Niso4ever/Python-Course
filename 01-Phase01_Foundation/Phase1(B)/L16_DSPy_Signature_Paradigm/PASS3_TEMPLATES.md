# PASS 3: DSPy Templates — Copy, Paste, Customize

**How to use:** Copy any template. Change the field names and descriptions. Run it.
You never write the prompt — just declare what goes in and what comes out.

See `template_dspy_signatures.py` for runnable versions of every pattern below.

---

## Template Overview

| # | Template | Use when |
|:--|:---------|:---------|
| 1 | Basic Signature + Predict | Simplest LLM task — one input, one output |
| 2 | Multi-Output Signature | Need several typed fields from one call |
| 3 | ChainOfThought | Complex task that benefits from reasoning |
| 4 | Full DSPy Module | Multi-step pipeline (retrieve → generate, etc.) |
| 5 | RAG Pipeline | Answer questions from a knowledge base |
| 6 | Optimizer | Improve quality automatically from examples |

---

## Template 1 — Basic Signature + Predict

The minimum DSPy pattern. No prompt. No parsing. Just declare and call.

```python
import dspy

# 1. Configure LLM once at the top
lm = dspy.LM("anthropic/claude-sonnet-5-5")
dspy.configure(lm=lm)

# 2. Declare the signature (what goes in → what comes out)
class Summarize(dspy.Signature):
    """Summarize a document into the most important points."""
    document: str = dspy.InputField(desc="The document text to summarize")
    summary:  str = dspy.OutputField(desc="Concise summary of key points")

# 3. Create the module
summarizer = dspy.Predict(Summarize)

# 4. Call it
result = summarizer(document="Your text here...")
print(result.summary)   # typed field, no parsing needed
```

**Customize:** Change field names, types, and `desc=` text. The docstring becomes the task description.

---

## Template 2 — Multi-Output Signature

When you need several typed results from one LLM call.

```python
import dspy

class ClassifyAndExplain(dspy.Signature):
    """Classify a customer message and explain the classification."""
    message:     str   = dspy.InputField()
    category:    str   = dspy.OutputField(desc="One of: complaint, question, praise, request")
    confidence:  float = dspy.OutputField(desc="Confidence score from 0.0 to 1.0")
    explanation: str   = dspy.OutputField(desc="Brief reason for this classification")

classifier = dspy.Predict(ClassifyAndExplain)
result = classifier(message="Your product broke after one day!")

print(result.category)    # "complaint"
print(result.confidence)  # 0.95
print(result.explanation) # "User expressing dissatisfaction..."
```

**Customize:** Add or remove OutputField lines. Each one is automatically extracted and typed.

---

## Template 3 — ChainOfThought

Adds a hidden reasoning step before the answer. Better quality for complex decisions.

```python
import dspy

class AnalyzeAndRecommend(dspy.Signature):
    """Analyze a business situation and recommend an action."""
    situation:      str = dspy.InputField(desc="Description of the business situation")
    recommendation: str = dspy.OutputField(desc="Specific recommended action with rationale")
    confidence:     str = dspy.OutputField(desc="High / Medium / Low")

# ChainOfThought instead of Predict
analyst = dspy.ChainOfThought(AnalyzeAndRecommend)

result = analyst(situation="Sales dropped 30% this quarter despite increased marketing spend.")

# ChainOfThought adds .reasoning automatically (the internal thinking)
print(result.reasoning)       # internal thought process
print(result.recommendation)  # final answer
print(result.confidence)      # "Medium"
```

**When to use over Predict:** When quality matters more than speed, or when you want to see the reasoning.

---

## Template 4 — Full DSPy Module (Multi-Step Pipeline)

When your task needs multiple LLM calls in sequence. Follows the L06 class pattern.

```python
import dspy

# Step signatures
class PlanSignature(dspy.Signature):
    """Identify what information is needed to answer the question."""
    question:       str       = dspy.InputField()
    search_queries: list[str] = dspy.OutputField(desc="2-3 specific search queries")

class SynthesizeSignature(dspy.Signature):
    """Synthesize research findings into a comprehensive answer."""
    question:   str       = dspy.InputField()
    findings:   list[str] = dspy.InputField(desc="Research findings from sources")
    answer:     str       = dspy.OutputField(desc="Comprehensive answer citing findings")
    confidence: str       = dspy.OutputField(desc="High / Medium / Low")

# The pipeline module
class ResearchAgent(dspy.Module):
    def __init__(self, search_fn=None):
        super().__init__()
        self.planner    = dspy.ChainOfThought(PlanSignature)
        self.synthesize = dspy.ChainOfThought(SynthesizeSignature)
        self.search_fn  = search_fn or self._mock_search

    def _mock_search(self, query: str) -> str:
        return f"[Results for: {query}]"

    def forward(self, question: str) -> dspy.Prediction:
        plan     = self.planner(question=question)
        findings = [self.search_fn(q) for q in plan.search_queries]
        return self.synthesize(question=question, findings=findings)

# Usage
agent  = ResearchAgent()
result = agent(question="What are the best practices for AI safety in 2026?")
print(result.answer)
print(result.confidence)
```

**Customize:** Add more steps by adding more signatures and calling them in `forward()`.

---

## Template 5 — RAG Pipeline

Retrieve relevant documents, then generate an answer grounded in them.

```python
import dspy

class RAGSignature(dspy.Signature):
    """Answer a question using retrieved context from a knowledge base."""
    context:  list[str] = dspy.InputField(desc="Relevant passages from knowledge base")
    question: str       = dspy.InputField()
    answer:   str       = dspy.OutputField(desc="Answer grounded in the provided context only")
    source:   str       = dspy.OutputField(desc="Which passage(s) support this answer")

class RAGPipeline(dspy.Module):
    def __init__(self, k: int = 3, retriever=None):
        super().__init__()
        self.k         = k
        self.retriever = retriever
        self.generate  = dspy.ChainOfThought(RAGSignature)

    def _mock_retrieve(self, query: str) -> list[str]:
        """Replace with real vector DB retriever in production."""
        return [
            f"Passage 1 about {query}: Key information here.",
            f"Passage 2 about {query}: Supporting details here.",
            f"Passage 3 about {query}: Additional context here.",
        ][:self.k]

    def forward(self, question: str) -> dspy.Prediction:
        # Step 1: Retrieve
        passages = (
            self.retriever(question, k=self.k).passages
            if self.retriever
            else self._mock_retrieve(question)
        )
        # Step 2: Generate (no hand-written prompt)
        return self.generate(context=passages, question=question)

# Usage
rag    = RAGPipeline(k=3)
result = rag(question="What is our refund policy?")
print(result.answer)
print(result.source)
```

**To connect a real retriever:** Pass any function that takes a query and returns passages as `retriever=` — for example a ChromaDB query wrapped in a small function, `dspy.retrievers.Embeddings(corpus=..., embedder=...)`, or `dspy.retrievers.WeaviateRM`. (DSPy 3.x no longer ships `ChromadbRM`; checked 2026-10-28.)

---

## Template 6 — Optimizer (BootstrapFewShot)

Automatically improve your module's quality from labeled examples.

```python
import dspy

# 1. Your signature
class Classify(dspy.Signature):
    """Classify customer message sentiment."""
    message:   str = dspy.InputField()
    sentiment: str = dspy.OutputField(desc="One of: positive, negative, neutral")

# 2. Training examples (replace with your real data)
trainset = [
    dspy.Example(message="Great product!", sentiment="positive").with_inputs("message"),
    dspy.Example(message="This is broken",  sentiment="negative").with_inputs("message"),
    dspy.Example(message="Arrived on time", sentiment="neutral").with_inputs("message"),
    dspy.Example(message="Love it!",        sentiment="positive").with_inputs("message"),
]

# 3. Metric — what does "correct" mean?
def accuracy_metric(example, prediction, trace=None) -> bool:
    return example.sentiment.lower() == prediction.sentiment.lower()

# 4. Compile (optimize)
optimizer = dspy.BootstrapFewShot(metric=accuracy_metric, max_bootstrapped_demos=2)
base      = dspy.Predict(Classify)
optimized = optimizer.compile(student=base, trainset=trainset)

# 5. Use — same interface, better prompts injected automatically
result = optimized(message="This product exceeded my expectations!")
print(result.sentiment)   # "positive"
```

**Customize:** Swap out `Predict` for `ChainOfThought`. Change the metric to match what "good" means for your task.

---

## Quick Swap Reference

```
dspy.Predict(Sig)              → simple, fast
dspy.ChainOfThought(Sig)       → adds reasoning, better quality
dspy.ReAct(Sig, tools=[...])   → full tool-use loop (L13 + DSPy combined)
dspy.Retrieve(k=3)             → RAG retrieval step
```

```
dspy.InputField()              → what goes IN to LLM
dspy.OutputField()             → what comes OUT from LLM
dspy.OutputField(desc="...")   → with guidance for LLM
```

```
dspy.configure(lm=lm)         → set LLM globally (once per program)
dspy.LM("anthropic/...")      → Anthropic model
dspy.LM("openai/...")         → OpenAI model
```
