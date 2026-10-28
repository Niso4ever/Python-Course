# PASS C: Visual DSPy Diagrams

---

## Diagram 1: Signature Anatomy

```
class Summarize(dspy.Signature):
    │              │
    │              └── Inherits from dspy.Signature
    └── Your class name (describes the task)

    """Summarize a document into key points."""
    ↑── Class docstring becomes part of the prompt DSPy generates

    document: str = dspy.InputField()
    │         │     └── Marks this as INPUT
    │         └── Python type hint (str, int, float, list, etc.)
    └── Field name (used in code: result.document)

    summary:  str = dspy.OutputField()
                    └── Marks this as OUTPUT (what LLM produces)
```

---

## Diagram 2: The Three Core Modules

```
SAME SIGNATURE — THREE MODULE TYPES:

class QA(dspy.Signature):
    question: str = dspy.InputField()
    answer:   str = dspy.OutputField()

┌─────────────────────────────────────────────────────────┐
│  dspy.Predict(QA)                                       │
│  ────────────────────────────────────────────────────── │
│  INPUT → LLM → OUTPUT                                  │
│  Simple, fast, no reasoning shown                       │
│  result.answer ✓                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  dspy.ChainOfThought(QA)                                │
│  ────────────────────────────────────────────────────── │
│  INPUT → REASONING → OUTPUT                            │
│  Adds hidden "reasoning" field before each output       │
│  result.reasoning ✓  result.answer ✓                   │
│  Better quality, slightly more tokens                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  dspy.ReAct(QA, tools=[search, calc])                   │
│  ────────────────────────────────────────────────────── │
│  INPUT → Thought → Action → Observe → ... → OUTPUT     │
│  Full ReAct loop (L13 pattern) using DSPy signature     │
│  Best for: questions requiring external information     │
└─────────────────────────────────────────────────────────┘
```

---

## Diagram 3: DSPy Module (Full Program Structure)

```
class MyPipeline(dspy.Module):    ← inherits from dspy.Module
    def __init__(self):
        super().__init__()        ← required
        self.step1 = dspy.Predict(Signature1)     ← sub-modules
        self.step2 = dspy.ChainOfThought(Signature2)

    def forward(self, input_field):               ← the "run" method
        intermediate = self.step1(input=input_field)   ← step 1
        result       = self.step2(input=intermediate.output)  ← step 2
        return result

# Usage:
pipeline = MyPipeline()
result   = pipeline(input_field="your data")
print(result.final_output)

CONNECTS TO L4:
  dspy.Module  ≈  class with __init__ + forward  ≈  L4 class pattern
  self.step1   ≈  self.history                   ≈  L4 instance attribute
  forward()    ≈  chat() / answer()              ≈  L4 method
```

---

## Diagram 4: Traditional Prompting vs DSPy

```
TRADITIONAL PROMPTING:
───────────────────────────────────────────────────────
You write:
  f"""You are an expert summarizer.
  Summarize the following document in 3 bullet points.
  Be concise. Focus on key insights. Use professional tone.

  Document: {document}

  Summary:"""

Problems:
  ✗ You wrote this prompt (time-consuming)
  ✗ Works for Claude Sonnet, may fail on Haiku
  ✗ Hard to add new output fields
  ✗ If quality is bad, you edit prompt manually
  ✗ "3 bullet points" is a guess — may not be optimal

DSPY:
───────────────────────────────────────────────────────
You write:
  class Summarize(dspy.Signature):
      """Summarize a document into key points."""
      document: str = dspy.InputField()
      summary:  str = dspy.OutputField()

Benefits:
  ✓ DSPy writes the prompt (optimizer figures out best wording)
  ✓ Works across models (Claude, GPT-4, Llama, etc.)
  ✓ Add a field → just add a line of code
  ✓ Quality improved → run optimizer, not manual editing
  ✓ Optimal format learned from your actual data
```

---

## Diagram 5: The Optimizer Loop

```
YOU PROVIDE:
  trainset = [Example(input="...", output="...") ...]
  metric   = def is_good(example, prediction) → bool

OPTIMIZER RUNS:
  ┌─────────────────────────────────────────────┐
  │  Try prompt variation 1 on trainset          │
  │  Measure: how many pass metric?  → 60%      │
  ├─────────────────────────────────────────────┤
  │  Try prompt variation 2 on trainset          │
  │  Measure: how many pass metric?  → 75%      │
  ├─────────────────────────────────────────────┤
  │  Try prompt variation 3 on trainset          │
  │  Measure: how many pass metric?  → 82%      │
  ├─────────────────────────────────────────────┤
  │  Keep best: variation 3 (82%)                │
  └─────────────────────────────────────────────┘

YOU GET:
  optimized_module = best prompt + best few-shot examples
  Runs like any other module: result = optimized(input=...)
  But performs ~15-30% better than unoptimized version
```

---

## Diagram 6: DSPy vs LangChain vs Anthropic Direct

```
ANTHROPIC DIRECT:
  client.messages.create(model=..., messages=[...])
  You control everything. Max flexibility. Max work.
  Use when: custom logic, no framework overhead needed.

LANGCHAIN:
  chain = prompt | llm | parser
  Pre-built components, easy chaining.
  Use when: standard RAG, agent, chat patterns.

DSPY:
  class Foo(dspy.Signature): input → output
  Declarative. Optimizable. Composable.
  Use when: quality matters, multi-step pipelines, production.

              ABSTRACTION LEVEL
  Low ────────────────────────────────── High
  Anthropic Direct    LangChain    DSPy
  (most control)                   (most automation)
```

---

## Diagram 7: Reading DSPy Code in 10 Seconds

```
Step 1: Find dspy.configure(lm=...) — what LLM is used?
  lm = dspy.LM("anthropic/claude-sonnet-5-5")

Step 2: Find class X(dspy.Signature) — what's the task?
  class Summarize: document → summary

Step 3: Find the module type — how is it called?
  dspy.Predict      → simple call
  dspy.ChainOfThought → reasoning added
  dspy.ReAct        → tool use loop

Step 4: Find class X(dspy.Module) — is it multi-step?
  self.step1 + self.step2 in forward() → yes, multi-step

Step 5: Find optimizer — is it trained?
  BootstrapFewShot + optimizer.compile() → yes, optimized
```

---

## Diagram 8: Field Type Reference

```
class MySignature(dspy.Signature):
    # INPUT TYPES:
    text:       str          = dspy.InputField()   # string
    count:      int          = dspy.InputField()   # integer
    threshold:  float        = dspy.InputField()   # decimal
    docs:       list[str]    = dspy.InputField()   # list of strings
    metadata:   dict         = dspy.InputField()   # dictionary

    # OUTPUT TYPES:
    answer:     str          = dspy.OutputField()
    score:      float        = dspy.OutputField(desc="0.0 to 1.0")
    categories: list[str]    = dspy.OutputField(desc="List of matching categories")
    approved:   bool         = dspy.OutputField(desc="True if approved, False if not")

# desc= provides guidance to LLM about what the field should contain
# It becomes part of the auto-generated prompt
```
