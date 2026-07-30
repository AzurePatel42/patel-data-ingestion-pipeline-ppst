from pathlib import Path

from docx import Document

from app.application.extraction.base_extractor import BaseExtractor


class DocxExtractor(BaseExtractor):
    """
    Extracts plain text from Microsoft Word (.docx) documents.
    """

    def extract(self, file_path: Path) -> str:
        """
        Extract text from a DOCX document.

        Args:
            file_path: Path to the DOCX file.

        Returns:
            The extracted text as a single string.
        """

        document = Document(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)