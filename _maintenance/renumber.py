"""Renumber 1-Course so folder number = phase number (0-9) and each phase's lessons start at L01.

Dry run by default: prints what would change. Pass --apply to rewrite text and rename paths.
Run once; it is not idempotent (applied 2026-10-28).
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/home/niso4ever/AIarch/1-Course")
EXCLUDE = {"UPDATE_LOG_2026-10-28.md", ".gitignore"}
EXCLUDE_DIRS = {"_maintenance", ".claude", ".git", "__pycache__"}
TEXT_SUFFIXES = {".md", ".py", ".txt"}

TOP = {
    "0-Phase0_OOP_Introduction": "00-Phase00_OOP_Introduction",
    "1-Phase1_Foundation": "01-Phase01_Foundation",
    "2-Phase3_RealSystems": "02-Phase02_Real_Systems",
    "3-Phase4_ToolUse_FunctionCalling": "03-Phase03_Tool_Use",
    "4-Phase5_Agentic_AI": "04-Phase04_Agentic_AI",
    "5-Anthropic_Agent_SDK": "05-Phase05_Agent_SDK",
    "6-Vibe coding": "99-Vibe_Coding_Companion",
    "7-Async_for_Agents": "06-Phase06_Async",
    "8-Evals_and_Testing": "07-Phase07_Evals",
    "9-Code_Review_and_Debugging": "08-Phase08_Debugging",
    "10-End_to_End_Projects": "09-Phase09_End_to_End_Projects",
}
AGENTIC = {  # old Phase 5 lesson number -> new Phase 4 lesson number
    "00": "01", "25": "02", "26": "03", "27": "04", "28": "05", "29": "06", "30": "07", "31": "08",
}
AGENTIC_DIRS = {
    "L00_Introduction_to_Agentic_AI": "L01_Introduction_to_Agentic_AI",
    "L25_Agent_Loop": "L02_Agent_Loop",
    "L26_Direct_Tool_Use": "L03_Direct_Tool_Use",
    "L27_Structured_Output": "L04_Structured_Output",
    "L28_MultiAgent_Orchestration": "L05_MultiAgent_Orchestration",
    "L29_MCP_Tool_Standard": "L06_MCP_Tool_Standard",
    "L30_Agentic_System_Design": "L07_Agentic_System_Design",
    "L31_OpenAI_Agents_SDK": "L08_OpenAI_Agents_SDK",
}
TRACK2_DIRS = {
    "L18_PydanticAI_Framework": "L22_PydanticAI_Framework",
    "L19_Structured_Outputs": "L23_Structured_Outputs",
    "L20_Evaluation_Metrics": "L24_Evaluation_Metrics",
}
VIBE_FILES = {
    "04_Phase4_ToolUse": "04_Phase3_ToolUse",
    "05_Phase5_Agentic": "05_Phase4_Agentic",
    "06_Phase6_SDK": "06_Phase5_SDK",
    "07_Phase7_Async": "07_Phase6_Async",
    "08_Phase8_Evals": "08_Phase7_Evals",
    "09_Phase9_Debugging": "09_Phase8_Debugging",
    "10_Phase10_EndToEnd": "10_Phase9_EndToEnd",
}
LITERALS = {**TOP, **AGENTIC_DIRS, **TRACK2_DIRS, **VIBE_FILES}
LITERALS.update({f"CHEATSHEET_L{o}": f"CHEATSHEET_L{n}" for o, n in AGENTIC.items() if o != "00"})


def phase(n: int) -> int:
    """Old phase number -> new. 0 and 1 stay; 3..10 move down one (there was no Phase 2)."""
    return n if n <= 2 else n - 1  # "Phase 2" never named a course phase (e.g. step labels)


LIT_RE = "|".join(re.escape(k) for k in sorted(LITERALS, key=len, reverse=True))
TOKEN = re.compile(
    rf"(?P<lit>(?<![0-9A-Za-z])(?:{LIT_RE}))"
    r"|(?P<p5l>\bPhase 5,? L(?P<p5n>2[5-9]|3[01])\b)"
    r"|(?P<ph>\bPh(?P<phn>\d+)-L)"
    r"|(?P<ag>\bL(?P<agn>2[5-9]|3[01])\b)"
    r"|(?P<t2>\bL(?P<t2n>18|19|20)(?=[\s|*:—_-]*(?:PydanticAI|Structured|Evaluation)))"
    r"|(?P<p2>\bPhase 2[AB]\b)"
    r"|(?P<phase>\b(?P<pw>Phases?) (?P<pnums>\d+(?:\s*[–/-]\s*\d+)*))"
)


def rewrite(text: str, rel: str, stats: Counter) -> str:
    in_agentic = rel.startswith("4-Phase5_Agentic_AI/")
    track2 = next((d for d in TRACK2_DIRS if f"/{d}/" in f"/{rel}"), None)

    def sub(m: re.Match) -> str:
        if m["lit"]:
            stats["literal"] += 1
            return LITERALS[m["lit"]]
        if m["p5l"]:
            stats["phase5+lesson"] += 1
            return f"Phase 4 L{AGENTIC[m['p5n']]}"
        if m["ph"]:
            stats["Ph-prefix"] += 1
            return f"Ph{phase(int(m['phn']))}-L"
        if m["ag"]:
            stats["agentic lesson"] += 1
            new = AGENTIC[m["agn"]]
            return f"L{new}" if in_agentic else f"Ph4-L{new}"
        if m["t2"]:
            stats["track2 lesson"] += 1
            return {"18": "L22", "19": "L23", "20": "L24"}[m["t2n"]]
        if m["p2"]:
            stats["Phase 2A/2B"] += 1
            return "Phase 1B"
        nums = re.sub(r"\d+", lambda d: str(phase(int(d.group()))), m["pnums"])
        if nums != m["pnums"]:
            stats["phase label"] += 1
        return f"{m['pw']} {nums}"

    out = TOKEN.sub(sub, text)
    out = re.sub(r"\b(Ph\d+-L\d\d)([–-])Ph\d+-L", r"\1\2L", out)  # "Ph4-L02–Ph4-L08" -> "Ph4-L02–L08"
    if in_agentic:  # lesson 0 of the agentic phase becomes L01 inside its own folder
        out, k = re.subn(r"\bL00\b", "L01", out)
        stats["agentic L00"] += k
    if track2:  # bare lesson number inside the second-track folders
        old = track2[:3]
        out, k = re.subn(rf"\b{old}\b", TRACK2_DIRS[track2][:3], out)
        stats["track2 in-folder"] += k
    return out


def text_files():
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        if not p.is_file() or p.suffix not in TEXT_SUFFIXES or p.name in EXCLUDE:
            continue
        if set(Path(rel).parts) & EXCLUDE_DIRS:
            continue
        yield p, rel


def renames():
    """(old, new) path pairs, deepest first so parents are renamed last."""
    pairs = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT).as_posix()
        if set(Path(rel).parts) & EXCLUDE_DIRS:
            continue
        name = p.name
        new = None
        if p.is_dir() and p.parent == ROOT and name in TOP:
            new = TOP[name]
        elif p.is_dir() and name in AGENTIC_DIRS and p.parent.name == "4-Phase5_Agentic_AI":
            new = AGENTIC_DIRS[name]
        elif p.is_dir() and name in TRACK2_DIRS:
            new = TRACK2_DIRS[name]
        elif p.is_file() and p.parent.name in AGENTIC_DIRS and re.fullmatch(r"CHEATSHEET_L\d\d\.py", name):
            new = f"CHEATSHEET_L{AGENTIC[name[12:14]]}.py"
        elif p.is_file() and p.parent.name == "L20_Evaluation_Metrics" and name == "CHEATSHEET_L20.py":
            new = "CHEATSHEET_L24.py"
        elif p.is_file() and p.parent.name == "6-Vibe coding" and p.stem in VIBE_FILES:
            new = VIBE_FILES[p.stem] + p.suffix
        if new:
            pairs.append((p, p.with_name(new)))
    return sorted(pairs, key=lambda t: len(t[0].parts), reverse=True)


def main(apply: bool) -> None:
    stats, changed = Counter(), 0
    for p, rel in text_files():
        old = p.read_text()
        new = rewrite(old, rel, stats)
        if new != old:
            changed += 1
            if apply:
                p.write_text(new)
    rn = renames()
    for a, b in rn:
        if apply:
            a.rename(b)
    print(f"text files changed: {changed}")
    for k, v in stats.most_common():
        print(f"  {k}: {v}")
    print(f"paths renamed: {len(rn)}")
    if not apply:
        for a, b in rn:
            print(f"  {a.relative_to(ROOT)}  ->  {b.name}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
