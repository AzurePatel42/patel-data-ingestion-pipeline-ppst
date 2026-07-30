from pathlib import Path

from pypdf import PdfReader

from app.application.extraction.base_extractor import BaseExtractor


class PdfExtractor(BaseExtractor):
    """
    Extracts text from PDF documents.
    """

    def extract(self, file_path: Path) -> str:
        reader = PdfReader(file_path)

        pages: list[str] = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)