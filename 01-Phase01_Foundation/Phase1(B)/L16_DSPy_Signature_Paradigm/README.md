# Lesson 16 Templates: DSPy Signature Paradigm

Describe what you want (input → output). DSPy figures out how to get it.

## Learning Materials
The lesson file covers signatures, modules, programs, and the optimizer with clear comparisons to traditional prompting.

## Templates
1. **PASS1_RECOGNITION.md** - 8 DSPy patterns from real production code
2. **PASS_C_VISUAL.md** - Visual diagrams: signature anatomy, module hierarchy, optimizer loop, DSPy vs traditional
3. **CHEATSHEET_L16.py** - Quick reference for all DSPy signals and patterns
4. **template_dspy_signatures.py** - 4 patterns: basic signature, ChainOfThought, full DSPy module, RAG pipeline (runnable demo)

## The DSPy Mental Model
```
Traditional: You write prompt → fragile, manual, hard to compose
DSPy:        You write signature (input → output) → DSPy writes prompt for you

Signature:  class Summarize(dspy.Signature):
                document: str = dspy.InputField()
                summary:  str = dspy.OutputField()

Module:     summarizer = dspy.Predict(Summarize)   # or ChainOfThought, ReAct
Result:     result.summary                          # structured output, no parsing
```

## The Key Insight
DSPy moves you from **prompt engineer** (write + tune prompts) to **program architect** (declare structure, let DSPy optimize).
