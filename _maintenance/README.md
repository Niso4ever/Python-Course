# Maintenance scripts

One-off scripts used to update the course on 2026-10-28. Kept so the changes can be checked or repeated.

- `sweep_models.py`: replaced retired Claude model IDs. Dry run by default; `--apply` writes.
- `fix_prices.py`: updated model-keyed price tables and model names in prose.
- `renumber.py`: renamed folders so folder number = phase number and renumbered lessons. Already applied; it is not safe to run twice.

`sweep_models.py` and `fix_prices.py` were run before `renumber.py`, so the paths inside them use the old folder names (for example `4-Phase5_Agentic_AI`). Translate with the mapping in `CLAUDE.md` before reusing them.
