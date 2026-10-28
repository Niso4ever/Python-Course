# Lesson 16 Templates: Import Pattern Deep Dive

Environment management, version control, and package diagnosis for AI projects.

## Learning Materials
1. **PASS1_RECOGNITION.md** - 8 scenarios: requirements.txt, venv, version pinning, sys.path
2. **PASS_C_VISUAL.md** - 8 diagrams: sandbox model, import search, lifecycle, .gitignore
3. **CHEATSHEET_L10.py** - All venv + pip commands, version checker, path inspector (runnable!)

## Learning Path
**Step 1:** Read PASS1 (20 min) — recognize environment patterns
**Step 2:** Study PASS_C (10 min) — see the sandbox mental model
**Step 3:** Run CHEATSHEET_L10.py — inspect your actual Python environment

## The Key Rule
```
Always create a .venv per project.
Always pip freeze > requirements.txt before sharing code.
AttributeError on a library method → check pip show <package> version first.
```
