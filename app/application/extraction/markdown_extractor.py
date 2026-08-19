from pathlib import Path

from app.application.extraction.base_extractor import BaseExtractor


class MarkdownExtractor(BaseExtractor):
    """
    Extracts plain text from .md files.
    """

    def extract(self, file_path: Path) -> str:
        """
        Extract Markdown content as text.

        Args:
            file_path: Path to the Markdown file.

        Returns:
            Markdown content as plain text.
        """

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )