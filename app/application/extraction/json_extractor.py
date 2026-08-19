import json
from pathlib import Path

from app.application.extraction.base_extractor import BaseExtractor


class JsonExtractor(BaseExtractor):
    """
    Extracts text from .json files.
    """

    def extract(self, file_path: Path) -> str:
        """
        Read JSON and return a normalized text representation.

        Args:
            file_path: Path to the JSON file.

        Returns:
            JSON content as formatted text.
        """

        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        try:
            data = json.loads(content)

            return json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )

        except json.JSONDecodeError:
            # Preserve the original content if the file
            # contains invalid JSON.
            return content