"""Tests for JSON exporter."""

import json
import gzip
from pathlib import Path
import pytest

from wotlk_char_backup.models import Character, GearSet, CharacterExport
from wotlk_char_backup.exporters import JSONExporter


@pytest.fixture
def sample_export():
    """Create a sample character export."""
    char = Character(
        name="TestChar",
        realm="test-realm",
        region="eu",
        level=80,
        race="Human",
        **{"class": "Paladin"},
        faction="Alliance",
    )
    return CharacterExport(
        character=char,
        gear=GearSet(),
        achievements=[],
        mounts=[],
        pets=[],
        source_url="https://example.com",
    )


def test_exporter_initialization():
    """Test exporter can be initialized."""
    exporter = JSONExporter()
    assert exporter.pretty is True
    assert exporter.compress is False


def test_export_to_string(sample_export):
    """Test export to JSON string."""
    exporter = JSONExporter()
    json_str = exporter.export_to_string(sample_export)

    assert isinstance(json_str, str)
    assert "TestChar" in json_str
    assert "metadata" in json_str

    # Verify it's valid JSON
    data = json.loads(json_str)
    assert data["metadata"]["character_name"] == "TestChar"
    assert data["data"]["character"]["name"] == "TestChar"


def test_export_to_string_not_pretty(sample_export):
    """Test export without pretty formatting."""
    exporter = JSONExporter(pretty=False)
    json_str = exporter.export_to_string(sample_export)

    assert "\n" not in json_str  # No newlines in compact JSON


def test_export_to_file(sample_export, tmp_path):
    """Test export to file."""
    exporter = JSONExporter()
    output_file = tmp_path / "test_export.json"

    result_path = exporter.export_to_file(sample_export, output_file)

    assert result_path == output_file
    assert output_file.exists()

    # Verify content
    data = json.loads(output_file.read_text())
    assert data["data"]["character"]["name"] == "TestChar"


def test_export_to_file_auto_name(sample_export, tmp_path, monkeypatch):
    """Test export with auto-generated filename."""
    monkeypatch.chdir(tmp_path)

    exporter = JSONExporter()
    result_path = exporter.export_to_file(sample_export)

    assert result_path.exists()
    assert "TestChar" in result_path.name
    assert "test-realm" in result_path.name
    assert result_path.suffix == ".json"


def test_export_compressed(sample_export, tmp_path):
    """Test compressed export."""
    exporter = JSONExporter(compress=True)
    output_file = tmp_path / "test_export.json.gz"

    result_path = exporter.export_to_file(sample_export, output_file)

    assert result_path.exists()

    # Verify it's gzipped
    with gzip.open(output_file, "rt", encoding="utf-8") as f:
        content = f.read()
        data = json.loads(content)
        assert data["data"]["character"]["name"] == "TestChar"


def test_export_partial_include(sample_export):
    """Test partial export with include."""
    exporter = JSONExporter()
    json_str = exporter.export_partial(sample_export, include=["gear"])

    data = json.loads(json_str)
    assert "character" in data["data"]  # Always included
    assert "gear" in data["data"]
    assert "achievements" not in data["data"]
    assert "mounts" not in data["data"]
    assert "pets" not in data["data"]


def test_export_partial_exclude(sample_export):
    """Test partial export with exclude."""
    exporter = JSONExporter()
    json_str = exporter.export_partial(sample_export, exclude=["achievements", "mounts"])

    data = json.loads(json_str)
    assert "character" in data["data"]
    assert "gear" in data["data"]
    assert "achievements" not in data["data"]
    assert "mounts" not in data["data"]
    assert "pets" in data["data"]
