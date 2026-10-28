"""
TEMPLATE: Conversation Agent
==============================
Use: Chat agents that remember conversation history

COPY this when you need to:
- Build a chatbot that remembers previous messages
- Create a multi-turn conversation loop
- Add system prompt / persona to an agent
- Track turn count or conversation length

2026 NOTE: Three class styles shown in AI code.
  This file = standard class (has methods + memory).
  For config containers, see @dataclass pattern in CHEATSHEET_L06.py.
  For LLM output validation, see Pydantic BaseModel in CHEATSHEET_L06.py.
"""

# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Basic Conversation Agent
# ═══════════════════════════════════════════════════════════
class ConversationAgent:
    """
    The foundational conversation agent.
    Remembers full history across all turns.

    IN:  model_name (str), system_prompt (str)
    USE: agent.chat(user_input) → response (str)
    """
    def __init__(self, model_name, system_prompt):
        self.model   = model_name
        self.system  = system_prompt
        self.history = []               # Grows with each turn
        self.turns   = 0                # Counts total exchanges

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        self.turns += 1

        # ── Uncomment to use real API ──────────────────────
        # import anthropic
        # client = anthropic.Anthropic()
        # response = client.messages.create(
        #     model=self.model,
        #     max_tokens=1000,
        #     system=self.system,
        #     messages=self.history
        # )
        # reply = response.content[0].text
        # ───────────────────────────────────────────────────

        # ← REMOVE when using real API:
        reply = f"[Simulated reply to: '{user_input[:30]}...' | turn {self.turns}]"

        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        """Start a fresh conversation, keep config."""
        self.history = []
        self.turns   = 0

    def get_stats(self):
        return {
            "model":  self.model,
            "turns":  self.turns,
            "messages_stored": len(self.history)
        }


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: Agent with Token Estimation
# ═══════════════════════════════════════════════════════════
class TokenAwareAgent:
    """
    Conversation agent that estimates token usage.
    Useful for cost tracking and context window management.

    IN:  model_name (str), system_prompt (str), max_context (int)
    USE: agent.chat(user_input) → response (str)
    """
    def __init__(self, model_name, system_prompt, max_context=4000):
        self.model       = model_name
        self.system      = system_prompt
        self.history     = []
        self.max_context = max_context
        self.total_tokens = 0

    def _estimate_tokens(self, text):
        """Rough estimate: 1 token ≈ 4 characters."""
        return len(text) // 4

    def chat(self, user_input):
        token_estimate = self._estimate_tokens(user_input)
        self.total_tokens += token_estimate

        self.history.append({"role": "user", "content": user_input})

        # Check context window before calling
        if self.total_tokens > self.max_context:
            return "Context window full. Call agent.reset() to start fresh."

        # ── Uncomment to use real API ──────────────────────
        # import anthropic
        # client = anthropic.Anthropic()
        # response = client.messages.create(
        #     model=self.model,
        #     max_tokens=1000,
        #     system=self.system,
        #     messages=self.history
        # )
        # reply = response.content[0].text
        # ───────────────────────────────────────────────────

        reply = f"[Simulated | tokens so far: ~{self.total_tokens}]"

        self.history.append({"role": "assistant", "content": reply})
        self.total_tokens += self._estimate_tokens(reply)
        return reply

    def reset(self):
        self.history      = []
        self.total_tokens = 0

    def get_usage(self):
        return {
            "total_tokens_est": self.total_tokens,
            "turns":            len(self.history) // 2,
            "context_used_pct": round(self.total_tokens / self.max_context * 100, 1)
        }


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: Agent with Sliding Window Memory
# ═══════════════════════════════════════════════════════════
class SlidingWindowAgent:
    """
    Keeps only the N most recent messages to stay within context.
    Older messages are dropped automatically.

    IN:  model_name (str), system_prompt (str), window_size (int)
    USE: agent.chat(user_input) → response (str)
    """
    def __init__(self, model_name, system_prompt, window_size=10):
        self.model       = model_name
        self.system      = system_prompt
        self.history     = []
        self.window_size = window_size   # Max messages to keep
        self.total_turns = 0

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        self.total_turns += 1

        # Trim to window size (keep most recent messages)
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size:]

        # ── Uncomment to use real API ──────────────────────
        # import anthropic
        # client = anthropic.Anthropic()
        # response = client.messages.create(
        #     model=self.model,
        #     max_tokens=1000,
        #     system=self.system,
        #     messages=self.history
        # )
        # reply = response.content[0].text
        # ───────────────────────────────────────────────────

        reply = f"[Simulated | window={len(self.history)} msgs | turn {self.total_turns}]"

        self.history.append({"role": "assistant", "content": reply})
        return reply

    def get_stats(self):
        return {
            "total_turns":   self.total_turns,
            "active_window": len(self.history),
            "window_size":   self.window_size
        }


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: Agent with Turn Limit (Guard Rail)
# ═══════════════════════════════════════════════════════════
class LimitedTurnAgent:
    """
    Conversation agent that stops after N turns.
    Useful for demos, testing, and cost control.

    IN:  model_name (str), system_prompt (str), max_turns (int)
    USE: agent.chat(user_input) → response or limit message (str)
    """
    def __init__(self, model_name, system_prompt, max_turns=5):
        self.model     = model_name
        self.system    = system_prompt
        self.history   = []
        self.max_turns = max_turns
        self.turns     = 0
        self.active    = True

    def chat(self, user_input):
        if not self.active:
            return f"Turn limit ({self.max_turns}) reached. Call reset() to continue."

        self.turns += 1
        self.history.append({"role": "user", "content": user_input})

        # ── Uncomment to use real API ──────────────────────
        # import anthropic
        # client = anthropic.Anthropic()
        # response = client.messages.create(
        #     model=self.model,
        #     max_tokens=1000,
        #     system=self.system,
        #     messages=self.history
        # )
        # reply = response.content[0].text
        # ───────────────────────────────────────────────────

        reply = f"[Simulated | turn {self.turns}/{self.max_turns}]"

        self.history.append({"role": "assistant", "content": reply})

        # Deactivate when limit hit
        if self.turns >= self.max_turns:
            self.active = False

        return reply

    def reset(self):
        self.history = []
        self.turns   = 0
        self.active  = True


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("TEMPLATE 1: Basic Conversation Agent")
    print("=" * 60)
    agent = ConversationAgent("claude-sonnet-5-5", "You are helpful.")
    r1 = agent.chat("What is RAG?")
    r2 = agent.chat("Give me an example.")
    print(f"Turn 1: {r1}")
    print(f"Turn 2: {r2}")
    print(f"Stats:  {agent.get_stats()}")
    print(f"History length: {len(agent.history)} messages")

    print("\n" + "=" * 60)
    print("TEMPLATE 2: Token-Aware Agent")
    print("=" * 60)
    ta = TokenAwareAgent("claude-sonnet-5-5", "You are concise.", max_context=500)
    ta.chat("Hello, what can you do?")
    ta.chat("Tell me about vector databases.")
    print(f"Usage: {ta.get_usage()}")

    print("\n" + "=" * 60)
    print("TEMPLATE 3: Sliding Window (keeps last 4 messages)")
    print("=" * 60)
    sw = SlidingWindowAgent("claude-sonnet-5-5", "You are helpful.", window_size=4)
    sw.chat("Message 1")
    sw.chat("Message 2")
    sw.chat("Message 3")
    sw.chat("Message 4 — oldest will be dropped next")
    sw.chat("Message 5 — now message 1 is gone")
    print(f"Stats: {sw.get_stats()}")

    print("\n" + "=" * 60)
    print("TEMPLATE 4: Turn-Limited Agent (max 3 turns)")
    print("=" * 60)
    la = LimitedTurnAgent("claude-sonnet-5-5", "You are helpful.", max_turns=3)
    print(la.chat("Question 1"))
    print(la.chat("Question 2"))
    print(la.chat("Question 3 — this is the last one"))
    print(la.chat("Question 4 — should be blocked"))
