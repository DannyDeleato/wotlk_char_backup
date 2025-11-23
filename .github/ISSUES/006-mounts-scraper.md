# Issue #006: Mounts Collection Scraping

## Description
Implement scraping of character mount collections from AoWoW profiles.

## Background
WotLK has ~170+ mounts available. AoWoW typically shows:
- Total mounts collected
- List of known mounts
- Mount icons and names
- Sometimes mount sources

## Tasks
- [ ] Identify mounts data location (tab, AJAX, embedded)
- [ ] Parse mount collection summary (X/Y mounts)
- [ ] Extract individual mount data:
  - Mount/Spell ID
  - Mount name
  - Icon URL
  - Mount type (ground/flying)
  - Source (if available)
- [ ] Handle faction-specific mounts display
- [ ] Support paginated mount lists if applicable

## Technical Notes
- Mounts tab might be: `?profile={char}&tab=mounts`
- Data might reference spell IDs (mount summoning spells)
- Consider mapping to Wowhead data for additional info

## Acceptance Criteria
- All known mounts are extracted
- Mount count matches displayed total
- Spell IDs are correctly captured for each mount

## Labels
`scraper`, `mounts`

## Priority
Medium

## Dependencies
- #003 Basic Profile Scraper
