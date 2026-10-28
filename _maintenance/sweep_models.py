"""Replace retired/legacy Claude model IDs in 1-Course. Dry run unless --apply.

Source for mapping: platform.claude.com/docs/en/about-claude/model-deprecations (retrieved 2026-10-28).
Files that still show forced tool_choice keep a model that accepts it (forced tool_choice
returns 400 on opus-5-5 / sonnet-5-5 / fable-5-1, per the define-tools page).
"""
import re
import sys
from pathlib import Path

ROOT = Path("/home/niso4ever/AIarch/1-Course")
SKIP_DIRS = ("L09_Error_Reading",)
FORCED = {
    "10-End_to_End_Projects/Project1_Data_Pipeline/extractor.py",
    "4-Phase5_Agentic_AI/L26_Direct_Tool_Use/CHEATSHEET_L26.py",
    "4-Phase5_Agentic_AI/L26_Direct_Tool_Use/PASS1_RECOGNITION.md",
    "4-Phase5_Agentic_AI/L26_Direct_Tool_Use/PASS3_TEMPLATES.md",
    "4-Phase5_Agentic_AI/L26_Direct_Tool_Use/PASS_C_VISUAL.md",
    "4-Phase5_Agentic_AI/L27_Structured_Output/CHEATSHEET_L27.py",
    "4-Phase5_Agentic_AI/L27_Structured_Output/PASS1_RECOGNITION.md",
    "4-Phase5_Agentic_AI/L27_Structured_Output/PASS3_TEMPLATES.md",
    "4-Phase5_Agentic_AI/L27_Structured_Output/PASS_C_VISUAL.md",
    "4-Phase5_Agentic_AI/L27_Structured_Output/README.md",
    "4-Phase5_Agentic_AI/L28_MultiAgent_Orchestration/PASS1_RECOGNITION.md",
    "4-Phase5_Agentic_AI/L28_MultiAgent_Orchestration/PASS3_TEMPLATES.md",
    "3-Phase4_ToolUse_FunctionCalling/CHEATSHEET.md",
}

END = r"(?![-\w.])"
CURRENT = [
    (r"claude-3-opus(?:-20240229)?" + END, "claude-opus-5-5"),
    (r"claude-opus-4-[68]" + END, "claude-opus-5-5"),
    (r"claude-3-5-sonnet(?:-20241022)?" + END, "claude-sonnet-5-5"),
    (r"claude-3-sonnet" + END, "claude-sonnet-5-5"),
    (r"claude-sonnet-4-6" + END, "claude-sonnet-5-5"),
    (r"claude-3-haiku(?:-20240307)?" + END, "claude-haiku-5-5"),
    (r"claude-haiku-4-5(?:-20251001)?" + END, "claude-haiku-5-5"),
    (r"claude-fable-5" + END, "claude-fable-5-1"),
]
# Forced-tool files: only retired IDs move, to replacements that still accept forced tool_choice.
RETIRED_ONLY = [
    (r"claude-3-opus(?:-20240229)?" + END, "claude-opus-4-8"),
    (r"claude-3-5-sonnet(?:-20241022)?" + END, "claude-sonnet-4-6"),
    (r"claude-3-sonnet" + END, "claude-sonnet-4-6"),
    (r"claude-3-haiku(?:-20240307)?" + END, "claude-haiku-5-5"),
    (r"claude-haiku-4-5(?:-20251001)?" + END, "claude-haiku-5-5"),
]


def main(apply: bool) -> None:
    total = 0
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in {".py", ".md", ".txt"} or not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(d in rel for d in SKIP_DIRS):
            continue
        rules = RETIRED_ONLY if rel in FORCED else CURRENT
        text = path.read_text()
        new, n = text, 0
        for pat, rep in rules:
            new, k = re.subn(pat, rep, new)
            n += k
        if n:
            total += n
            print(f"{n:4d}  {'[forced] ' if rel in FORCED else ''}{rel}")
            if apply:
                path.write_text(new)
    print("total", total, "(applied)" if apply else "(dry run)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
