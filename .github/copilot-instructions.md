# GitHub Copilot instructions for FINANCIAL_KG

## Project context
- This repository builds a financial knowledge graph from Yahoo Finance data and uploads it to Memgraph.
- Main ingestion flow:
  - `src/main.py` orchestrates download + upload.
  - `src/download.py` downloads and stores CSV snapshots under `data/data_YYYY-MM-DD/`.
  - `src/db/upload.py` uploads CSV data into Memgraph graph entities/relationships.
  - `src/db/models.py` defines graph schema (nodes and relationships).

## Preferred way to run
- Local stack: `docker-compose up -d`
- MCP endpoint: `http://localhost:8000/mcp/`
- Python entrypoint in container: `src/main.py` (triggered by `src/entrypoint.sh` / cron in `src/Dockerfile`)

## Code change rules
- Keep changes focused and minimal; avoid unrelated refactors.
- Preserve existing CSV column names and graph property names unless explicitly changing schema.
- When changing extraction (`ticker_handler.py`) also verify upload mapping (`src/db/upload.py`) remains consistent.
- Use explicit error logging; do not silently swallow failures.

## Validation commands
- Syntax check: `python -m compileall src`
- Style/hooks: `pre-commit run --files <changed-files>`
