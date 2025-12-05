"""Gear and equipment models."""

from typing import Optional, List
from pydantic import BaseModel, Field


class Item(BaseModel):
    """Represents a WoW item."""

    item_id: int = Field(..., description="WoW item ID")
    name: str = Field(..., description="Item name")
    slot: str = Field(..., description="Equipment slot")
    quality: str = Field(
        ...,
        description="Item quality: Poor, Common, Uncommon, Rare, Epic, Legendary, Artifact, Heirloom",
    )
    item_level: int = Field(..., ge=1, description="Item level")
    icon_url: Optional[str] = Field(None, description="Item icon URL")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item_id": 40343,
                    "name": "Armageddon",
                    "slot": "main_hand",
                    "quality": "Legendary",
                    "item_level": 239,
                    "icon_url": "https://example.com/icon.jpg",
                }
            ]
        }
    }


class Gem(BaseModel):
    """Represents a gem socketed in an item."""

    gem_id: int = Field(..., description="Gem item ID")
    name: str = Field(..., description="Gem name")
    color: str = Field(
        ..., description="Socket color: Red, Blue, Yellow, Meta, Orange, Green, Purple, Prismatic"
    )
    stats: str = Field(..., description="Gem stats/bonuses")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "gem_id": 41398,
                    "name": "Relentless Earthsiege Diamond",
                    "color": "Meta",
                    "stats": "+21 Agility and 3% Critical Damage",
                }
            ]
        }
    }


class Enchantment(BaseModel):
    """Represents an enchantment on an item."""

    enchant_id: int = Field(..., description="Enchantment ID")
    name: str = Field(..., description="Enchantment name")
    stats: str = Field(..., description="Enchantment stats/bonuses")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "enchant_id": 3789,
                    "name": "Berserking",
                    "stats": "Increases attack power by 400 for 15 sec",
                }
            ]
        }
    }


class EquippedItem(BaseModel):
    """Represents a fully equipped item with gems and enchantments."""

    item: Item = Field(..., description="The base item")
    gems: List[Gem] = Field(default_factory=list, description="Socketed gems")
    enchantment: Optional[Enchantment] = Field(None, description="Applied enchantment")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item": {
                        "item_id": 40343,
                        "name": "Armageddon",
                        "slot": "main_hand",
                        "quality": "Legendary",
                        "item_level": 239,
                    },
                    "gems": [
                        {
                            "gem_id": 41398,
                            "name": "Relentless Earthsiege Diamond",
                            "color": "Meta",
                            "stats": "+21 Agility",
                        }
                    ],
                    "enchantment": {
                        "enchant_id": 3789,
                        "name": "Berserking",
                        "stats": "+400 Attack Power proc",
                    },
                }
            ]
        }
    }


class GearSet(BaseModel):
    """Represents a complete set of equipped gear (19 slots in WotLK)."""

    head: Optional[EquippedItem] = None
    neck: Optional[EquippedItem] = None
    shoulder: Optional[EquippedItem] = None
    back: Optional[EquippedItem] = None
    chest: Optional[EquippedItem] = None
    shirt: Optional[EquippedItem] = None
    tabard: Optional[EquippedItem] = None
    wrist: Optional[EquippedItem] = None
    hands: Optional[EquippedItem] = None
    waist: Optional[EquippedItem] = None
    legs: Optional[EquippedItem] = None
    feet: Optional[EquippedItem] = None
    finger1: Optional[EquippedItem] = None
    finger2: Optional[EquippedItem] = None
    trinket1: Optional[EquippedItem] = None
    trinket2: Optional[EquippedItem] = None
    main_hand: Optional[EquippedItem] = None
    off_hand: Optional[EquippedItem] = None
    ranged: Optional[EquippedItem] = None

    def equipped_slots(self) -> int:
        """Return the number of equipped slots."""
        slots = [
            self.head,
            self.neck,
            self.shoulder,
            self.back,
            self.chest,
            self.wrist,
            self.hands,
            self.waist,
            self.legs,
            self.feet,
            self.finger1,
            self.finger2,
            self.trinket1,
            self.trinket2,
            self.main_hand,
            self.off_hand,
            self.ranged,
        ]
        return sum(1 for slot in slots if slot is not None)
