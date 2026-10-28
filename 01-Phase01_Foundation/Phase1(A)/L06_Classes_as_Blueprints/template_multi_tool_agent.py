"""
TEMPLATE: Multi-Tool Agent
============================
Use: Agents that route between models or select from multiple tools

COPY this when you need to:
- Route questions to different LLM models (fast/balanced/powerful)
- Build an agent with a registry of callable tools
- Create fallback chains (try A, then B, then C)
- Centralize all agent configuration in one place

2026 NOTE: Three class styles shown in AI code.
  This file = standard class (has methods + memory).
  For config containers, see @dataclass pattern in CHEATSHEET_L06.py.
  For LLM output validation, see Pydantic BaseModel in CHEATSHEET_L06.py.
"""

# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Multi-Model Router
# ═══════════════════════════════════════════════════════════
class MultiModelAgent:
    """
    Routes questions to different Claude models based on mode.
    Tracks per-model usage automatically.

    IN:  (no params — uses built-in model map)
    USE: agent.answer(question, mode="balanced") → response (str)
    """
    def __init__(self):
        self.models = {
            "fast":      "claude-haiku-5-5",   # Speed priority
            "balanced":  "claude-sonnet-5-5",            # Default
            "powerful":  "claude-opus-5-5"               # Quality priority
        }
        self.usage = {"fast": 0, "balanced": 0, "powerful": 0}
        self.cost_estimate = {
            "fast":     0.0000001,    # per token (rough input rate)
            "balanced": 0.000002,
            "powerful": 0.000004
        }
        self.total_calls = 0

    def answer(self, question, mode="balanced"):
        if mode not in self.models:
            return f"Unknown mode '{mode}'. Choose: fast, balanced, powerful"

        model = self.models[mode]          # L1: dict lookup
        self.usage[mode] += 1             # L1: update counter
        self.total_calls += 1

        # ── Uncomment to use real API ──────────────────────
        # import anthropic
        # client = anthropic.Anthropic()
        # response = client.messages.create(
        #     model=model,
        #     max_tokens=1000,
        #     messages=[{"role": "user", "content": question}]
        # )
        # return response.content[0].text
        # ───────────────────────────────────────────────────

        return f"[Simulated | mode={mode} | model={model} | q='{question[:30]}...']"

    def usage_report(self):
        return {
            "total_calls": self.total_calls,
            "per_model":   self.usage
        }

    def recommend_mode(self, task_type):
        """Simple mode recommender based on task description."""
        task_lower = task_type.lower()
        if any(w in task_lower for w in ["quick", "simple", "yes/no", "classify"]):
            return "fast"
        elif any(w in task_lower for w in ["analyze", "explain", "research", "complex"]):
            return "powerful"
        else:
            return "balanced"


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: Tool Registry Agent
# ═══════════════════════════════════════════════════════════
class ToolRegistryAgent:
    """
    Agent with a registry of named tools.
    Selects and runs the right tool for each task.

    IN:  tools (list of tool objects with .name, .can_handle(), .execute())
    USE: agent.run(task) → result (str)
    """
    def __init__(self, tools):
        self.tools    = tools            # List of tool objects
        self.results  = []              # All past results
        self.calls    = 0               # Total tool activations
        self.registry = {               # Name → tool lookup
            tool.name: tool for tool in tools
        }

    def run(self, task):
        self.calls += 1

        # Loop through tools, use first match (L2.5 + L2 combined)
        for tool in self.tools:
            if tool.can_handle(task):
                result = tool.execute(task)
                self.results.append({
                    "task":   task,
                    "tool":   tool.name,
                    "result": result
                })
                return result

        # No tool matched — return fallback
        return f"No tool available for: {task}"

    def run_by_name(self, tool_name, task):
        """Directly call a specific tool by name."""
        if tool_name in self.registry:
            return self.registry[tool_name].execute(task)
        return f"Tool '{tool_name}' not found. Available: {list(self.registry.keys())}"

    def get_history(self):
        return self.results

    def list_tools(self):
        return [tool.name for tool in self.tools]


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: Fallback Chain Agent
# ═══════════════════════════════════════════════════════════
class FallbackChainAgent:
    """
    Tries primary → secondary → tertiary in order.
    Falls back automatically if a source fails or returns nothing.

    IN:  sources (list of callables: primary, secondary, fallback)
    USE: agent.query(question) → result (str)
    """
    def __init__(self, sources):
        self.sources      = sources      # Ordered list: best → fallback
        self.query_count  = 0
        self.fallback_log = []           # Track when fallbacks triggered

    def query(self, question):
        self.query_count += 1

        for i, source in enumerate(self.sources):
            try:
                result = source(question)
                if result:
                    if i > 0:
                        self.fallback_log.append({
                            "question": question[:50],
                            "used_fallback_level": i
                        })
                    return result
            except Exception as e:
                print(f"Source {i} failed: {e}. Trying next...")

        return "All sources failed. No answer available."

    def get_fallback_stats(self):
        return {
            "total_queries":     self.query_count,
            "fallbacks_used":    len(self.fallback_log),
            "fallback_rate_pct": round(len(self.fallback_log) / max(self.query_count, 1) * 100, 1),
            "fallback_log":      self.fallback_log
        }


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: Config Manager (Central Settings)
# ═══════════════════════════════════════════════════════════
class AgentConfig:
    """
    Singleton configuration class.
    Store all agent settings in one place.

    IN:  (no params — loads defaults, can be overridden)
    USE: config.model, config.is_confident(score), etc.
    """
    def __init__(self):
        # Model settings
        self.model       = "claude-sonnet-5-5"
        self.temperature = 0.7
        self.max_tokens  = 1000

        # Thresholds
        self.thresholds = {
            "confidence": 0.85,
            "toxicity":   0.20,
            "relevance":  0.70
        }

        # RAG settings
        self.top_k        = 3
        self.chunk_size   = 500
        self.chunk_overlap = 50

        # Cost limits
        self.max_cost_per_session = 1.00   # USD
        self.max_tokens_per_call  = 2000

    # Threshold checkers (L2 logic inside L4 class)
    def is_confident(self, score):
        return score >= self.thresholds["confidence"]

    def is_safe(self, toxicity_score):
        return toxicity_score < self.thresholds["toxicity"]

    def is_relevant(self, relevance_score):
        return relevance_score >= self.thresholds["relevance"]

    def to_dict(self):
        """Export all settings as a dict."""
        return {
            "model":       self.model,
            "temperature": self.temperature,
            "max_tokens":  self.max_tokens,
            "thresholds":  self.thresholds,
            "rag":         {"top_k": self.top_k, "chunk_size": self.chunk_size}
        }


# ═══════════════════════════════════════════════════════════
# SIMULATED TOOLS (for demo)
# ═══════════════════════════════════════════════════════════
class WebSearchTool:
    name = "web_search"
    def can_handle(self, task):
        return "search" in task.lower() or "find" in task.lower()
    def execute(self, task):
        return f"[Web search results for: '{task}']"

class CalculatorTool:
    name = "calculator"
    def can_handle(self, task):
        return any(op in task for op in ["+", "-", "*", "/", "calculate", "compute"])
    def execute(self, task):
        return f"[Calculation result for: '{task}']"

class SummaryTool:
    name = "summarizer"
    def can_handle(self, task):
        return "summarize" in task.lower() or "summary" in task.lower()
    def execute(self, task):
        return f"[Summary of: '{task[:40]}...']"


# ═══════════════════════════════════════════════════════════
# DEMO (runnable!)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("TEMPLATE 1: Multi-Model Router")
    print("=" * 60)
    router = MultiModelAgent()
    print(router.answer("Is 2+2=4?", mode="fast"))
    print(router.answer("Explain quantum entanglement", mode="balanced"))
    print(router.answer("Deep analysis of market trends", mode="powerful"))

    # Recommender
    print(f"\nRecommended mode for 'quick yes/no': {router.recommend_mode('quick yes/no')}")
    print(f"Recommended mode for 'complex analysis': {router.recommend_mode('complex analysis')}")
    print(f"\nUsage report: {router.usage_report()}")

    print("\n" + "=" * 60)
    print("TEMPLATE 2: Tool Registry Agent")
    print("=" * 60)
    tools = [WebSearchTool(), CalculatorTool(), SummaryTool()]
    agent = ToolRegistryAgent(tools)

    print(f"Available tools: {agent.list_tools()}")
    print(agent.run("search for AI papers"))
    print(agent.run("calculate 45 * 12"))
    print(agent.run("summarize this document"))
    print(agent.run("generate a poem"))   # No tool matches

    print(f"\nHistory ({len(agent.get_history())} results):")
    for item in agent.get_history():
        print(f"  [{item['tool']}] {item['task'][:40]} → {item['result'][:50]}")

    print("\n" + "=" * 60)
    print("TEMPLATE 3: Fallback Chain")
    print("=" * 60)

    # Define three sources as lambdas (simple demo)
    primary   = lambda q: None  # Always fails (returns None)
    secondary = lambda q: f"[Secondary source answer for: {q}]"
    tertiary  = lambda q: f"[Fallback answer for: {q}]"

    chain = FallbackChainAgent([primary, secondary, tertiary])
    print(chain.query("What is RAG?"))
    print(chain.query("How does attention work?"))
    print(f"\nFallback stats: {chain.get_fallback_stats()}")

    print("\n" + "=" * 60)
    print("TEMPLATE 4: Config Manager")
    print("=" * 60)
    config = AgentConfig()
    print(f"Model:       {config.model}")
    print(f"Confident?   {config.is_confident(0.90)} (score=0.90)")
    print(f"Confident?   {config.is_confident(0.70)} (score=0.70)")
    print(f"Safe?        {config.is_safe(0.10)} (toxicity=0.10)")
    print(f"Safe?        {config.is_safe(0.35)} (toxicity=0.35)")
    print(f"\nFull config: {config.to_dict()}")
