# Issue #007: Companion Pets Collection Scraping

## Description
Implement scraping of character companion pet (non-combat pet) collections from AoWoW profiles.

## Background
WotLK has 100+ companion pets. AoWoW typically shows:
- Total pets collected
- List of known companion pets
- Pet icons and names

Note: This is for non-combat/vanity pets, not hunter pets.

## Tasks
- [ ] Identify pets data location (tab, AJAX, embedded)
- [ ] Parse pet collection summary (X/Y pets)
- [ ] Extract individual pet data:
  - Pet/Spell ID
  - Pet name
  - Icon URL
  - Source (if available)
- [ ] Handle faction-specific pets display
- [ ] Support paginated pet lists if applicable

## Technical Notes
- Pets tab might be: `?profile={char}&tab=companions`
- Data might reference spell IDs (pet summoning spells)
- Some pets are from achievements, others from drops/vendors

## Acceptance Criteria
- All known companion pets are extracted
- Pet count matches displayed total
- Spell IDs are correctly captured for each pet

## Labels
`scraper`, `pets`

## Priority
Medium

## Dependencies
- #003 Basic Profile Scraper
