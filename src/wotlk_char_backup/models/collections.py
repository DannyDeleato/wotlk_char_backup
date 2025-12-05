"""Mount and pet collection models."""

from typing import Optional
from pydantic import BaseModel, Field


class Mount(BaseModel):
    """Represents a collected mount."""

    mount_id: int = Field(..., description="Mount ID (spell ID)")
    name: str = Field(..., description="Mount name")
    spell_id: int = Field(..., description="Mount summoning spell ID")
    icon_url: Optional[str] = Field(None, description="Mount icon URL")
    source: Optional[str] = Field(None, description="How the mount was obtained")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "mount_id": 48954,
                    "name": "Swift Zhevra",
                    "spell_id": 49322,
                    "icon_url": "https://example.com/mount.jpg",
                    "source": "Recruit-A-Friend",
                }
            ]
        }
    }


class Pet(BaseModel):
    """Represents a collected companion pet (non-combat)."""

    pet_id: int = Field(..., description="Pet ID (spell ID)")
    name: str = Field(..., description="Pet name")
    spell_id: int = Field(..., description="Pet summoning spell ID")
    icon_url: Optional[str] = Field(None, description="Pet icon URL")
    source: Optional[str] = Field(None, description="How the pet was obtained")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "pet_id": 32498,
                    "name": "Mr. Wiggles",
                    "spell_id": 10715,
                    "icon_url": "https://example.com/pet.jpg",
                    "source": "Vendor: Jeremiah Payson",
                }
            ]
        }
    }
