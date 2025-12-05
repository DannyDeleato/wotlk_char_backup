"""Tests for scraper functionality."""

import pytest
from wotlk_char_backup.scraper.aowow import AoWoWScraper, AoWowScraperError
from wotlk_char_backup.config import ScrapingConfig


def test_scraper_initialization():
    """Test scraper can be initialized."""
    scraper = AoWoWScraper()
    assert scraper is not None
    scraper.close()


def test_scraper_context_manager():
    """Test scraper works as context manager."""
    with AoWoWScraper() as scraper:
        assert scraper is not None


def test_parse_profile_url():
    """Test profile URL parsing."""
    scraper = AoWoWScraper()
    url = "https://db.rising-gods.de/?profile=eu.rising-gods.lopht"

    base_url, region, realm, char = scraper._parse_profile_url(url)

    assert base_url == "https://db.rising-gods.de"
    assert region == "eu"
    assert realm == "rising-gods"
    assert char == "lopht"

    scraper.close()


def test_parse_profile_url_invalid():
    """Test profile URL parsing with invalid URL."""
    scraper = AoWoWScraper()

    with pytest.raises(ValueError):
        scraper._parse_profile_url("https://example.com")

    with pytest.raises(ValueError):
        scraper._parse_profile_url("https://example.com/?profile=invalid")

    scraper.close()


def test_race_id_to_name():
    """Test race ID conversion."""
    scraper = AoWoWScraper()

    assert scraper._race_id_to_name(1) == "Human"
    assert scraper._race_id_to_name(2) == "Orc"
    assert scraper._race_id_to_name(10) == "Blood Elf"
    assert scraper._race_id_to_name(11) == "Draenei"
    assert scraper._race_id_to_name(999) == "Unknown(999)"

    scraper.close()


def test_class_id_to_name():
    """Test class ID conversion."""
    scraper = AoWoWScraper()

    assert scraper._class_id_to_name(1) == "Warrior"
    assert scraper._class_id_to_name(2) == "Paladin"
    assert scraper._class_id_to_name(6) == "Death Knight"
    assert scraper._class_id_to_name(11) == "Druid"
    assert scraper._class_id_to_name(999) == "Unknown(999)"

    scraper.close()


def test_parse_item_link():
    """Test item link parsing."""
    scraper = AoWoWScraper()

    # Basic item
    result = scraper._parse_item_link("item=12345")
    assert result["item_id"] == 12345
    assert "enchant_id" not in result
    assert "gem_ids" not in result

    # Item with enchant
    result = scraper._parse_item_link("item=12345&ench=3000")
    assert result["item_id"] == 12345
    assert result["enchant_id"] == 3000

    # Item with gems
    result = scraper._parse_item_link("item=12345&gems=123:456:789")
    assert result["item_id"] == 12345
    assert result["gem_ids"] == [123, 456, 789]

    # Item with gems and enchant
    result = scraper._parse_item_link("item=12345&ench=3000&gems=123:456:0")
    assert result["item_id"] == 12345
    assert result["enchant_id"] == 3000
    assert result["gem_ids"] == [123, 456]  # 0 is filtered out

    scraper.close()


def test_quality_id_to_name():
    """Test item quality ID conversion."""
    scraper = AoWoWScraper()

    assert scraper._quality_id_to_name(0) == "Poor"
    assert scraper._quality_id_to_name(1) == "Common"
    assert scraper._quality_id_to_name(2) == "Uncommon"
    assert scraper._quality_id_to_name(3) == "Rare"
    assert scraper._quality_id_to_name(4) == "Epic"
    assert scraper._quality_id_to_name(5) == "Legendary"
    assert scraper._quality_id_to_name(7) == "Heirloom"

    scraper.close()


def test_slot_id_to_name():
    """Test equipment slot ID conversion."""
    scraper = AoWoWScraper()

    assert scraper._slot_id_to_name(1) == "head"
    assert scraper._slot_id_to_name(2) == "neck"
    assert scraper._slot_id_to_name(5) == "chest"
    assert scraper._slot_id_to_name(16) == "main_hand"
    assert scraper._slot_id_to_name(17) == "off_hand"

    scraper.close()
