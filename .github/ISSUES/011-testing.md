# Issue #011: Testing Infrastructure

## Description
Set up comprehensive testing for the project including unit tests, integration tests, and test fixtures.

## Tasks
- [ ] Set up pytest with coverage reporting
- [ ] Create test fixtures:
  - Sample HTML pages from AoWoW (anonymized)
  - Expected parsed output for each fixture
  - Mock responses for HTTP requests
- [ ] Write unit tests for:
  - Data models (validation, serialization)
  - HTML parsing functions
  - Export formatters
- [ ] Write integration tests for:
  - Full profile scraping (using fixtures)
  - CLI commands
- [ ] Set up CI/CD with GitHub Actions:
  - Run tests on push/PR
  - Check code coverage
  - Lint with ruff/flake8
  - Type check with mypy
- [ ] Add test documentation

## Test Coverage Targets
- Models: 100%
- Parsers: 90%+
- Exporters: 90%+
- CLI: 80%+

## Acceptance Criteria
- All tests pass
- Coverage report is generated
- CI runs automatically on changes
- Tests don't hit live servers (use mocks/fixtures)

## Labels
`testing`, `infrastructure`

## Priority
Medium

## Dependencies
- #001 Project Setup
- #002 Data Models
