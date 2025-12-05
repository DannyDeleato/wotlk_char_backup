"""Configuration management for WotLK Character Backup."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ScrapingConfig:
    """Configuration for web scraping behavior."""

    delay: float = 1.0  # Seconds between requests
    timeout: int = 30  # Request timeout in seconds
    retries: int = 3  # Number of retry attempts
    user_agent: str = "WotLK-Backup/0.1.0"


@dataclass
class Config:
    """Main application configuration."""

    scraping: ScrapingConfig = ScrapingConfig()
    output_format: str = "json"
    compress: bool = False
    verbose: bool = False


# Default configuration instance
default_config = Config()
