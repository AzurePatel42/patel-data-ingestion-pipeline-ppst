from html.parser import HTMLParser
from pathlib import Path

from app.application.extraction.base_extractor import BaseExtractor


class _TextExtractor(HTMLParser):
    """Extract visible text from HTML."""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()

        if text:
            self.parts.append(text)

    def get_text(self) -> str:
        return "\n".join(self.parts)


class HtmlExtractor(BaseExtractor):
    """
    Extracts visible text from .html files.
    """

    def extract(self, file_path: Path) -> str:
        """
        Extract visible text from an HTML document.

        Args:
            file_path: Path to the HTML file.

        Returns:
            Extracted plain text.
        """

        html_content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        parser = _TextExtractor()
        parser.feed(html_content)
        parser.close()

        return parser.get_text()