# Lab 5: Static Code Analysis - Issues Found and Fixed

File analysed: `recruitment_tracker.py` (Applicant Tracking System)

## Results summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.47/10 | 10.00/10 |
| Bandit | 3 issues (2 Medium, 1 Low) | 0 issues |
| Flake8 | 8 issues | 0 issues |

## Issue table

Line numbers refer to the original file (before the fixes).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608, Medium) | Security | 8 | `addApplicant` builds the INSERT using an f-string, so input such as `x'); DROP TABLE applicants;--` could change the query | Use a parameterised query with `?` placeholders and pass the values as a tuple |
| Use of `eval` (Bandit B307 Medium, Pylint W0123) | Security | 14 | `shortlist` runs `eval(salary_rule)` on a string, which allows arbitrary code execution | Removed `eval`; `shortlist` now takes a numeric `salary_limit` and `main` passes `500000 + 150000` |
| Silent broad exception (Bandit B110 Low, Pylint W0718) | Bug | 26-29 | `except Exception: pass` hides every failure, so a failed update looks successful | Catch only `sqlite3.Error`, log it, roll back and return `False` (return `True` on success) |
| Inconsistent return (Pylint R1710) | Bug | 12-22 | `shortlist` returns a list when there are matches but implicitly returns `None` otherwise | Always return a list (empty if nobody matches) using a list comprehension |
| Unused variable (Pylint W0612, Flake8 F841) | Code quality | 15 | `total_seen` is assigned but never used | Deleted the variable |
| File not closed safely (Pylint R1732, W1514) | Bug | 32-35 | File opened without `with` (stays open if a write fails) and without an encoding | Used `with open(..., encoding="utf-8", newline="")` and the `csv` module |
| Naming convention (Pylint C0103) | Style | 7, 24, 31, 38 | `addApplicant`, `updateStatus`, `exportReport` and `countByStatus` are camelCase, not snake_case | Renamed to `add_applicant`, `update_status`, `export_report`, `count_by_status` and updated every call |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 7, 12, 24, 31, 38, 42 | The module and every function have no docstring | Added a module docstring and a docstring for each function |
| Code runs on import | Design | 54 | `main()` is called at module level, so importing the file runs the demo and writes a CSV | Wrapped the call in `if __name__ == "__main__":` |
| Line too long (Flake8 E501, Pylint C0301) | Style | 4, 8, 13, 26, 39 | Lines up to 140 characters, over the 79-character limit | Wrapped long SQL strings and function arguments across lines |
| Trailing whitespace (Flake8 W291, Pylint C0303) | Style | 15 | Spaces at the end of the `total_seen = len(rows)` line | Removed (the line was deleted with the unused variable) |
| Missing blank line (Flake8 E302) | Style | 31 | Only one blank line before `exportReport` | Two blank lines between top-level functions |

## Commits

1. Bandit fixes: SQL injection, `eval`, silent exception
2. Pylint fixes: inconsistent return, unused variable, file handling, naming, docstrings, `__main__` guard
3. Flake8 fixes: line length, trailing whitespace, blank lines

## Verification

All three tools were re-run after the fixes. The final reports are in `after/` and the original reports are in `before/`. The program output is unchanged (`['Nina']` and `2 in interview`).
