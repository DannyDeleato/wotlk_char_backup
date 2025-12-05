"""AoWoW profile scraper."""

import re
import json
import time
from typing import Optional, Dict, Any, Tuple, List
from urllib.parse import urlparse, parse_qs

import httpx
from bs4 import BeautifulSoup

from ..config import ScrapingConfig
from ..models import Character, GearSet, Achievement, Mount, Pet, CharacterExport
from ..models.gear import EquippedItem, Item, Gem, Enchantment


class AoWowScraperError(Exception):
    """Base exception for AoWoW scraper errors."""

    pass


class ProfileNotFoundError(AoWowScraperError):
    """Raised when a profile cannot be found."""

    pass


class AoWoWScraper:
    """Scraper for AoWoW character profiles."""

    def __init__(self, config: Optional[ScrapingConfig] = None):
        """Initialize the scraper with optional configuration.

        Args:
            config: Scraping configuration. If None, uses defaults.
        """
        self.config = config or ScrapingConfig()
        self.client = httpx.Client(
            timeout=self.config.timeout,
            headers={"User-Agent": self.config.user_agent},
            follow_redirects=True,
        )
        self._last_request_time: float = 0

    def __enter__(self) -> "AoWoWScraper":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        if self._last_request_time > 0:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.config.delay:
                time.sleep(self.config.delay - elapsed)
        self._last_request_time = time.time()

    def _fetch_page(self, url: str) -> str:
        """Fetch a page with retry logic.

        Args:
            url: URL to fetch

        Returns:
            Page HTML content

        Raises:
            AoWowScraperError: If fetching fails after retries
        """
        self._rate_limit()

        for attempt in range(self.config.retries):
            try:
                response = self.client.get(url)
                response.raise_for_status()
                return response.text

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ProfileNotFoundError(f"Profile not found: {url}")
                elif e.response.status_code == 403:
                    raise AoWowScraperError(f"Access forbidden (403): {url}")
                elif attempt < self.config.retries - 1:
                    time.sleep(2**attempt)  # Exponential backoff
                    continue
                else:
                    raise AoWowScraperError(f"HTTP error {e.response.status_code}: {url}")

            except httpx.RequestError as e:
                if attempt < self.config.retries - 1:
                    time.sleep(2**attempt)
                    continue
                else:
                    raise AoWowScraperError(f"Request failed: {e}")

        raise AoWowScraperError(f"Failed to fetch {url} after {self.config.retries} attempts")

    def _parse_profile_url(self, url: str) -> Tuple[str, str, str, str]:
        """Parse AoWoW profile URL to extract components.

        Args:
            url: AoWoW profile URL (e.g., https://db.rising-gods.de/?profile=eu.rising-gods.lopht)

        Returns:
            Tuple of (base_url, region, realm, character)

        Raises:
            ValueError: If URL format is invalid
        """
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        query_params = parse_qs(parsed.query)
        if "profile" not in query_params:
            raise ValueError(f"Invalid AoWoW profile URL: {url}")

        profile = query_params["profile"][0]
        parts = profile.split(".")

        if len(parts) != 3:
            raise ValueError(f"Invalid profile format: {profile}. Expected: region.realm.character")

        region, realm, character = parts
        return base_url, region, realm, character

    def _extract_javascript_data(self, html: str) -> Dict[str, Any]:
        """Extract data from JavaScript variables in the page.

        AoWoW often embeds data in JavaScript variables like g_user, g_profile, etc.

        Args:
            html: Page HTML content

        Returns:
            Dictionary of extracted data
        """
        data: Dict[str, Any] = {}

        # Try to find common AoWoW JavaScript variables
        patterns = [
            (r"var\s+g_user\s*=\s*({.+?});", "g_user"),
            (r"var\s+g_profile\s*=\s*({.+?});", "g_profile"),
            (r"var\s+g_items\s*=\s*({.+?});", "g_items"),
            (r"var\s+g_chr\s*=\s*({.+?});", "g_chr"),
        ]

        for pattern, key in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    data[key] = json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass

        return data

    def _parse_character_info(
        self, html: str, soup: BeautifulSoup, js_data: Dict[str, Any], region: str, realm: str
    ) -> Character:
        """Parse basic character information.

        Args:
            html: Page HTML
            soup: BeautifulSoup parsed HTML
            js_data: Extracted JavaScript data
            region: Character region
            realm: Character realm

        Returns:
            Character model

        Raises:
            AoWowScraperError: If parsing fails
        """
        # Try to get character data from JavaScript
        char_data = js_data.get("g_user", {}) or js_data.get("g_chr", {})

        # Extract character name
        name = char_data.get("name")
        if not name:
            # Try to find in HTML
            name_elem = soup.find("h1", class_=re.compile("name|character-name"))
            if name_elem:
                name = name_elem.get_text(strip=True)

        if not name:
            raise AoWowScraperError("Could not extract character name")

        # Extract level
        level = char_data.get("level", 80)
        if isinstance(level, str):
            level = int(level)

        # Extract race
        race = char_data.get("race", "Unknown")
        if isinstance(race, int):
            race = self._race_id_to_name(race)

        # Extract class
        char_class = char_data.get("class", "Unknown")
        if isinstance(char_class, int):
            char_class = self._class_id_to_name(char_class)

        # Extract faction
        faction = char_data.get("faction", "Unknown")
        if isinstance(faction, int):
            faction = "Alliance" if faction == 1 else "Horde"

        # Extract guild
        guild = char_data.get("guild")

        # Extract title
        title = char_data.get("title")

        # Extract avatar
        avatar_url = char_data.get("avatar")

        return Character(
            name=name,
            realm=realm,
            region=region,
            level=level,
            race=race,
            character_class=char_class,
            faction=faction,
            guild=guild,
            title=title,
            avatar_url=avatar_url,
        )

    def _race_id_to_name(self, race_id: int) -> str:
        """Convert race ID to race name.

        Args:
            race_id: WoW race ID

        Returns:
            Race name
        """
        races = {
            1: "Human",
            2: "Orc",
            3: "Dwarf",
            4: "Night Elf",
            5: "Undead",
            6: "Tauren",
            7: "Gnome",
            8: "Troll",
            10: "Blood Elf",
            11: "Draenei",
        }
        return races.get(race_id, f"Unknown({race_id})")

    def _class_id_to_name(self, class_id: int) -> str:
        """Convert class ID to class name.

        Args:
            class_id: WoW class ID

        Returns:
            Class name
        """
        classes = {
            1: "Warrior",
            2: "Paladin",
            3: "Hunter",
            4: "Rogue",
            5: "Priest",
            6: "Death Knight",
            7: "Shaman",
            8: "Mage",
            9: "Warlock",
            11: "Druid",
        }
        return classes.get(class_id, f"Unknown({class_id})")

    def _parse_item_link(self, item_str: str) -> Optional[Dict[str, Any]]:
        """Parse item link string (e.g., 'item=12345&ench=3000&gems=123:456:789').

        Args:
            item_str: Item link string

        Returns:
            Dictionary with item_id, enchant_id, gem_ids
        """
        result: Dict[str, Any] = {}

        # Parse item ID
        item_match = re.search(r"item=(\d+)", item_str)
        if item_match:
            result["item_id"] = int(item_match.group(1))

        # Parse enchant ID
        ench_match = re.search(r"ench=(\d+)", item_str)
        if ench_match:
            result["enchant_id"] = int(ench_match.group(1))

        # Parse gem IDs
        gems_match = re.search(r"gems=([0-9:]+)", item_str)
        if gems_match:
            gem_ids = [int(g) for g in gems_match.group(1).split(":") if g and g != "0"]
            result["gem_ids"] = gem_ids

        return result if "item_id" in result else None

    def _quality_id_to_name(self, quality_id: int) -> str:
        """Convert item quality ID to name.

        Args:
            quality_id: Item quality ID (0-7)

        Returns:
            Quality name
        """
        qualities = {
            0: "Poor",
            1: "Common",
            2: "Uncommon",
            3: "Rare",
            4: "Epic",
            5: "Legendary",
            6: "Artifact",
            7: "Heirloom",
        }
        return qualities.get(quality_id, "Common")

    def _slot_id_to_name(self, slot_id: int) -> str:
        """Convert equipment slot ID to name.

        Args:
            slot_id: Equipment slot ID

        Returns:
            Slot name
        """
        slots = {
            1: "head",
            2: "neck",
            3: "shoulder",
            15: "back",
            5: "chest",
            4: "shirt",
            19: "tabard",
            9: "wrist",
            10: "hands",
            6: "waist",
            7: "legs",
            8: "feet",
            11: "finger1",
            12: "finger2",
            13: "trinket1",
            14: "trinket2",
            16: "main_hand",
            17: "off_hand",
            18: "ranged",
        }
        return slots.get(slot_id, f"slot_{slot_id}")

    def _parse_gear(
        self, html: str, soup: BeautifulSoup, js_data: Dict[str, Any], base_url: str
    ) -> GearSet:
        """Parse equipped gear with gems and enchantments.

        Args:
            html: Page HTML
            soup: BeautifulSoup parsed HTML
            js_data: Extracted JavaScript data
            base_url: Base URL for constructing icon URLs

        Returns:
            GearSet model
        """
        gear_data: Dict[str, Optional[EquippedItem]] = {}

        # Try to get items from JavaScript data
        items_data = js_data.get("g_items", {})

        if not items_data:
            # Try to find item data in HTML
            # AoWoW typically uses data attributes or JavaScript in item links
            item_links = soup.find_all("a", href=re.compile(r"\?item="))
            for link in item_links:
                href = link.get("href", "")
                item_info = self._parse_item_link(href)
                if item_info:
                    # Extract additional info from data attributes
                    slot_str = link.get("data-slot", "")
                    if slot_str:
                        try:
                            slot_id = int(slot_str)
                            slot_name = self._slot_id_to_name(slot_id)
                        except ValueError:
                            continue
                    else:
                        continue

                    # Build item
                    item = Item(
                        item_id=item_info["item_id"],
                        name=link.get_text(strip=True) or f"Item {item_info['item_id']}",
                        slot=slot_name,
                        quality=self._quality_id_to_name(
                            int(link.get("data-quality", "2"))
                        ),
                        item_level=int(link.get("data-ilvl", "1")),
                        icon_url=None,
                    )

                    # Parse gems
                    gems: List[Gem] = []
                    if "gem_ids" in item_info:
                        for gem_id in item_info["gem_ids"]:
                            gems.append(
                                Gem(
                                    gem_id=gem_id,
                                    name=f"Gem {gem_id}",
                                    color="Unknown",
                                    stats="Unknown",
                                )
                            )

                    # Parse enchantment
                    enchantment = None
                    if "enchant_id" in item_info:
                        enchantment = Enchantment(
                            enchant_id=item_info["enchant_id"],
                            name=f"Enchant {item_info['enchant_id']}",
                            stats="Unknown",
                        )

                    equipped_item = EquippedItem(
                        item=item, gems=gems, enchantment=enchantment
                    )
                    gear_data[slot_name] = equipped_item

        # Handle duplicate slots (finger1/finger2, trinket1/trinket2)
        finger_count = 0
        trinket_count = 0
        final_gear_data: Dict[str, Optional[EquippedItem]] = {}

        for slot_name, item in gear_data.items():
            if "finger" in slot_name:
                finger_count += 1
                final_gear_data[f"finger{finger_count}"] = item
            elif "trinket" in slot_name:
                trinket_count += 1
                final_gear_data[f"trinket{trinket_count}"] = item
            else:
                final_gear_data[slot_name] = item

        return GearSet(**final_gear_data)

    def _parse_achievements(
        self, html: str, soup: BeautifulSoup, js_data: Dict[str, Any], base_url: str
    ) -> List[Achievement]:
        """Parse completed achievements.

        Args:
            html: Page HTML
            soup: BeautifulSoup parsed HTML
            js_data: Extracted JavaScript data
            base_url: Base URL for constructing icon URLs

        Returns:
            List of Achievement models
        """
        achievements: List[Achievement] = []

        # Try to find achievement data in JavaScript
        # Common patterns: g_achievements, listviewachievements, etc.
        achievement_data = js_data.get("g_achievements", {})

        if achievement_data:
            # If we have JavaScript data, parse it
            for ach_id, ach_info in achievement_data.items():
                if isinstance(ach_info, dict):
                    achievement = Achievement(
                        achievement_id=int(ach_id),
                        name=ach_info.get("name", f"Achievement {ach_id}"),
                        description=ach_info.get("description", ""),
                        points=ach_info.get("points", 0),
                        category=ach_info.get("category", "Unknown"),
                        completed_date=None,  # Parse timestamp if available
                        icon_url=ach_info.get("icon"),
                    )
                    achievements.append(achievement)
        else:
            # Try to parse from HTML
            # Look for achievement links or lists
            ach_links = soup.find_all("a", href=re.compile(r"\?achievement="))
            for link in ach_links:
                href = link.get("href", "")
                ach_match = re.search(r"achievement=(\d+)", href)
                if ach_match:
                    ach_id = int(ach_match.group(1))
                    achievement = Achievement(
                        achievement_id=ach_id,
                        name=link.get_text(strip=True) or f"Achievement {ach_id}",
                        description=link.get("title", ""),
                        points=int(link.get("data-points", "0")),
                        category=link.get("data-category", "Unknown"),
                        completed_date=None,
                        icon_url=None,
                    )
                    achievements.append(achievement)

        return achievements

    def _parse_mounts(
        self, html: str, soup: BeautifulSoup, js_data: Dict[str, Any], base_url: str
    ) -> List[Mount]:
        """Parse collected mounts.

        Args:
            html: Page HTML
            soup: BeautifulSoup parsed HTML
            js_data: Extracted JavaScript data
            base_url: Base URL for constructing icon URLs

        Returns:
            List of Mount models
        """
        mounts: List[Mount] = []

        # Try to find mount data in JavaScript
        mount_data = js_data.get("g_mounts", {}) or js_data.get("g_spells", {})

        if mount_data:
            # Parse from JavaScript data
            for mount_id, mount_info in mount_data.items():
                if isinstance(mount_info, dict) and mount_info.get("type") == "mount":
                    mount = Mount(
                        mount_id=int(mount_id),
                        name=mount_info.get("name", f"Mount {mount_id}"),
                        spell_id=int(mount_info.get("spell_id", mount_id)),
                        icon_url=mount_info.get("icon"),
                        source=mount_info.get("source"),
                    )
                    mounts.append(mount)
        else:
            # Try to parse from HTML
            # Look for spell links that are mounts
            spell_links = soup.find_all("a", href=re.compile(r"\?spell="))
            for link in spell_links:
                # Check if this is a mount (usually in a mounts section)
                if "mount" in link.get("class", []) or "mount" in str(link.parent):
                    href = link.get("href", "")
                    spell_match = re.search(r"spell=(\d+)", href)
                    if spell_match:
                        spell_id = int(spell_match.group(1))
                        mount = Mount(
                            mount_id=spell_id,
                            name=link.get_text(strip=True) or f"Mount {spell_id}",
                            spell_id=spell_id,
                            icon_url=None,
                            source=None,
                        )
                        mounts.append(mount)

        return mounts

    def _parse_pets(
        self, html: str, soup: BeautifulSoup, js_data: Dict[str, Any], base_url: str
    ) -> List[Pet]:
        """Parse collected companion pets.

        Args:
            html: Page HTML
            soup: BeautifulSoup parsed HTML
            js_data: Extracted JavaScript data
            base_url: Base URL for constructing icon URLs

        Returns:
            List of Pet models
        """
        pets: List[Pet] = []

        # Try to find pet data in JavaScript
        pet_data = js_data.get("g_pets", {}) or js_data.get("g_companions", {})

        if pet_data:
            # Parse from JavaScript data
            for pet_id, pet_info in pet_data.items():
                if isinstance(pet_info, dict):
                    pet = Pet(
                        pet_id=int(pet_id),
                        name=pet_info.get("name", f"Pet {pet_id}"),
                        spell_id=int(pet_info.get("spell_id", pet_id)),
                        icon_url=pet_info.get("icon"),
                        source=pet_info.get("source"),
                    )
                    pets.append(pet)
        else:
            # Try to parse from HTML
            # Look for spell links that are companion pets
            spell_links = soup.find_all("a", href=re.compile(r"\?spell="))
            for link in spell_links:
                # Check if this is a companion pet
                if "companion" in link.get("class", []) or "pet" in str(link.parent):
                    href = link.get("href", "")
                    spell_match = re.search(r"spell=(\d+)", href)
                    if spell_match:
                        spell_id = int(spell_match.group(1))
                        pet = Pet(
                            pet_id=spell_id,
                            name=link.get_text(strip=True) or f"Pet {spell_id}",
                            spell_id=spell_id,
                            icon_url=None,
                            source=None,
                        )
                        pets.append(pet)

        return pets

    def scrape_profile(self, profile_url: str) -> CharacterExport:
        """Scrape a complete character profile.

        Args:
            profile_url: AoWoW profile URL

        Returns:
            Complete character export data

        Raises:
            AoWowScraperError: If scraping fails
        """
        # Parse URL
        base_url, region, realm, char_name = self._parse_profile_url(profile_url)

        # Fetch profile page
        html = self._fetch_page(profile_url)
        soup = BeautifulSoup(html, "lxml")

        # Extract JavaScript data
        js_data = self._extract_javascript_data(html)

        # Parse character info
        character = self._parse_character_info(html, soup, js_data, region, realm)

        # Parse gear
        gear = self._parse_gear(html, soup, js_data, base_url)

        # Parse achievements
        achievements = self._parse_achievements(html, soup, js_data, base_url)

        # Parse mounts
        mounts = self._parse_mounts(html, soup, js_data, base_url)

        # Parse companion pets
        pets = self._parse_pets(html, soup, js_data, base_url)

        return CharacterExport(
            character=character,
            gear=gear,
            achievements=achievements,
            mounts=mounts,
            pets=pets,
            source_url=profile_url,
        )
