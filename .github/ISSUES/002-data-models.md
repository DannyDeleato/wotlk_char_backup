# Issue #002: Define Data Models

## Description
Create Pydantic data models to represent all character data that can be exported from AoWoW.

## Tasks
- [ ] Create `Character` base model with:
  - `name: str`
  - `realm: str`
  - `region: str`
  - `level: int`
  - `race: str`
  - `character_class: str`
  - `faction: str` (Alliance/Horde)
  - `guild: Optional[str]`
  - `title: Optional[str]`
  - `avatar_url: Optional[str]`

- [ ] Create `Item` model with:
  - `item_id: int`
  - `name: str`
  - `slot: str`
  - `quality: str` (Common, Uncommon, Rare, Epic, Legendary)
  - `item_level: int`
  - `icon_url: Optional[str]`

- [ ] Create `Gem` model with:
  - `gem_id: int`
  - `name: str`
  - `color: str` (Red, Blue, Yellow, Meta, Prismatic)
  - `stats: str`

- [ ] Create `Enchantment` model with:
  - `enchant_id: int`
  - `name: str`
  - `stats: str`

- [ ] Create `EquippedItem` model combining Item + Gems + Enchantment:
  - `item: Item`
  - `gems: List[Gem]`
  - `enchantment: Optional[Enchantment]`

- [ ] Create `GearSet` model:
  - `head: Optional[EquippedItem]`
  - `neck: Optional[EquippedItem]`
  - `shoulder: Optional[EquippedItem]`
  - `back: Optional[EquippedItem]`
  - `chest: Optional[EquippedItem]`
  - `shirt: Optional[EquippedItem]`
  - `tabard: Optional[EquippedItem]`
  - `wrist: Optional[EquippedItem]`
  - `hands: Optional[EquippedItem]`
  - `waist: Optional[EquippedItem]`
  - `legs: Optional[EquippedItem]`
  - `feet: Optional[EquippedItem]`
  - `finger1: Optional[EquippedItem]`
  - `finger2: Optional[EquippedItem]`
  - `trinket1: Optional[EquippedItem]`
  - `trinket2: Optional[EquippedItem]`
  - `main_hand: Optional[EquippedItem]`
  - `off_hand: Optional[EquippedItem]`
  - `ranged: Optional[EquippedItem]`

- [ ] Create `Achievement` model:
  - `achievement_id: int`
  - `name: str`
  - `description: str`
  - `points: int`
  - `category: str`
  - `completed_date: Optional[datetime]`
  - `icon_url: Optional[str]`

- [ ] Create `Mount` model:
  - `mount_id: int`
  - `name: str`
  - `spell_id: int`
  - `icon_url: Optional[str]`
  - `source: Optional[str]`

- [ ] Create `Pet` model (companion/non-combat):
  - `pet_id: int`
  - `name: str`
  - `spell_id: int`
  - `icon_url: Optional[str]`
  - `source: Optional[str]`

- [ ] Create `CharacterExport` model combining all:
  - `character: Character`
  - `gear: GearSet`
  - `achievements: List[Achievement]`
  - `mounts: List[Mount]`
  - `pets: List[Pet]`
  - `export_date: datetime`
  - `source_url: str`

## Acceptance Criteria
- All models are defined with proper types and validation
- Models can be serialized to JSON
- Models include docstrings and examples

## Labels
`models`, `core`

## Priority
High - Required before scraper implementation
