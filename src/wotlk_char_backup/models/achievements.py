"""Achievement models."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Achievement(BaseModel):
    """Represents a WoW achievement."""

    achievement_id: int = Field(..., description="Achievement ID")
    name: str = Field(..., description="Achievement name")
    description: str = Field(..., description="Achievement description")
    points: int = Field(..., ge=0, description="Achievement point value")
    category: str = Field(..., description="Achievement category")
    completed_date: Optional[datetime] = Field(None, description="Date achievement was completed")
    icon_url: Optional[str] = Field(None, description="Achievement icon URL")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "achievement_id": 2186,
                    "name": "The Immortal",
                    "description": "Within one raid lockout, defeat every boss in Naxxramas without allowing any raid member to die during any of the boss encounters in 25-player mode.",
                    "points": 10,
                    "category": "Dungeons & Raids",
                    "completed_date": "2024-01-15T20:30:00Z",
                    "icon_url": "https://example.com/achievement.jpg",
                }
            ]
        }
    }
