"""Export data model combining all character data."""

from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

from .character import Character
from .gear import GearSet
from .achievements import Achievement
from .collections import Mount, Pet


class CharacterExport(BaseModel):
    """Complete character export data."""

    character: Character = Field(..., description="Character basic information")
    gear: GearSet = Field(..., description="Equipped gear with gems and enchantments")
    achievements: List[Achievement] = Field(
        default_factory=list, description="Completed achievements"
    )
    mounts: List[Mount] = Field(default_factory=list, description="Collected mounts")
    pets: List[Pet] = Field(default_factory=list, description="Collected companion pets")
    export_date: datetime = Field(
        default_factory=datetime.now, description="When this export was created"
    )
    source_url: str = Field(..., description="Original AoWoW profile URL")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "character": {
                        "name": "Lopht",
                        "realm": "rising-gods",
                        "region": "eu",
                        "level": 80,
                        "race": "Human",
                        "class": "Paladin",
                        "faction": "Alliance",
                    },
                    "gear": {"head": None, "neck": None},
                    "achievements": [],
                    "mounts": [],
                    "pets": [],
                    "export_date": "2024-01-15T10:30:00Z",
                    "source_url": "https://db.rising-gods.de/?profile=eu.rising-gods.lopht",
                }
            ]
        }
    }
