# Issue #001: Project Setup and Structure

## Description
Set up the initial project structure, dependencies, and configuration for the WotLK Character Backup exporter.

## Tasks
- [ ] Initialize project (Python recommended for web scraping)
- [ ] Set up `pyproject.toml` or `requirements.txt` with dependencies:
  - `requests` or `httpx` for HTTP requests
  - `beautifulsoup4` for HTML parsing
  - `lxml` for fast HTML/XML parsing
  - `pydantic` for data models and validation
  - `click` or `typer` for CLI
- [ ] Create basic project structure:
  ```
  wotlk_char_backup/
  ├── src/
  │   ├── __init__.py
  │   ├── cli.py
  │   ├── scraper/
  │   ├── models/
  │   ├── exporters/
  │   └── config.py
  ├── tests/
  ├── pyproject.toml
  └── README.md
  ```
- [ ] Set up basic logging
- [ ] Create README with project overview

## Acceptance Criteria
- Project can be installed with `pip install -e .`
- Basic CLI command works (`wotlk-backup --help`)
- All dependencies are pinned to specific versions

## Labels
`setup`, `infrastructure`

## Priority
High - Foundation for all other work
