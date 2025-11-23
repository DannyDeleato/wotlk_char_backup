# Issue #008: JSON Export Format

## Description
Implement JSON export functionality for scraped character data.

## Tasks
- [ ] Create `JSONExporter` class
- [ ] Implement full character export to JSON:
  - Properly formatted/indented output
  - All data models serialized
  - Datetime fields as ISO 8601 strings
- [ ] Add metadata to export:
  - Export timestamp
  - Source URL
  - Exporter version
  - AoWoW installation info
- [ ] Support partial exports (e.g., gear only, achievements only)
- [ ] Implement JSON schema generation for validation
- [ ] Add compression option (gzip)

## Export Structure
```json
{
  "metadata": {
    "export_version": "1.0.0",
    "export_date": "2024-01-15T10:30:00Z",
    "source_url": "https://db.rising-gods.de/?profile=eu.rising-gods.lopht",
    "aowow_installation": "rising-gods"
  },
  "character": { ... },
  "gear": { ... },
  "achievements": [ ... ],
  "mounts": [ ... ],
  "pets": [ ... ]
}
```

## Acceptance Criteria
- JSON output is valid and well-formatted
- Can be re-imported and parsed by the same models
- File size is reasonable (compressed option available)

## Labels
`exporter`, `output`

## Priority
Medium

## Dependencies
- #002 Data Models
