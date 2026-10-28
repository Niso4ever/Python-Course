# Lesson 16: DSPy Signature Paradigm

**Estimated time: 45 minutes**

---

## The Recipe Card Theory

Traditional prompting is like calling a restaurant and explaining exactly how to cook your meal:

> "First sauté the onions in butter for 3 minutes. Then add garlic. Then add cream. Season with salt and pepper. Serve with parsley."

DSPy is like ordering from a menu using a **recipe card** that only describes the input and output:

> **Input:** Onions, garlic, cream, seasonings
> **Output:** Creamy pasta sauce

*You tell it what goes in and what comes out. DSPy figures out the cooking instructions (the prompt).*

---

## The Problem DSPy Solves

Hand-written prompts have three problems:

**Problem 1: They're brittle.** Change the model, and your carefully crafted prompt might perform 30% worse.

**Problem 2: They're manual.** You write, test, tweak, repeat — by hand, for hours.

**Problem 3: They don't compose.** Chaining 5 prompts together means debugging 5 prompts independently.

DSPy replaces hand-written prompts with **learnable modules** that optimize themselves.

```
Traditional:
  You write: "Summarize this text in 3 bullet points. Focus on..."
  → fragile, model-specific, hand-tuned

DSPy:
  You declare: document → summary
  → DSPy finds the best prompt for you, for your model, on your data
```

---

## The Signature: Input → Output

A DSPy signature is a Python class that declares what goes in and what comes out:

```python
import dspy

# ── Basic signature ──────────────────────────────────────
class Summarize(dspy.Signature):
    """Summarize a document into key points."""   # ← becomes part of prompt
    document: str = dspy.InputField()             # ← what goes IN
    summary:  str = dspy.OutputField()            # ← what comes OUT

# ── Multi-field signature ────────────────────────────────
class ClassifyIntent(dspy.Signature):
    """Classify the intent of a customer message."""
    message:     str = dspy.InputField()
    category:    str = dspy.OutputField(desc="One of: complaint, question, praise, request")
    confidence:  float = dspy.OutputField(desc="Confidence score 0.0 to 1.0")
    explanation: str = dspy.OutputField(desc="Why this category was chosen")

# ── RAG signature ────────────────────────────────────────
class RAGAnswer(dspy.Signature):
    """Answer a question using retrieved context."""
    context:  list[str] = dspy.InputField(desc="Relevant passages from knowledge base")
    question: str       = dspy.InputField()
    answer:   str       = dspy.OutputField(desc="Grounded answer using context only")
```

**What you don't write:** The actual prompt text. DSPy generates it.

---

## The Module: Making Signatures Do Work

A signature declares the shape. A **module** makes it run:

```python
# Three built-in modules (most common):

# 1. Predict — simplest, just calls the LLM
summarizer = dspy.Predict(Summarize)
result = summarizer(document="Long article text here...")
print(result.summary)   # ← structured output field

# 2. ChainOfThought — adds reasoning step before answer
# (automatically adds a "reasoning" field before each output)
classifier = dspy.ChainOfThought(ClassifyIntent)
result = classifier(message="Your product broke after one day!")
print(result.category)    # "complaint"
print(result.reasoning)   # "The user is expressing dissatisfaction..."

# 3. ReAct — ReAct agent with tool use (L13 + L14 combined!)
agent = dspy.ReAct(
    signature=RAGAnswer,
    tools=[search_knowledge_base, calculator]
)
result = agent(question="What is our refund policy?")
print(result.answer)
```

---

## The Full DSPy Program (Like a Class in L4)

DSPy programs are built like L4 classes — `__init__` for setup, `forward` for execution:

```python
class RAGPipeline(dspy.Module):
    """
    Full RAG pipeline: retrieve → generate.
    This is a DSPy program — not a function, not a chain.
    """
    def __init__(self, k=3):
        super().__init__()
        self.k        = k
        self.retrieve  = dspy.Retrieve(k=k)   # ← retrieval module
        self.generate  = dspy.ChainOfThought(RAGAnswer)   # ← generation module

    def forward(self, question: str) -> dspy.Prediction:
        # Step 1: Retrieve relevant passages
        passages = self.retrieve(question).passages

        # Step 2: Generate answer using passages
        prediction = self.generate(
            context=passages,
            question=question
        )
        return prediction

# Usage — looks like a function call:
rag = RAGPipeline(k=3)
result = rag(question="What is our return policy?")
print(result.answer)
```

---

## The Optimizer: Where the Magic Happens

Here's what makes DSPy revolutionary. Instead of tweaking prompts by hand, you **optimize** the program on examples:

```python
# Step 1: Give DSPy some labeled examples
trainset = [
    dspy.Example(
        document="...",
        summary="..."   # ← the correct answer
    ).with_inputs("document")
    for doc, summ in your_data
]

# Step 2: Define what "good" means (metric function)
def summary_quality(example, prediction, trace=None) -> bool:
    """Returns True if prediction is good."""
    return len(prediction.summary) > 50 and "key" in prediction.summary.lower()

# Step 3: Compile (optimize) the program
optimizer = dspy.BootstrapFewShot(metric=summary_quality)
optimized_summarizer = optimizer.compile(
    student=dspy.Predict(Summarize),   # ← the module to optimize
    trainset=trainset
)

# Step 4: Use the optimized program (automatically uses best prompts)
result = optimized_summarizer(document="Your text here...")
# ↑ The optimized version has better prompts automatically injected
```

**What happened:** DSPy tried many prompt variations on your training data, measured which ones scored highest on `summary_quality`, and kept the best ones. No manual prompt writing.

---

## DSPy vs Traditional: Side by Side

```python
# ── TRADITIONAL (hand-written prompt) ────────────────────
def classify_traditional(message: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-5-5",
        messages=[{
            "role": "user",
            "content": f"""Classify this customer message into one of these categories:
complaint, question, praise, request.

Message: {message}

Respond with ONLY the category name, nothing else."""   # ← hand-written, brittle
        }]
    )
    return response.content[0].text.strip()

# Problems:
# - If model changes, prompt may need rewriting
# - Hard to add explanation field without more prompt work
# - Getting structured output requires extra parsing

# ── DSPY (declarative) ───────────────────────────────────
class Classify(dspy.Signature):
    """Classify a customer support message."""
    message:  str = dspy.InputField()
    category: str = dspy.OutputField(desc="One of: complaint, question, praise, request")

classifier = dspy.ChainOfThought(Classify)
result = classifier(message=message)
print(result.category)    # Already parsed and typed

# Benefits:
# - Works well across models (Claude, GPT-4, local models)
# - Add a field → DSPy adds it to prompt automatically
# - Structured output is automatic
# - Can optimize prompt quality without rewriting
```

---

## Reading DSPy Code in the Wild

```
You see this                              You understand
────────────────────────────────────────  ────────────────────────────────────
class Foo(dspy.Signature):                Input→output declaration (recipe card)
dspy.InputField()                         This variable is INPUT to the LLM
dspy.OutputField()                        This variable is OUTPUT from LLM
dspy.Predict(Signature)                   Simple LLM call using signature
dspy.ChainOfThought(Signature)            LLM reasons before answering
dspy.ReAct(Signature, tools=[...])        ReAct agent using DSPy signature
class Foo(dspy.Module):                   Full DSPy program (like L4 class)
def forward(self, ...):                   The "call" method for DSPy modules
dspy.Retrieve(k=3)                        RAG retrieval built-in
BootstrapFewShot(metric=...)              Optimizer: finds best few-shot examples
optimizer.compile(student, trainset)      Run the optimization process
dspy.configure(lm=..., rm=...)            Set the LLM and retriever globally
```

---

## The DSPy Mental Model

```
Traditional AI Pipeline:
  You → write prompt → LLM → parse output → You → debug → rewrite prompt
  [Manual iteration loop, never converges]

DSPy Pipeline:
  You → define signature → DSPy → finds best prompt → Optimizer → measures quality
  [Automated optimization loop, converges to good prompts]
```

DSPy moves you from **prompt engineer** to **program architect**. You describe what you want. The system figures out how to get it.

---

## DSPy Setup (What You'll See at Top of Files)

```python
import dspy

# Configure the LLM (do this once, globally)
lm = dspy.LM("anthropic/claude-sonnet-5-5")   # or openai/gpt-4o, etc.
dspy.configure(lm=lm)

# Configure retriever (for RAG programs)
rm = dspy.ColBERTv2(url="http://colbert-server/")  # or any retriever
dspy.configure(lm=lm, rm=rm)

# That's it. All modules now use this LLM/retriever automatically.
```

---

## Pattern Recognition Summary

| What you see | What it means |
|:-------------|:--------------|
| `class X(dspy.Signature)` | Input→output declaration |
| `dspy.InputField()` | This field goes INTO the LLM |
| `dspy.OutputField()` | This field comes OUT of the LLM |
| `dspy.Predict(X)` | Simplest module: just predict |
| `dspy.ChainOfThought(X)` | Adds reasoning before answer |
| `class X(dspy.Module)` | Full multi-step DSPy program |
| `def forward(self, ...)` | The execution method |
| `BootstrapFewShot` | Finds best few-shot examples |
| `optimizer.compile(...)` | Run the optimization |
| `dspy.configure(lm=...)` | Set global LLM config |

**Next: L15 — Multi-Agent Patterns**
One LLM is a solo musician. Multi-agent is an orchestra — specialized, coordinated, parallel.
