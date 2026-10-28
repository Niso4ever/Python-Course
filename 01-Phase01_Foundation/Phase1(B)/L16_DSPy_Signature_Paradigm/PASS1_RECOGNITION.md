# PASS 1: DSPy Pattern Recognition

**Rule:** Read each example. Find the signature, the module, and the output field.

---

## Example 1: Basic Signature (Input → Output Declaration)

```python
import dspy

class Summarize(dspy.Signature):        # ← SIGNATURE: declares I/O shape
    """Summarize a document into key points."""   # ← becomes part of prompt
    document: str = dspy.InputField()            # ← what goes IN
    summary:  str = dspy.OutputField()           # ← what comes OUT

# No prompt written. No API call yet. Just a declaration.
```

**Identify:** What is the InputField? OutputField? What is the class docstring?
**Key insight:** The class body replaces the prompt. No `f"Summarize this: {text}"` needed.

---

## Example 2: Module — Making Signatures Run

```python
import dspy

# Set up LLM once globally
lm = dspy.LM("anthropic/claude-sonnet-5-5")
dspy.configure(lm=lm)

# Three module types on same signature:

# Predict — simplest: just calls LLM
summarizer_basic = dspy.Predict(Summarize)

# ChainOfThought — adds reasoning before output
summarizer_cot = dspy.ChainOfThought(Summarize)   # ← adds hidden "reasoning" field

# Usage looks the same for both:
result = summarizer_basic(document="Long article text here...")
print(result.summary)     # ← structured field, no parsing needed
print(result.reasoning)   # ← only present with ChainOfThought
```

**Identify:** What is `dspy.Predict`? What does `dspy.ChainOfThought` add?
**Key insight:** `.summary` is a typed field, not raw text. No `.split()` or regex needed.

---

## Example 3: Multi-Output Signature

```python
class ClassifyAndExplain(dspy.Signature):
    """Classify customer message and explain the classification."""
    message:     str   = dspy.InputField()
    category:    str   = dspy.OutputField(desc="One of: complaint, question, praise, request")
    confidence:  float = dspy.OutputField(desc="Confidence score from 0.0 to 1.0")
    explanation: str   = dspy.OutputField(desc="Brief reason for this classification")

classifier = dspy.ChainOfThought(ClassifyAndExplain)
result = classifier(message="Your product broke after one day!")

print(result.category)    # "complaint"
print(result.confidence)  # 0.95
print(result.explanation) # "User expressing dissatisfaction with product failure"
```

**Identify:** How many InputFields? OutputFields? What type is `confidence`?
**Key insight:** Multiple typed outputs — DSPy handles the structured extraction automatically.

---

## Example 4: DSPy Module Class (Full Program)

```python
class RAGPipeline(dspy.Module):    # ← full program (like L4 class)
    def __init__(self, k: int = 3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)         # ← retrieval step
        self.generate = dspy.ChainOfThought(       # ← generation step
            "context, question -> answer"          # ← inline signature
        )

    def forward(self, question: str) -> dspy.Prediction:   # ← the "call" method
        passages = self.retrieve(question).passages   # Step 1: retrieve
        return self.generate(context=passages, question=question)  # Step 2: generate

# Usage:
rag = RAGPipeline(k=3)
result = rag(question="What is the return policy?")
print(result.answer)
```

**Identify:** What is `dspy.Module`? What does `forward()` do? What is `dspy.Retrieve`?
**Connects to L4:** `class RAGPipeline(dspy.Module)` uses the L4 class pattern.

---

## Example 5: Inline Signature Syntax

```python
# Signature can be a compact string instead of a full class:

# Full class version:
class QA(dspy.Signature):
    question: str = dspy.InputField()
    answer:   str = dspy.OutputField()

# Compact string version (same result):
qa = dspy.Predict("question -> answer")

# Multi-field compact version:
summarizer = dspy.Predict("document, max_words -> summary")
classifier = dspy.ChainOfThought("message, context -> category, confidence")
```

**Identify:** What's between the `->` on the left? On the right?
**When to use compact syntax:** Quick prototyping. Use full class for production (better docs).

---

## Example 6: The Optimizer (BootstrapFewShot)

```python
# Training data — pairs of (input, correct output)
trainset = [
    dspy.Example(
        document="Long article about climate...",
        summary="Three key points about climate change..."
    ).with_inputs("document")   # ← tell DSPy which fields are inputs
    for doc, summ in your_training_data
]

# Metric function — tells DSPy what "good" means
def summary_quality(example, prediction, trace=None) -> bool:
    """Return True if prediction meets quality bar."""
    return (
        len(prediction.summary) > 50 and
        len(prediction.summary) < 300 and
        "key" in prediction.summary.lower()
    )

# Compile (optimize) the module
optimizer  = dspy.BootstrapFewShot(metric=summary_quality)
optimized  = optimizer.compile(
    student=dspy.Predict(Summarize),   # ← module to optimize
    trainset=trainset                  # ← examples to learn from
)

# After compilation, optimized has better prompts automatically
result = optimized(document="Your article here...")
```

**Identify:** What is `trainset`? What does `metric` measure? What does `compile` do?
**Key insight:** You write WHAT you want. DSPy finds prompts that achieve it.

---

## Example 7: `dspy.configure` — Global Setup

```python
import dspy

# Configure LLM (do this once at the top of your program)
lm = dspy.LM("anthropic/claude-sonnet-5-5")
dspy.configure(lm=lm)

# Configure with retriever too (for RAG programs)
from dspy.retrieve.chromadb_rm import ChromadbRM
rm = ChromadbRM(collection_name="my_docs", persist_directory="./db")
dspy.configure(lm=lm, rm=rm)

# Now ALL modules use this LLM and retriever automatically
# No need to pass model to every module
```

**Identify:** What is `dspy.configure`? What is `lm`? What is `rm`?
**Pattern:** Configure globally once → all modules inherit.

---

## Example 8: DSPy vs Traditional Prompting (Side by Side)

```python
# ── TRADITIONAL ─────────────────────────────────────────
def classify_traditional(message: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-5-5",
        messages=[{
            "role": "user",
            "content": f"""Classify this customer message.
Categories: complaint, question, praise, request.
Only reply with the category name.

Message: {message}"""
        }]
    )
    raw = response.content[0].text.strip()
    # Must parse, validate, handle edge cases manually
    if raw not in ["complaint", "question", "praise", "request"]:
        raw = "question"  # fallback hack
    return raw

# ── DSPY ────────────────────────────────────────────────
class Classify(dspy.Signature):
    """Classify a customer support message."""
    message:  str = dspy.InputField()
    category: str = dspy.OutputField(desc="One of: complaint, question, praise, request")

classifier = dspy.Predict(Classify)

def classify_dspy(message: str) -> str:
    result = classifier(message=message)
    return result.category   # ← already typed, already validated
```

**Identify:** What is different between the two approaches?
**Key differences:**
- Traditional: you write/tune the prompt; DSPy: you declare the structure
- Traditional: parse raw text manually; DSPy: typed output fields
- Traditional: breaks if model changes; DSPy: works across models

---

## Pattern Summary Table

| Code signal | Meaning |
|:-----------|:--------|
| `class X(dspy.Signature)` | Input→output declaration |
| `dspy.InputField()` | This variable goes INTO the LLM |
| `dspy.OutputField()` | This variable comes OUT from LLM |
| `dspy.Predict(X)` | Simplest module: just call LLM |
| `dspy.ChainOfThought(X)` | Add reasoning step before output |
| `dspy.ReAct(X, tools=[...])` | ReAct agent (L13 + L14 combined) |
| `class X(dspy.Module)` | Full multi-step DSPy program |
| `def forward(self, ...)` | The execution method |
| `dspy.Retrieve(k=N)` | Built-in RAG retrieval module |
| `"input -> output"` | Compact inline signature |
| `dspy.configure(lm=...)` | Set global LLM (done once) |
| `dspy.Example(...)` | Labeled training example |
| `BootstrapFewShot(metric=...)` | Optimizer: finds best few-shots |
| `optimizer.compile(student, trainset)` | Run optimization |
