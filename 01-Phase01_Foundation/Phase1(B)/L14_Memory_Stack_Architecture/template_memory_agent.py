"""
TEMPLATE: Memory Agent Patterns
================================
4 memory strategies — from simple to production-grade.

pip install: pip install anthropic python-dotenv

All 4 templates include simulated demos (no API key needed to run).
"""
import json, os
from dotenv import load_dotenv

load_dotenv()


# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Full History Agent (Layer 2 — Working Memory)
# ═══════════════════════════════════════════════════════════
class FullHistoryAgent:
    """
    Simplest memory pattern. Keeps every turn.
    Works great for short sessions. Breaks at ~200+ turns.
    """
    def __init__(self, model: str = "claude-sonnet-5-5"):
        import anthropic
        self.client  = anthropic.Anthropic()
        self.model   = model
        self.history = []     # Layer 2: full history

    def chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=self.history   # ← entire history sent every time
        )
        reply = response.content[0].text
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        self.history = []

    def turn_count(self) -> int:
        return len(self.history) // 2


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: Sliding Window Agent (Layer 2 — Capped)
# ═══════════════════════════════════════════════════════════
class SlidingWindowAgent:
    """
    Fixed-size context window. Keeps last N turns only.
    Memory-safe for long conversations.
    Tradeoff: early turns forgotten after N turns.
    """
    def __init__(self, window_size: int = 10, model: str = "claude-sonnet-5-5"):
        import anthropic
        self.client      = anthropic.Anthropic()
        self.model       = model
        self.window_size = window_size
        self.all_history = []    # full log (for audit)

    def chat(self, user_input: str) -> str:
        self.all_history.append({"role": "user", "content": user_input})

        # Slide the window — only send last N turns to LLM
        recent = self.all_history[-self.window_size:]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=recent   # ← truncated to window_size
        )
        reply = response.content[0].text
        self.all_history.append({"role": "assistant", "content": reply})
        return reply

    def total_turns(self) -> int:
        return len(self.all_history) // 2

    def visible_turns(self) -> int:
        return min(self.total_turns(), self.window_size // 2)


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: Summarization Agent (Layer 2 — Compressed)
# ═══════════════════════════════════════════════════════════
class SummarizationAgent:
    """
    Best of both worlds: compress old history, keep recent turns crisp.
    Never overflows context. Some detail lost in summary.
    """
    def __init__(self, compress_after: int = 10, keep_recent: int = 4,
                 model: str = "claude-sonnet-5-5"):
        import anthropic
        self.client         = anthropic.Anthropic()
        self.model          = model
        self.compress_after = compress_after  # trigger compression at N turns
        self.keep_recent    = keep_recent     # always keep last N turns raw
        self.recent         = []              # high-resolution recent turns
        self.summary        = ""             # compressed old history

    def _compress(self):
        """Compress old turns into a summary paragraph."""
        if not self.recent:
            return

        # Build text of old turns (all except last keep_recent)
        old_turns = self.recent[:-self.keep_recent]
        if not old_turns:
            return

        convo_text = "\n".join(
            f"{m['role'].upper()}: {m['content'][:200]}"
            for m in old_turns
        )

        # Use cheap model to summarize
        response = self.client.messages.create(
            model="claude-haiku-5-5",   # cheaper for compression
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": (
                    f"Summarize this conversation in 2-3 sentences, "
                    f"preserving key facts and decisions:\n\n{convo_text}"
                )
            }]
        )
        new_summary = response.content[0].text

        # Update summary and trim recent
        if self.summary:
            self.summary = f"{self.summary} {new_summary}"
        else:
            self.summary = new_summary

        self.recent = self.recent[-self.keep_recent:]   # keep only recent
        print(f"  [Memory compressed. Summary: {self.summary[:60]}...]")

    def chat(self, user_input: str) -> str:
        # Check if compression needed
        if len(self.recent) >= self.compress_after:
            self._compress()

        self.recent.append({"role": "user", "content": user_input})

        # Build context: summary (if any) + recent turns
        messages = []
        if self.summary:
            messages.append({
                "role": "user",
                "content": f"[Previous conversation summary: {self.summary}]"
            })
            messages.append({
                "role": "assistant",
                "content": "I have that context, thank you."
            })
        messages.extend(self.recent)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=messages
        )
        reply = response.content[0].text
        self.recent.append({"role": "assistant", "content": reply})
        return reply


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: Persistent Agent (Layer 4 — Episodic)
# ═══════════════════════════════════════════════════════════
class PersistentAgent:
    """
    Remembers users across sessions using JSON files.
    Layer 4 (episodic) + Layer 2 (working) combined.
    Profile loaded at startup, saved after every change.
    """
    def __init__(self, user_id: str, model: str = "claude-sonnet-5-5",
                 storage_dir: str = "./user_profiles"):
        import anthropic
        self.client     = anthropic.Anthropic()
        self.model      = model
        self.user_id    = user_id
        self.storage_dir = storage_dir
        self.filepath   = os.path.join(storage_dir, f"{user_id}.json")
        self.profile    = self._load()    # Layer 4: load from disk
        self.history    = []             # Layer 2: current session

        os.makedirs(storage_dir, exist_ok=True)

    def _load(self) -> dict:
        """Load user profile. Returns default if new user."""
        if os.path.exists(self.filepath):
            with open(self.filepath) as f:
                return json.load(f)
        return {
            "user_id":    self.user_id,
            "name":       None,
            "preferences":{},
            "topics":     [],
            "turns_total": 0
        }

    def _save(self):
        """Persist profile to disk immediately."""
        os.makedirs(self.storage_dir, exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self.profile, f, indent=2)

    def remember(self, key: str, value):
        """Store a fact about this user (persisted to disk)."""
        self.profile[key] = value
        self._save()

    def recall(self, key: str, default=None):
        """Retrieve a stored fact about this user."""
        return self.profile.get(key, default)

    def _build_system_prompt(self) -> str:
        """Build system prompt with user memory injected."""
        lines = ["You are a helpful, personalized assistant."]
        if self.profile.get("name"):
            lines.append(f"The user's name is: {self.profile['name']}")
        if self.profile.get("preferences"):
            lines.append(f"Their preferences: {self.profile['preferences']}")
        if self.profile.get("topics"):
            recent_topics = self.profile["topics"][-3:]   # last 3 topics
            lines.append(f"Recent topics they asked about: {', '.join(recent_topics)}")
        lines.append("Use this context to personalize responses.")
        return "\n".join(lines)

    def chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self._build_system_prompt(),   # ← Layer 4 injected into Layer 1
            messages=self.history[-20:]           # ← Layer 2 (last 20 turns)
        )
        reply = response.content[0].text
        self.history.append({"role": "assistant", "content": reply})

        # Update profile stats
        self.profile["turns_total"] = self.profile.get("turns_total", 0) + 1
        self._save()

        return reply

    def get_profile_summary(self) -> str:
        return f"User: {self.profile.get('name', 'unknown')} | Turns: {self.profile.get('turns_total', 0)}"


# ═══════════════════════════════════════════════════════════
# DEMO (no API key needed)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("Memory Agent Templates — Demo (Simulated)")
    print("=" * 60)
    print()

    print("TEMPLATE 1: FullHistoryAgent")
    print("  agent = FullHistoryAgent()")
    print("  agent.chat('My name is Alex')")
    print("  agent.chat('What did I just say?')  ← remembers")
    print("  agent.turn_count()                  → 2")
    print()

    print("TEMPLATE 2: SlidingWindowAgent(window_size=10)")
    print("  agent = SlidingWindowAgent(window_size=10)")
    print("  After 11 turns: turn 1 is forgotten")
    print("  agent.total_turns()   → 11")
    print("  agent.visible_turns() → 5  (last 5 remembered)")
    print()

    print("TEMPLATE 3: SummarizationAgent(compress_after=10)")
    print("  agent = SummarizationAgent()")
    print("  After 10 turns: old turns compressed to summary")
    print("  Summary injected into next context window")
    print()

    print("TEMPLATE 4: PersistentAgent(user_id='alex_123')")
    print("  agent = PersistentAgent('alex_123')")
    print("  agent.remember('name', 'Alex')    # saved to disk")
    print("  agent.recall('name')              → 'Alex'")
    print("  [next session] agent = PersistentAgent('alex_123')")
    print("  agent.recall('name')              → 'Alex'  (still there!)")
    print()

    # Demonstrate PersistentAgent profile save/load (no API needed)
    print("--- Simulated Persistent Memory Demo ---")
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # Simulate session 1
        agent = PersistentAgent("user_test", storage_dir=tmpdir)
        agent.remember("name", "Alex")
        agent.remember("preferences", {"language": "English", "style": "brief"})
        print(f"Session 1 saved: {agent.get_profile_summary()}")

        # Simulate session 2 (new agent object, same user_id)
        agent2 = PersistentAgent("user_test", storage_dir=tmpdir)
        print(f"Session 2 loaded: name = {agent2.recall('name')}")
        print(f"                  prefs = {agent2.recall('preferences')}")

    print()
    print("To run with real API: set ANTHROPIC_API_KEY in .env")
    print("Then use: agent.chat('Your message here')")
