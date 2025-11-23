# Issue #010: Configuration System

## Description
Implement a configuration system to support multiple AoWoW installations and user preferences.

## Tasks
- [ ] Create configuration file structure (YAML or TOML)
- [ ] Implement config loading from:
  - Default locations (`~/.config/wotlk-backup/config.yaml`)
  - Project directory (`.wotlk-backup.yaml`)
  - Environment variables
  - CLI arguments (highest priority)
- [ ] Define configurable settings:
  - Known AoWoW servers with their URLs
  - Default output format
  - Default output directory
  - Request delay/rate limiting
  - User-agent string
  - Proxy settings
  - Logging level
- [ ] Pre-configure known servers:
  - Rising Gods (db.rising-gods.de)
  - Other popular WotLK private servers
- [ ] Add config validation
- [ ] Support config profiles for different servers

## Example Config
```yaml
# ~/.config/wotlk-backup/config.yaml
defaults:
  output_format: json
  output_dir: ~/wow-backups
  compress: false

servers:
  rising-gods:
    url: https://db.rising-gods.de
    realm: rising-gods
    region: eu
  warmane:
    url: https://armory.warmane.com
    # Different parser might be needed

scraping:
  delay: 1.0  # seconds between requests
  timeout: 30
  retries: 3
  user_agent: "WotLK-Backup/1.0"
```

## Acceptance Criteria
- Config file is auto-created with defaults on first run
- CLI args override config file settings
- Unknown servers can be used with manual URL entry

## Labels
`config`, `infrastructure`

## Priority
Low

## Dependencies
- #001 Project Setup
