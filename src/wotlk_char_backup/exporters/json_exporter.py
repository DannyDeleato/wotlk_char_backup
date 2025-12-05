"""JSON export functionality."""

import json
import gzip
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from ..models import CharacterExport
from .. import __version__


class JSONExporter:
    """Export character data to JSON format."""

    def __init__(self, pretty: bool = True, compress: bool = False):
        """Initialize the JSON exporter.

        Args:
            pretty: If True, format JSON with indentation
            compress: If True, compress output with gzip
        """
        self.pretty = pretty
        self.compress = compress

    def _add_metadata(self, data: Dict[str, Any], export: CharacterExport) -> Dict[str, Any]:
        """Add export metadata to the output.

        Args:
            data: Serialized export data
            export: Original export object

        Returns:
            Data with metadata added
        """
        return {
            "metadata": {
                "export_version": __version__,
                "export_date": datetime.now().isoformat(),
                "source_url": export.source_url,
                "character_name": export.character.name,
                "character_realm": export.character.realm,
            },
            "data": data,
        }

    def export_to_string(self, character_export: CharacterExport) -> str:
        """Export character data to JSON string.

        Args:
            character_export: Character data to export

        Returns:
            JSON string
        """
        # Serialize to dict
        data = character_export.model_dump(mode="json")

        # Add metadata
        output = self._add_metadata(data, character_export)

        # Convert to JSON
        if self.pretty:
            return json.dumps(output, indent=2, ensure_ascii=False)
        else:
            return json.dumps(output, ensure_ascii=False)

    def export_to_file(
        self, character_export: CharacterExport, output_path: Optional[Path] = None
    ) -> Path:
        """Export character data to JSON file.

        Args:
            character_export: Character data to export
            output_path: Output file path. If None, auto-generates filename.

        Returns:
            Path to the created file
        """
        # Generate default filename if not provided
        if output_path is None:
            char = character_export.character
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{char.name}_{char.realm}_{timestamp}.json"
            if self.compress:
                filename += ".gz"
            output_path = Path(filename)

        # Get JSON string
        json_str = self.export_to_string(character_export)

        # Write to file
        if self.compress:
            with gzip.open(output_path, "wt", encoding="utf-8") as f:
                f.write(json_str)
        else:
            output_path.write_text(json_str, encoding="utf-8")

        return output_path

    def export_partial(
        self,
        character_export: CharacterExport,
        include: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
    ) -> str:
        """Export only selected parts of character data.

        Args:
            character_export: Character data to export
            include: List of fields to include (e.g., ['gear', 'achievements'])
            exclude: List of fields to exclude

        Returns:
            JSON string with partial data
        """
        # Serialize to dict
        data = character_export.model_dump(mode="json")

        # Apply filters
        if include:
            filtered_data = {"character": data["character"]}  # Always include character info
            for field in include:
                if field in data and field != "character":
                    filtered_data[field] = data[field]
            data = filtered_data

        if exclude:
            for field in exclude:
                data.pop(field, None)

        # Add metadata
        output = self._add_metadata(data, character_export)

        # Convert to JSON
        if self.pretty:
            return json.dumps(output, indent=2, ensure_ascii=False)
        else:
            return json.dumps(output, ensure_ascii=False)
