# Issue #003: AoWoW Profile Page Scraper - Basic Character Info

## Description
Implement the core scraper to fetch and parse basic character information from AoWoW profile pages.

## Background
AoWoW profile URLs follow the pattern:
- `https://{domain}/?profile={region}.{realm}.{character}`
- Example: `https://db.rising-gods.de/?profile=eu.rising-gods.lopht`

AoWoW typically loads character data through:
1. Initial HTML page with basic info
2. JavaScript/AJAX calls for detailed data (gear, achievements, etc.)
3. Data often embedded in `<script>` tags as JavaScript variables

## Tasks
- [ ] Create `AoWoWScraper` class with configurable base URL
- [ ] Implement profile page fetching with proper headers/user-agent
- [ ] Handle common HTTP errors (404, 403, rate limiting)
- [ ] Parse basic character info from HTML:
  - Character name
  - Level
  - Race
  - Class
  - Guild
  - Realm/Server
- [ ] Extract character portrait/avatar URL
- [ ] Implement retry logic with exponential backoff
- [ ] Add request caching to avoid hitting servers repeatedly during development

## Technical Notes
- AoWoW may have bot protection - may need to handle cookies/sessions
- Consider using `requests-html` if JavaScript rendering is needed
- Profile data might be in `g_profiles` JavaScript variable

## Acceptance Criteria
- Can fetch a profile page and extract basic character info
- Handles errors gracefully with meaningful messages
- Respects rate limiting (add configurable delay between requests)

## Labels
`scraper`, `core`

## Priority
High

## Dependencies
- #001 Project Setup
- #002 Data Models
