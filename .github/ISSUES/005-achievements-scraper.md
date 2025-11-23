# Issue #005: Achievements Scraping

## Description
Implement scraping of character achievements from AoWoW profiles.

## Background
AoWoW typically shows achievements in:
- A summary section with total points
- Categorized lists (General, Quests, Exploration, PvP, Dungeons & Raids, etc.)
- Each achievement shows: name, description, points, completion date

Achievements may be loaded via AJAX or available in the page source.

## Tasks
- [ ] Identify how achievements are loaded (AJAX endpoint or embedded data)
- [ ] Parse achievement summary (total points, completion percentage)
- [ ] Extract individual achievements:
  - Achievement ID
  - Name
  - Description
  - Points value
  - Category/subcategory
  - Completion timestamp
  - Icon URL
- [ ] Handle achievement criteria progress (if shown)
- [ ] Support paginated achievement lists if applicable
- [ ] Parse Feats of Strength separately

## Technical Notes
- Achievements endpoint might be: `?profile={char}&tab=achievements`
- Data might be in `g_achievements` JavaScript variable
- Consider storing only completed achievements vs all progress

## Acceptance Criteria
- All completed achievements are extracted
- Achievement categories are preserved
- Completion dates are parsed correctly
- Total points match the displayed total

## Labels
`scraper`, `achievements`

## Priority
Medium

## Dependencies
- #003 Basic Profile Scraper
