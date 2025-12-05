# WotLK Character Backup

Export World of Warcraft: Wrath of the Lich King character data from AoWoW installations (armory/database sites used by private servers).

## Features

- 📊 **Character Info**: Name, race, class, level, guild, faction
- ⚔️ **Gear**: All equipped items with gems and enchantments
- 🏆 **Achievements**: Completed achievements with dates and points
- 🐴 **Mounts**: Complete mount collection
- 🐾 **Pets**: Companion pet collection
- 💾 **Export**: JSON format with optional compression

## Installation

```bash
# Clone the repository
git clone https://github.com/DannyDeleato/wotlk_char_backup.git
cd wotlk_char_backup

# Install with pip (editable mode for development)
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```bash
# Export a character from Rising Gods
wotlk-backup export "https://db.rising-gods.de/?profile=eu.rising-gods.lopht"

# Export to a specific file
wotlk-backup export "https://db.rising-gods.de/?profile=eu.rising-gods.lopht" --output my-char.json

# Export only specific data
wotlk-backup export "URL" --include gear achievements

# Show help
wotlk-backup --help
```

## Supported AoWoW Installations

- Rising Gods (`db.rising-gods.de`)
- Other AoWoW-based armories (configurable)

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy src/
```

## Project Status

🚧 **In Development** - Core features are being actively developed.

See [.github/ISSUES/000-roadmap.md](.github/ISSUES/000-roadmap.md) for the complete roadmap and task breakdown.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.
