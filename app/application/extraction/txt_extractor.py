from pathlib import Path

from app.application.extraction.base_extractor import BaseExtractor


class TxtExtractor(BaseExtractor):
    """
    Extracts plain text from .txt files.
    """

    def extract(self, file_path: Path) -> str:
        """
        Extract text from a plain text file.

        Args:
            file_path: Path to the text file.

        Returns:
            The extracted text.
        """

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )