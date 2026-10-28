# Lesson 09 Templates: Error Reading

Reference files for reading, diagnosing, and fixing Python errors in AI projects.

## Learning Materials
1. **PASS1_RECOGNITION.md** - 8 real error scenarios with fixes (START HERE)
2. **PASS_C_VISUAL.md** - Visual diagrams: traceback anatomy, decision tree, debug flow
3. **PASS3_TEMPLATES.md** - Overview of all reference files

## Reference Files
4. **error_decoder.md** - Full per-error diagnosis (KEEP OPEN when debugging!)
5. **CHEATSHEET_errors.py** - All 10 errors: wrong code vs right code (runnable!)
6. **CHEATSHEET_L09.py** - Debug print toolkit + safe patterns + ask-Claude template

## Quick Selection

| I need to... | File |
|:-------------|:-----|
| Look up what an error means | error_decoder.md |
| See bad code vs good code | CHEATSHEET_errors.py |
| Get debug print snippets | CHEATSHEET_L09.py |
| See how to read a traceback | PASS_C_VISUAL.md |

## Learning Path

**Step 1:** Read `PASS1_RECOGNITION.md` (30 min) — 8 error examples
**Step 2:** Study `PASS_C_VISUAL.md` (15 min) — 9 diagrams
**Step 3:** Run `CHEATSHEET_errors.py` — see all 10 errors in action
**Step 4:** Bookmark `error_decoder.md` — open it every time you get an error

## The 3-Second Error Process
1. **Last line** → error type + message
2. **Your file** → which line in YOUR code
3. **Fix table** → apply the standard fix

## The 10 Errors (in order of frequency in AI projects)
1. `KeyError` — wrong dict key name
2. `IndexError` — empty list accessed
3. `AttributeError` — wrong object type
4. `ModuleNotFoundError` — pip install missing
5. `TypeError` — wrong data type
6. `NameError` — typo or wrong order
7. `ValueError` — bad model name or value
8. `IndentationError` — missing 4 spaces
9. `JSONDecodeError` — LLM returned plain text
10. `FileNotFoundError` — wrong file path
