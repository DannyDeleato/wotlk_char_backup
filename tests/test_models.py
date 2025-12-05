"""Tests for data models."""

from datetime import datetime
import pytest
from wotlk_char_backup.models import (
    Character,
    Item,
    Gem,
    Enchantment,
    EquippedItem,
    GearSet,
    Achievement,
    Mount,
    Pet,
    CharacterExport,
)


def test_character_model():
    """Test Character model creation and validation."""
    char = Character(
        name="TestChar",
        realm="test-realm",
        region="eu",
        level=80,
        race="Human",
        **{"class": "Paladin"},
        faction="Alliance",
    )
    assert char.name == "TestChar"
    assert char.level == 80
    assert char.race == "Human"


def test_character_level_validation():
    """Test that character level is validated."""
    with pytest.raises(Exception):  # Pydantic validation error
        Character(
            name="TestChar",
            realm="test-realm",
            region="eu",
            level=100,  # Invalid for WotLK
            race="Human",
            **{"class": "Paladin"},
            faction="Alliance",
        )


def test_item_model():
    """Test Item model."""
    item = Item(
        item_id=12345,
        name="Test Sword",
        slot="main_hand",
        quality="Epic",
        item_level=200,
    )
    assert item.item_id == 12345
    assert item.quality == "Epic"


def test_gem_model():
    """Test Gem model."""
    gem = Gem(
        gem_id=40111,
        name="Bold Scarlet Ruby",
        color="Red",
        stats="+16 Strength",
    )
    assert gem.gem_id == 40111
    assert gem.color == "Red"


def test_enchantment_model():
    """Test Enchantment model."""
    ench = Enchantment(
        enchant_id=3789,
        name="Berserking",
        stats="+400 Attack Power proc",
    )
    assert ench.enchant_id == 3789


def test_equipped_item():
    """Test EquippedItem with gems and enchantment."""
    item = Item(
        item_id=40343,
        name="Armageddon",
        slot="main_hand",
        quality="Legendary",
        item_level=239,
    )
    gem = Gem(gem_id=41398, name="Test Gem", color="Meta", stats="+21 Agility")
    ench = Enchantment(enchant_id=3789, name="Berserking", stats="+400 AP")

    equipped = EquippedItem(item=item, gems=[gem], enchantment=ench)
    assert equipped.item.item_id == 40343
    assert len(equipped.gems) == 1
    assert equipped.enchantment.enchant_id == 3789


def test_gear_set():
    """Test GearSet model."""
    gear = GearSet()
    assert gear.equipped_slots() == 0

    item = Item(
        item_id=12345, name="Test", slot="head", quality="Epic", item_level=200
    )
    equipped = EquippedItem(item=item, gems=[], enchantment=None)

    gear = GearSet(head=equipped, chest=equipped, legs=equipped)
    assert gear.equipped_slots() == 3


def test_achievement_model():
    """Test Achievement model."""
    ach = Achievement(
        achievement_id=2186,
        name="The Immortal",
        description="Complete Naxxramas without deaths",
        points=10,
        category="Raids",
    )
    assert ach.achievement_id == 2186
    assert ach.points == 10


def test_mount_model():
    """Test Mount model."""
    mount = Mount(
        mount_id=48954,
        name="Swift Zhevra",
        spell_id=49322,
    )
    assert mount.mount_id == 48954
    assert mount.spell_id == 49322


def test_pet_model():
    """Test Pet model."""
    pet = Pet(
        pet_id=32498,
        name="Mr. Wiggles",
        spell_id=10715,
    )
    assert pet.pet_id == 32498
    assert pet.name == "Mr. Wiggles"


def test_character_export():
    """Test CharacterExport model."""
    char = Character(
        name="TestChar",
        realm="test-realm",
        region="eu",
        level=80,
        race="Human",
        **{"class": "Paladin"},
        faction="Alliance",
    )
    gear = GearSet()
    export = CharacterExport(
        character=char,
        gear=gear,
        achievements=[],
        mounts=[],
        pets=[],
        source_url="https://example.com",
    )
    assert export.character.name == "TestChar"
    assert isinstance(export.export_date, datetime)


def test_character_export_serialization():
    """Test that CharacterExport can be serialized to JSON."""
    char = Character(
        name="TestChar",
        realm="test-realm",
        region="eu",
        level=80,
        race="Human",
        **{"class": "Paladin"},
        faction="Alliance",
    )
    gear = GearSet()
    export = CharacterExport(
        character=char,
        gear=gear,
        achievements=[],
        mounts=[],
        pets=[],
        source_url="https://example.com",
    )

    # Test JSON serialization
    data = export.model_dump(mode="json")
    assert data["character"]["name"] == "TestChar"
    assert data["character"]["level"] == 80
