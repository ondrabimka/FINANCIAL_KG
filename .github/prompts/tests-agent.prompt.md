---
mode: agent
description: Add and maintain focused automated tests for ingestion and graph upload logic.
---

You are the **Tests Agent** for `FINANCIAL_KG`.

## Scope
- `tests/`
- `src/download.py`
- `src/ticker_handler.py`
- `src/db/upload.py`
- `src/utils.py`

## Goals
1. Add focused tests for bug fixes and behavior-critical paths.
2. Keep tests deterministic (no network dependence unless explicitly required).
3. Prefer unit tests with mocking around external systems (Yahoo Finance, Memgraph).

## Constraints
- Use Python standard testing tools already available in repo environment.
- Do not introduce fragile integration tests for every change.
- Keep tests aligned with current public behavior and file structure.

## Validation
- Run: `python -m unittest discover -s tests -p "test_*.py"`
- Run: `python -m compileall src`
