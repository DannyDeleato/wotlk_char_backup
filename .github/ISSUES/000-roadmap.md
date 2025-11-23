# WotLK Character Backup - Project Roadmap

## Overview
A tool to export World of Warcraft: Wrath of the Lich King character data from AoWoW installations (armory/database sites used by private servers).

## Features
Export the following character data:
- **Basic Info**: Name, Race, Class, Level, Guild, Faction
- **Gear**: All equipped items with gems and enchantments
- **Achievements**: Completed achievements with dates and points
- **Mounts**: Collected mount collection
- **Pets**: Companion pet collection

## Supported AoWoW Installations
- Rising Gods (`db.rising-gods.de`)
- Other AoWoW-based armories (configurable)

---

## Issue Index

### Phase 1: Foundation (High Priority)
| Issue | Title | Status | Dependencies |
|-------|-------|--------|--------------|
| #001 | [Project Setup](001-project-setup.md) | Pending | - |
| #002 | [Data Models](002-data-models.md) | Pending | #001 |
| #003 | [Basic Profile Scraper](003-aowow-profile-scraper.md) | Pending | #001, #002 |
| #004 | [Gear Scraper](004-gear-scraper.md) | Pending | #003 |

### Phase 2: Complete Data Extraction (Medium Priority)
| Issue | Title | Status | Dependencies |
|-------|-------|--------|--------------|
| #005 | [Achievements Scraper](005-achievements-scraper.md) | Pending | #003 |
| #006 | [Mounts Scraper](006-mounts-scraper.md) | Pending | #003 |
| #007 | [Pets Scraper](007-pets-scraper.md) | Pending | #003 |
| #008 | [JSON Exporter](008-json-exporter.md) | Pending | #002 |
| #009 | [CLI Interface](009-cli-interface.md) | Pending | #003-#008 |

### Phase 3: Polish (Low Priority)
| Issue | Title | Status | Dependencies |
|-------|-------|--------|--------------|
| #010 | [Configuration System](010-configuration-system.md) | Pending | #001 |
| #011 | [Testing Infrastructure](011-testing.md) | Pending | #001, #002 |
| #012 | [Documentation](012-documentation.md) | Pending | All |

---

## Suggested Implementation Order

1. **#001 Project Setup** - Initialize Python project structure
2. **#002 Data Models** - Define all Pydantic models
3. **#003 Basic Scraper** - Fetch profile pages, parse basic info
4. **#004 Gear Scraper** - Extract items, gems, enchantments
5. **#008 JSON Exporter** - Output to JSON format
6. **#009 CLI Interface** - Basic command-line tool
7. **#005 Achievements** - Add achievements support
8. **#006 Mounts** - Add mounts support
9. **#007 Pets** - Add pets support
10. **#010 Configuration** - Multi-server support
11. **#011 Testing** - Add tests and CI
12. **#012 Documentation** - Complete docs

---

## Tech Stack (Recommended)
- **Language**: Python 3.10+
- **HTTP Client**: httpx or requests
- **HTML Parsing**: BeautifulSoup4 + lxml
- **Data Models**: Pydantic v2
- **CLI**: Typer or Click
- **Testing**: pytest + pytest-cov
- **Output**: JSON (primary), potentially CSV

---

## Notes
- AoWoW installations may have slight variations in their HTML structure
- Some servers may have bot protection requiring special handling
- Rate limiting should be respected to avoid IP bans
