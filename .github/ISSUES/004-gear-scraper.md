# Issue #004: Gear Scraping with Gems and Enchantments

## Description
Extend the scraper to extract complete gear information including equipped items, gems, and enchantments.

## Background
AoWoW displays gear in a paper-doll format with:
- Item tooltips containing detailed info
- Gem sockets shown within items
- Enchantments displayed on items
- Item links often contain encoded data (item:id:enchant:gem1:gem2:gem3:...)

## Tasks
- [ ] Parse gear slots from profile page
- [ ] Extract item information for each slot:
  - Item ID
  - Item name
  - Item level
  - Item quality/rarity
- [ ] Parse gem information:
  - Socket colors and bonuses
  - Socketed gems with IDs and stats
- [ ] Parse enchantment information:
  - Enchant ID
  - Enchant name/effect
- [ ] Handle item links format (Wowhead-style: `item=12345&ench=3000&gems=123:456:789`)
- [ ] Handle empty slots gracefully
- [ ] Parse random enchantment suffixes (e.g., "of the Whale")

## Technical Notes
- Item data might be in JavaScript tooltips
- May need to parse `$WowheadPower.registerItem()` calls
- Consider looking for `rel="item=..."` attributes in links

## Acceptance Criteria
- All 19 gear slots can be parsed
- Gems are correctly associated with items
- Enchantments are correctly extracted
- Works with empty slots and unenchanted/ungemmed items

## Labels
`scraper`, `gear`

## Priority
High

## Dependencies
- #003 Basic Profile Scraper
