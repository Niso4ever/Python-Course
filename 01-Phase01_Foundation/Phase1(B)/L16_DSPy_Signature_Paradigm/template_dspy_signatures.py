"""
TEMPLATE: DSPy Signature Patterns
=====================================
4 patterns: basic signature, ChainOfThought, full module, RAG pipeline.

pip install: pip install dspy python-dotenv

Simulated demos run without API key.
Real API calls need: ANTHROPIC_API_KEY in .env (DSPy uses it automatically)
"""
from dotenv import load_dotenv

load_dotenv()


# ═══════════════════════════════════════════════════════════
# SETUP (run before any pattern)
# ═══════════════════════════════════════════════════════════
def setup_dspy(model: str = "anthropic/claude-sonnet-5-5"):
    """Configure DSPy with Anthropic LLM. Call once at startup."""
    import dspy
    lm = dspy.LM(model)
    dspy.configure(lm=lm)
    return dspy

# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Basic Signature + Predict
# ═══════════════════════════════════════════════════════════
def template_basic_signature():
    """
    Simplest DSPy pattern: declare input→output, use Predict.
    No hand-written prompt needed.
    """
    import dspy

    # Define signature (what goes in → what comes out)
    class Summarize(dspy.Signature):
        """Summarize a document into the most important points."""
        document: str = dspy.InputField(desc="The document text to summarize")
        summary:  str = dspy.OutputField(desc="Concise summary of key points")

    # Create module (no prompt written!)
    summarizer = dspy.Predict(Summarize)

    # Use it — result has typed fields
    result = summarizer(document="Your document text here...")
    return result.summary   # ← typed field, no parsing needed


try:
    import dspy

    class ClassifyIntent(dspy.Signature):
        """Classify the intent of a customer support message."""
        message:     str   = dspy.InputField()
        category:    str   = dspy.OutputField(desc="One of: complaint, question, praise, request")
        confidence:  float = dspy.OutputField(desc="Confidence score 0.0 to 1.0")

    class QASignature(dspy.Signature):
        """Answer a question based on provided context."""
        context:  str = dspy.InputField(desc="Background information to use")
        question: str = dspy.InputField()
        answer:   str = dspy.OutputField(desc="Accurate answer based on context only")

except ImportError:
    pass


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: ChainOfThought (Reasoning Before Answering)
# ═══════════════════════════════════════════════════════════
def template_chain_of_thought():
    """
    ChainOfThought adds an internal reasoning step before each output.
    Better quality for complex tasks. Adds .reasoning field to result.
    """
    import dspy

    class AnalyzeAndRecommend(dspy.Signature):
        """Analyze a business situation and recommend an action."""
        situation:      str = dspy.InputField(desc="Description of the business situation")
        recommendation: str = dspy.OutputField(desc="Specific recommended action with rationale")
        confidence:     str = dspy.OutputField(desc="High/Medium/Low confidence in recommendation")

    # ChainOfThought: LLM reasons before answering
    analyst = dspy.ChainOfThought(AnalyzeAndRecommend)

    result = analyst(situation="Sales dropped 30% this quarter despite increased marketing spend.")

    # ChainOfThought adds .reasoning (the internal thinking)
    # print(result.reasoning)      # ← the internal thought process
    print(f"Recommendation: {result.recommendation}")
    print(f"Confidence: {result.confidence}")
    return result


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: Full DSPy Module (Multi-Step Pipeline)
# ═══════════════════════════════════════════════════════════
try:
    import dspy

    class ResearchSignature(dspy.Signature):
        """Identify what information is needed to answer a question."""
        question:        str       = dspy.InputField()
        search_queries:  list[str] = dspy.OutputField(desc="List of 2-3 specific search queries needed")

    class SynthesizeSignature(dspy.Signature):
        """Synthesize research findings into a comprehensive answer."""
        question:  str       = dspy.InputField()
        findings:  list[str] = dspy.InputField(desc="Research findings from multiple sources")
        answer:    str       = dspy.OutputField(desc="Comprehensive answer citing the findings")
        confidence: str      = dspy.OutputField(desc="High/Medium/Low confidence level")

    class ResearchAgent(dspy.Module):
        """
        Multi-step research pipeline:
        1. Identify what to search for
        2. Execute searches (simulated)
        3. Synthesize findings into answer

        Combines L4 (class pattern) + L14 (DSPy signatures).
        """
        def __init__(self, search_fn=None):
            super().__init__()   # ← required for dspy.Module
            self.planner    = dspy.ChainOfThought(ResearchSignature)
            self.synthesize = dspy.ChainOfThought(SynthesizeSignature)
            self.search_fn  = search_fn or self._mock_search

        def _mock_search(self, query: str) -> str:
            return f"[Research results for: {query}]"

        def forward(self, question: str) -> dspy.Prediction:
            """Execute the research pipeline."""
            # Step 1: Plan what to search
            plan     = self.planner(question=question)
            queries  = plan.search_queries   # ← typed list

            # Step 2: Execute searches
            findings = [self.search_fn(q) for q in queries]

            # Step 3: Synthesize into answer
            return self.synthesize(question=question, findings=findings)

except ImportError:
    ResearchAgent = None


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: RAG Pipeline (Retrieve + Generate)
# ═══════════════════════════════════════════════════════════
try:
    import dspy

    class RAGSignature(dspy.Signature):
        """Answer a question using retrieved context from knowledge base."""
        context:  list[str] = dspy.InputField(desc="Relevant passages from knowledge base")
        question: str       = dspy.InputField()
        answer:   str       = dspy.OutputField(desc="Answer grounded in the provided context")
        source:   str       = dspy.OutputField(desc="Which context passage(s) support this answer")

    class DSPyRAGPipeline(dspy.Module):
        """
        Complete RAG pipeline using DSPy:
        1. Retrieve relevant passages (dspy.Retrieve or custom)
        2. Generate answer from passages

        Advantage over traditional RAG: no hand-written prompt for generation step.
        Optimizer can improve both retrieval and generation jointly.
        """
        def __init__(self, k: int = 3, retriever=None):
            super().__init__()
            self.k         = k
            self.retriever = retriever   # pass a real retriever in production
            self.generate  = dspy.ChainOfThought(RAGSignature)

        def _mock_retrieve(self, query: str) -> list:
            """Simulated retrieval — replace with real vector DB."""
            return [
                f"Passage 1 about {query}: Key information here.",
                f"Passage 2 about {query}: Supporting details here.",
                f"Passage 3 about {query}: Additional context here.",
            ][:self.k]

        def forward(self, question: str) -> dspy.Prediction:
            # Step 1: Retrieve relevant passages
            if self.retriever:
                passages = self.retriever(question, k=self.k).passages
            else:
                passages = self._mock_retrieve(question)

            # Step 2: Generate answer from passages (no hand-written prompt!)
            return self.generate(context=passages, question=question)

except ImportError:
    DSPyRAGPipeline = None


# ═══════════════════════════════════════════════════════════
# TEMPLATE 5: Optimizer (BootstrapFewShot)
# ═══════════════════════════════════════════════════════════
def template_optimizer_example():
    """
    Demonstrates the optimizer pattern.
    In production: replace mock data with real labeled examples.
    """
    import dspy

    class Classify(dspy.Signature):
        """Classify customer message sentiment."""
        message:   str = dspy.InputField()
        sentiment: str = dspy.OutputField(desc="One of: positive, negative, neutral")

    # Training examples (replace with your real data)
    mock_trainset = [
        dspy.Example(message="Great product!", sentiment="positive").with_inputs("message"),
        dspy.Example(message="This is broken", sentiment="negative").with_inputs("message"),
        dspy.Example(message="Arrived on time", sentiment="neutral").with_inputs("message"),
        dspy.Example(message="Love it!",        sentiment="positive").with_inputs("message"),
    ]

    # Metric: prediction matches expected output
    def accuracy_metric(example, prediction, trace=None) -> bool:
        return example.sentiment.lower() == prediction.sentiment.lower()

    # Compile (optimize) the module
    optimizer  = dspy.BootstrapFewShot(metric=accuracy_metric, max_bootstrapped_demos=2)
    base       = dspy.Predict(Classify)
    optimized  = optimizer.compile(student=base, trainset=mock_trainset)

    # Use optimized module
    result = optimized(message="This product exceeded my expectations!")
    return result.sentiment


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("DSPy Signature Templates — Demo")
    print("=" * 60)
    print()

    print("TEMPLATE 1: Basic Signature + Predict")
    print("  class Summarize(dspy.Signature):")
    print("      document: str = dspy.InputField()")
    print("      summary:  str = dspy.OutputField()")
    print("  summarizer = dspy.Predict(Summarize)")
    print("  result = summarizer(document='...')")
    print("  print(result.summary)  ← typed output, no parsing")
    print()

    print("TEMPLATE 2: ChainOfThought")
    print("  analyst = dspy.ChainOfThought(AnalyzeAndRecommend)")
    print("  result.reasoning     ← internal thought process")
    print("  result.recommendation ← final typed output")
    print()

    print("TEMPLATE 3: ResearchAgent (dspy.Module)")
    print("  agent = ResearchAgent()")
    print("  result = agent('What caused the 2008 financial crisis?')")
    print("  Multi-step: plan → search → synthesize")
    print()

    print("TEMPLATE 4: DSPyRAGPipeline")
    print("  rag = DSPyRAGPipeline(k=3)")
    print("  result = rag('What is our return policy?')")
    print("  No hand-written prompt for generation step!")
    print()

    print("TEMPLATE 5: Optimizer")
    print("  optimizer = dspy.BootstrapFewShot(metric=accuracy_metric)")
    print("  optimized = optimizer.compile(student=module, trainset=data)")
    print("  → DSPy finds best few-shot examples automatically")
    print()

    # Simulated DSPy check
    try:
        import dspy
        print("--- DSPy is installed. To run with API: set ANTHROPIC_API_KEY ---")
        print("    Then call: setup_dspy() and use any template above.")
    except ImportError:
        print("--- DSPy not installed. Run: pip install dspy ---")

    print()
    print("Key: declare signature → create module → call with inputs → use typed output")
