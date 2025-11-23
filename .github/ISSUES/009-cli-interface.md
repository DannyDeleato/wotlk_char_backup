# Issue #009: Command Line Interface

## Description
Create a user-friendly CLI for the WotLK character backup tool.

## Tasks
- [ ] Implement main CLI using Click or Typer
- [ ] Add `export` command:
  ```
  wotlk-backup export <profile-url> [options]
  wotlk-backup export "https://db.rising-gods.de/?profile=eu.rising-gods.lopht"
  ```
- [ ] Add command options:
  - `--output`, `-o`: Output file path
  - `--format`, `-f`: Output format (json, etc.)
  - `--include`: What to include (gear, achievements, mounts, pets, all)
  - `--exclude`: What to exclude
  - `--compress`: Enable compression
  - `--verbose`, `-v`: Verbose output
  - `--quiet`, `-q`: Quiet mode
- [ ] Add `config` command for managing settings:
  ```
  wotlk-backup config set delay 2
  wotlk-backup config list
  ```
- [ ] Add `list-servers` command to show known AoWoW installations
- [ ] Implement progress indicators for long operations
- [ ] Add colored output for better readability
- [ ] Support batch export from file (list of profile URLs)

## Example Usage
```bash
# Basic export
wotlk-backup export "https://db.rising-gods.de/?profile=eu.rising-gods.lopht"

# Export only gear to specific file
wotlk-backup export "..." --include gear --output my-char-gear.json

# Batch export
wotlk-backup export --batch characters.txt --output exports/
```

## Acceptance Criteria
- CLI is intuitive and follows common conventions
- Help text is comprehensive
- Error messages are user-friendly
- Progress is shown for long operations

## Labels
`cli`, `ux`

## Priority
Medium

## Dependencies
- #003-#007 Scrapers
- #008 JSON Exporter
