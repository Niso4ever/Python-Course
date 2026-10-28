"""
═══════════════════════════════════════════════════════════════════
LESSON 14 CHEATSHEET: DSPy Signature Paradigm
═══════════════════════════════════════════════════════════════════
Declare input→output. DSPy writes the prompt. Optimizer tunes it.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. SIGNATURE SKELETON
# ═══════════════════════════════════════════════════════════
"""
class TaskName(dspy.Signature):
    \"\"\"One-sentence description of what this does.\"\"\"   # ← prompt instruction
    input_field:  str   = dspy.InputField(desc="...")       # ← input
    output_field: str   = dspy.OutputField(desc="...")      # ← output
"""

# ═══════════════════════════════════════════════════════════
# 2. THE THREE MODULES
# ═══════════════════════════════════════════════════════════
"""
dspy.Predict(Sig)              → simple LLM call
dspy.ChainOfThought(Sig)       → LLM reasons before answering (adds .reasoning field)
dspy.ReAct(Sig, tools=[...])   → full ReAct loop (combines L13 + L14)

All return dspy.Prediction with typed .field_name attributes.
"""

# ═══════════════════════════════════════════════════════════
# 3. PATTERN RECOGNITION GUIDE
# ═══════════════════════════════════════════════════════════
"""
You see                              You understand
──────────────────────────────────   ──────────────────────────────────────
class X(dspy.Signature)              Input→output declaration (recipe card)
dspy.InputField()                    This goes INTO the LLM
dspy.OutputField()                   This comes OUT from the LLM
dspy.Predict(X)                      Simplest module: just predict
dspy.ChainOfThought(X)               Add reasoning before answer
dspy.ReAct(X, tools=[...])           Tool-use agent (L13 pattern)
class X(dspy.Module)                 Full DSPy program (like L4 class)
def forward(self, ...)               The execution method (like L4 method)
dspy.Retrieve(k=N)                   Built-in RAG retrieval
"input -> output"                    Compact inline signature
dspy.configure(lm=...)               Set global LLM (done once)
result.field_name                    Access typed output field
dspy.Example(field=value)            Labeled training example
BootstrapFewShot(metric=fn)          Optimizer: finds best prompts
optimizer.compile(student, trainset) Run the optimization
"""

# ═══════════════════════════════════════════════════════════
# 4. COMPLETE SETUP (copy-paste start)
# ═══════════════════════════════════════════════════════════
DSPY_SETUP_CODE = """
import dspy

# 1. Configure LLM (once at startup)
lm = dspy.LM("anthropic/claude-sonnet-5-5")
dspy.configure(lm=lm)

# 2. Define signature
class MyTask(dspy.Signature):
    \"\"\"Describe the task here.\"\"\"
    input_text: str = dspy.InputField()
    output_text: str = dspy.OutputField(desc="What the output should be")

# 3. Create module
module = dspy.ChainOfThought(MyTask)

# 4. Use it
result = module(input_text="Your input here")
print(result.output_text)
"""

# ═══════════════════════════════════════════════════════════
# 5. MODULE CLASS SKELETON (multi-step)
# ═══════════════════════════════════════════════════════════
"""
class MyPipeline(dspy.Module):
    def __init__(self):
        super().__init__()                              # required!
        self.step1 = dspy.Predict(SignatureA)
        self.step2 = dspy.ChainOfThought(SignatureB)

    def forward(self, question: str) -> dspy.Prediction:
        intermediate = self.step1(question=question)
        result       = self.step2(context=intermediate.context, question=question)
        return result

# Use:
pipeline = MyPipeline()
result   = pipeline(question="Your question")
print(result.answer)
"""

# ═══════════════════════════════════════════════════════════
# 6. OPTIMIZER SKELETON
# ═══════════════════════════════════════════════════════════
"""
# Prepare training data
trainset = [
    dspy.Example(input_text="...", output_text="...").with_inputs("input_text")
    for input_text, output_text in your_data
]

# Define quality metric
def my_metric(example, prediction, trace=None) -> bool:
    return example.output_text.lower() in prediction.output_text.lower()

# Compile (optimize)
optimizer = dspy.BootstrapFewShot(metric=my_metric, max_bootstrapped_demos=3)
optimized = optimizer.compile(
    student=dspy.Predict(MyTask),
    trainset=trainset
)

# Use optimized module (same API, better prompts)
result = optimized(input_text="Your input")
"""

# ═══════════════════════════════════════════════════════════
# 7. COMMON DSPY MISTAKES
# ═══════════════════════════════════════════════════════════
"""
MISTAKE 1: Forgetting super().__init__()
  class MyModule(dspy.Module):
      def __init__(self):
          # missing: super().__init__()  ← AttributeError
          self.step = dspy.Predict(...)

MISTAKE 2: Accessing non-existent output field
  result = dspy.Predict(QA)(question="...")
  result.reasoning  ← AttributeError! Only ChainOfThought adds reasoning
  FIX: use dspy.ChainOfThought(QA) instead of Predict

MISTAKE 3: No dspy.configure before using modules
  module = dspy.Predict(MyTask)
  module(input="...")   ← Error: no LM configured
  FIX: dspy.configure(lm=dspy.LM("anthropic/claude-sonnet-5-5")) first

MISTAKE 4: Forgetting .with_inputs() in trainset
  dspy.Example(question="...", answer="...")          ← DSPy doesn't know which is input
  FIX: dspy.Example(...).with_inputs("question")     ← specify input fields

MISTAKE 5: Using Predict when CoT needed
  result = dspy.Predict(ComplexReasoning)(problem="...")
  ← Simple Predict may struggle with multi-step logic
  FIX: dspy.ChainOfThought(...) for complex reasoning tasks
"""

print("DSPy cheatsheet loaded!")
print("Key: class Signature(dspy.Signature): input → output")
print("     dspy.Predict | ChainOfThought | ReAct")
print("     BootstrapFewShot optimizes prompts automatically.")
