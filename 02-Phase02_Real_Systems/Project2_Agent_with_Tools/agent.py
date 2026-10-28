"""
agent.py — ReAct Agent using Anthropic tool-use API.

This is the core agent loop from L11 (Tool Use Pattern) and L13 (ReAct),
now built into a production-ready class.

The loop:
  1. LLM receives research brief + available tools
  2. LLM reasons (Thought) → calls a tool (Action)
  3. Tool executes → result returned to LLM (Observation)
  4. LLM reasons again → calls another tool or writes Final Answer
  5. Repeat until LLM returns stop_reason="end_turn"
"""

import anthropic
from tools import TOOL_DEFINITIONS, execute_tool

# In 2026: use Opus 5.5 for complex research — it plans better and reasons deeper
AGENT_MODEL   = "claude-opus-5-5"
MAX_TOKENS    = 4000
MAX_TOOL_CALLS = 15    # safety limit on tool calls per session

SYSTEM_PROMPT = """You are a Senior AI Research Analyst at Nexus AI (2026).
You have access to tools for web search, calculations, document reading, and report writing.

Your research process:
1. Understand the research brief thoroughly
2. Plan what information you need (searches, calculations, documents)
3. Execute searches systematically — be specific in your queries
4. Use the calculator for ALL numeric calculations (never estimate math)
5. Synthesize findings into a professional, data-driven report
6. Save the final report using write_report

Report format:
- Executive Summary (2-3 sentences)
- Key Findings (3-5 bullet points with data)
- Detailed Analysis (sections with subsections)
- Data & Statistics (table format where possible)
- Conclusions & Recommendations
- Methodology (what tools you used and why)

In 2026, business leaders expect AI-generated reports to be:
- Specific (numbers, not vague claims)
- Sourced (cite what you found)
- Actionable (conclude with recommendations)
- Concise (executives read summaries, not essays)"""


class ResearchAgent:
    """
    Autonomous research agent with tool use.

    Combines patterns from:
    - L4: class with __init__ and methods
    - L11: tool use loop (stop_reason == "tool_use")
    - L13: ReAct reasoning (Thought → Action → Observe)
    - L9: async for future parallel tool calls
    """

    def __init__(self, model: str = AGENT_MODEL, verbose: bool = True):
        self.client   = anthropic.Anthropic()
        self.model    = model
        self.verbose  = verbose
        self.tool_log = []   # L4 pattern: state tracked in instance

    def _log(self, msg: str):
        """Print if verbose mode is on."""
        if self.verbose:
            print(msg)

    def _execute_and_log(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool, log the call, return result."""
        self._log(f"\n  → [{tool_name}] {str(tool_input)[:80]}")
        result = execute_tool(tool_name, tool_input)
        self._log(f"  ← Result: {str(result)[:120]}...")

        self.tool_log.append({
            "tool":   tool_name,
            "input":  tool_input,
            "result": result[:200]   # store first 200 chars for audit
        })
        return result

    def research(self, brief: str) -> dict:
        """
        Run the full research loop on a given brief.

        IN:  research brief (str)
        OUT: {answer, tool_log, messages, tool_calls_made}
        """
        self.tool_log = []   # reset for each research session
        messages = [{"role": "user", "content": brief}]
        tool_calls_made = 0
        final_answer = ""

        self._log(f"\n{'='*60}")
        self._log(f"NEXUS AI RESEARCH AGENT")
        self._log(f"Model: {self.model}")
        self._log(f"Brief: {brief[:80]}...")
        self._log(f"{'='*60}")

        for step in range(MAX_TOOL_CALLS + 1):
            # Call the LLM
            response = self.client.messages.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS,
                messages=messages
            )

            self._log(f"\n[Step {step + 1}] stop_reason={response.stop_reason}")

            # ── Done: LLM finished reasoning ────────────────
            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        final_answer = block.text
                break

            # ── Tool use: LLM wants to call a tool ──────────
            if response.stop_reason == "tool_use":
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_calls_made += 1
                        result = self._execute_and_log(block.name, block.input)
                        tool_results.append({
                            "type":        "tool_result",
                            "tool_use_id": block.id,
                            "content":     result
                        })

                messages.append({"role": "user", "content": tool_results})

            # Safety: stop if max tool calls reached
            if tool_calls_made >= MAX_TOOL_CALLS:
                self._log(f"\n[SAFETY] Max tool calls ({MAX_TOOL_CALLS}) reached.")
                break

        self._log(f"\n{'='*60}")
        self._log(f"Research complete. Tool calls: {tool_calls_made}")
        self._log(f"{'='*60}\n")

        return {
            "answer":          final_answer,
            "tool_log":        self.tool_log,
            "tool_calls_made": tool_calls_made,
            "messages":        messages
        }

    def get_tool_summary(self) -> str:
        """Return a summary of all tool calls made in the last session."""
        if not self.tool_log:
            return "No tool calls made."
        lines = [f"Tool calls made ({len(self.tool_log)} total):"]
        for i, call in enumerate(self.tool_log, 1):
            lines.append(f"  {i}. [{call['tool']}] {str(call['input'])[:60]}")
        return "\n".join(lines)
