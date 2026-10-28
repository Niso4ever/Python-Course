"""Exact-string fixes: prices keyed to models + prose model names.
Prices: platform.claude.com/docs/en/about-claude/models/overview (retrieved 2026-10-28):
Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, Haiku 5.5 from $0.10/$0.50 per MTok."""
import sys
from pathlib import Path
R = Path("/home/niso4ever/AIarch/1-Course")
P1 = "1-Phase1_Foundation/Phase1(A)"
FIX = {
 f"{P1}/L05_Functions_as_Tools/template_llm_caller.py": [
  ('"claude-sonnet-5-5": {"input": 0.000003, "output": 0.000015}', '"claude-sonnet-5-5": {"input": 0.000002, "output": 0.00001}'),
  ('"claude-opus-5-5":     {"input": 0.000015, "output": 0.000075}', '"claude-opus-5-5":     {"input": 0.000004, "output": 0.00002}'),
  ('"claude-haiku-5-5":    {"input": 0.00000025, "output": 0.00000125}', '"claude-haiku-5-5":    {"input": 0.0000001, "output": 0.0000005}'),
  ('{"input": 0.000003, "output": 0.000015})', '{"input": 0.000002, "output": 0.00001})')],
 f"{P1}/L06_Classes_as_Blueprints/template_rag_agent.py": [
  ('"claude-sonnet-5-5":         {"input": 0.000003, "output": 0.000015}', '"claude-sonnet-5-5":         {"input": 0.000002, "output": 0.00001}'),
  ('"claude-haiku-5-5": {"input": 0.00000025, "output": 0.00000125}', '"claude-haiku-5-5":          {"input": 0.0000001, "output": 0.0000005}'),
  ('"claude-opus-5-5":           {"input": 0.000015, "output": 0.000075}', '"claude-opus-5-5":           {"input": 0.000004, "output": 0.00002}'),
  ('{"input": 0.000003, "output": 0.000015})', '{"input": 0.000002, "output": 0.00001})')],
 f"{P1}/L06_Classes_as_Blueprints/template_multi_tool_agent.py": [
  ('"fast":     0.00000025,', '"fast":     0.0000001, '), ('"balanced": 0.000003,', '"balanced": 0.000002,'), ('"powerful": 0.000015', '"powerful": 0.000004')],
 "1-Phase1_Foundation/Phase1(B)/L12_Advanced_Debugging/template_debug_toolkit.py": [
  ('"claude-sonnet-5-5":         {"input": 0.000003, "output": 0.000015}', '"claude-sonnet-5-5":         {"input": 0.000002, "output": 0.00001}'),
  ('"claude-opus-5-5":           {"input": 0.000015, "output": 0.000075}', '"claude-opus-5-5":           {"input": 0.000004, "output": 0.00002}'),
  ('"claude-haiku-5-5": {"input": 0.00000025, "output": 0.00000125}', '"claude-haiku-5-5":          {"input": 0.0000001, "output": 0.0000005}')],
 "1-Phase1_Foundation/Phase1(B)/L20_Evaluation_Metrics/CHEATSHEET_L20.py": [
  ("# claude-sonnet-5-5: $0.003/1K input, $0.015/1K output", "# claude-sonnet-5-5: $0.002/1K input, $0.010/1K output (pricing page, 2026-10-28)")],
 "2-Phase3_RealSystems/Project1_RAG_Pipeline/main.py": [
  ("# Rough cost estimate: Sonnet 4.6 ~$3/M input, $15/M output", "# Rough cost estimate: Sonnet 5.5 ~$2/M input, $10/M output (pricing page, 2026-10-28)"),
  ('result["tokens"]["input"] * 0.000003 +', 'result["tokens"]["input"] * 0.000002 +'),
  ('result["tokens"]["output"] * 0.000015)', 'result["tokens"]["output"] * 0.00001)'),
  ("Powered by Claude Sonnet 4.6", "Powered by Claude Sonnet 5.5"), ("REAL (Claude Sonnet 4.6 + ChromaDB)", "REAL (Claude Sonnet 5.5 + ChromaDB)")],
 "2-Phase3_RealSystems/Project1_RAG_Pipeline/retriever.py": [("Claude Sonnet 4.6 would", "Claude Sonnet 5.5 would")],
 "2-Phase3_RealSystems/Project1_RAG_Pipeline/README.md": [("→ Claude Sonnet 4.6", "→ Claude Sonnet 5.5")],
 "2-Phase3_RealSystems/Project2_Agent_with_Tools/README.md": [("(Claude Opus 4.6)", "(Claude Opus 5.5)")],
 "2-Phase3_RealSystems/Project2_Agent_with_Tools/main.py": [("Claude Opus 4.6 |", "Claude Opus 5.5 |")],
 "2-Phase3_RealSystems/Project2_Agent_with_Tools/agent.py": [("use Opus 4.6 for", "use Opus 5.5 for")],
 "2-Phase3_RealSystems/Project2_Agent_with_Tools/tools.py": [
  ('"Anthropic\'s Claude family in 2026: Opus 4.6 (most capable), "', '"Anthropic\'s Claude family in late 2026: Fable 5.1 (demanding reasoning), Opus 5.5 (recommended default), "'),
  ('"Sonnet 4.6 (best value), Haiku 4.5 (fastest). "', '"Sonnet 5.5 (speed and intelligence), Haiku 5.5 (fastest). "')],
 "2-Phase3_RealSystems/Project4_DSPy_Pipeline/main.py": [("Claude Haiku 4.5\")", "Claude Haiku 5.5\")")],
 "1-Phase1_Foundation/Phase1(B)/L14_Memory_Stack_Architecture/L14_Memory_Stack_Architecture.md": [
  ("- Claude Haiku 4.5: 200K tokens ≈ 150,000 words ≈ 300-page book", "- Claude Haiku 5.5: 1M tokens ≈ 555,000 words (models overview, retrieved 2026-10-28)"),
  ("- Claude Sonnet 4.6: 200K tokens", "- Claude Sonnet 5.5: 1M tokens"), ("- Claude Opus 4.6: 200K tokens", "- Claude Opus 5.5: 1M tokens")],
 "4-Phase5_Agentic_AI/L25_Agent_Loop/template_agent_loop.py": [("Claude Opus 4 is Anthropic's most capable model as of 2026", "Claude Opus 5.5 is Anthropic's recommended default model as of late 2026")],
 "4-Phase5_Agentic_AI/L26_Direct_Tool_Use/template_tool_caller.py": [("Claude Opus 4 is the most capable version as of 2026.", "Claude Opus 5.5 is the recommended default as of late 2026; Fable 5.1 is for the hardest reasoning.")],
 "4-Phase5_Agentic_AI/L26_Direct_Tool_Use/PASS1_RECOGNITION.md": [("Claude Opus 4, Claude Sonnet 4.6, and Claude Haiku 4.5", "Claude Opus 5.5, Claude Sonnet 5.5, and Claude Haiku 5.5")],
}
apply = "--apply" in sys.argv
bad = 0
for rel, pairs in FIX.items():
    p = R / rel; t = p.read_text()
    for old, new in pairs:
        c = t.count(old)
        if c == 0: print("MISS", rel, old[:60]); bad += 1
        t = t.replace(old, new)
    if apply and not bad: p.write_text(t)
print("misses", bad, "applied" if apply and not bad else "dry")
