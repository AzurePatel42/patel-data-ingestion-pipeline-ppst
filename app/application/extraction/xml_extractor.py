import xml.etree.ElementTree as ET
from pathlib import Path

from app.application.extraction.base_extractor import BaseExtractor


class XmlExtractor(BaseExtractor):
    """
    Extracts text from .xml files.
    """

    def extract(self, file_path: Path) -> str:
        """
        Extract text content from an XML document.

        Args:
            file_path: Path to the XML file.

        Returns:
            Extracted text content.
        """

        tree = ET.parse(file_path)
        root = tree.getroot()

        text_parts = [
            text.strip()
            for text in root.itertext()
            if text and text.strip()
        ]

        return "\n".join(text_parts)