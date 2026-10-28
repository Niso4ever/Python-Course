# Pass 3: Templates Overview — Error Reading
## Your Lesson 09 Reference Library

All templates are in this lesson folder (`Phase1(B)/L09_Error_Reading/`).
**Your workflow:** Error appears → identify type → open matching reference → apply fix.

---

## Template Files at a Glance

| File | Format | Use it when |
|:-----|:-------|:------------|
| `error_decoder.md` | Markdown reference | Quick lookup: "what does this error mean?" |
| `CHEATSHEET_errors.py` | Python file (runnable) | Side-by-side bad vs good code for all 10 errors |
| `CHEATSHEET_L09.py` | Python file | Debug patterns and "what to ask Claude" template |

---

## File 1: error_decoder.md

**Format:** Markdown table + fix instructions
**Use when:** You see an error and want the fastest lookup

Contains:
- 10-error quick table (error → cause → fix in one line each)
- Full diagnosis for each error type
- pip name mapping for ImportError
- "What to print for debugging" guide

---

## File 2: CHEATSHEET_errors.py

**Format:** Runnable Python — shows bad code and good code side by side
**Use when:** You want to see exactly what the broken vs fixed code looks like

Contains:
- 10 complete error scenarios
- Each shows: what triggers it, what the error says, how to fix it
- Runnable demo at the bottom — shows good patterns working

---

## File 3: CHEATSHEET_L09.py

**Format:** Python reference file
**Use when:** General error-reading workflow

Contains:
- The 3-step process (Read → Locate → Fix)
- Debug print patterns
- type() and keys() diagnostic snippets
- The "ask Claude" template

---

## The 3-Step Fix — Quick Card

```
STEP 1: READ (5 seconds)
  Last line of traceback = error type + message
  KeyError? AttributeError? ImportError?

STEP 2: LOCATE (10 seconds)
  Find YOUR file in the traceback (not /site-packages/)
  Note the line number
  Look at that line in your code

STEP 3: FIX (15 seconds)
  Look up error type in error_decoder.md
  Apply the standard fix pattern
```

---

## Error Type → Fix Path

| If you see | Go to |
|:-----------|:------|
| `KeyError` | Print the dict → find real key name |
| `IndexError` | Add `if docs:` before `docs[0]` |
| `AttributeError` | Add `print(type(obj))` before the failing line |
| `ModuleNotFoundError` | Run `pip install <name>` (check L6 name table) |
| `TypeError` | Add `print(type(variable))` before the call |
| `NameError` | Check for typo; check variable was assigned |
| `ValueError` | Check model name, check value range |
| `IndentationError` | Add 4 spaces; check copy-paste |
| `JSONDecodeError` | Print the string before `json.loads()` |
| `FileNotFoundError` | Print `os.getcwd()`; check the path |

---

## The "Ask Claude" Template

Copy this every time you share an error:

```
Error I got:
[paste the full traceback here — all lines]

My code that caused it:
[paste the relevant function/class — 5-20 lines]

What I was trying to do:
[one sentence description]
```

**Never share just the last line.** Claude needs the traceback + code + intent.
