"""Character base model."""

from typing import Optional
from pydantic import BaseModel, Field


class Character(BaseModel):
    """Represents a WoW character's basic information."""

    name: str = Field(..., description="Character name")
    realm: str = Field(..., description="Server/realm name")
    region: str = Field(..., description="Region (e.g., 'eu', 'us')")
    level: int = Field(..., ge=1, le=80, description="Character level (1-80 for WotLK)")
    race: str = Field(..., description="Character race")
    character_class: str = Field(..., description="Character class", alias="class")
    faction: str = Field(..., description="Faction: Alliance or Horde")
    guild: Optional[str] = Field(None, description="Guild name if any")
    title: Optional[str] = Field(None, description="Character title")
    avatar_url: Optional[str] = Field(None, description="Character portrait/avatar URL")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Lopht",
                    "realm": "rising-gods",
                    "region": "eu",
                    "level": 80,
                    "race": "Human",
                    "class": "Paladin",
                    "faction": "Alliance",
                    "guild": "Example Guild",
                    "title": "the Argent Champion",
                    "avatar_url": "https://example.com/avatar.jpg",
                }
            ]
        }
    }
