import logging
from pathlib import Path

from pypdf import PdfReader

from app.application.extraction.base_extractor import BaseExtractor
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class PdfExtractor(BaseExtractor):
    """
    Extracts plain text from PDF documents.
    """

    def extract(self, file_path: Path) -> str:
        """
        Extract text from a PDF document.

        Args:
            file_path: Path to the PDF file.

        Returns:
            The extracted text as a single string.

        Raises:
            AppException: If the PDF cannot be read or parsed.
        """

        try:
            logger.info(
                "Extracting text from PDF: %s",
                file_path,
            )

            reader = PdfReader(file_path)

            pages: list[str] = []

            for page_number, page in enumerate(reader.pages, start=1):

                text = page.extract_text() or ""

                if text.strip():
                    pages.append(text)

                logger.debug(
                    "Processed page %d",
                    page_number,
                )

            extracted_text = "\n".join(pages)

            logger.info(
                "Successfully extracted %d pages from '%s'",
                len(pages),
                file_path.name,
            )

            return extracted_text

        except Exception as ex:

            logger.exception(
                "Failed to extract text from PDF '%s'",
                file_path,
            )

            raise AppException(
                f"Failed to extract text from PDF '{file_path.name}'."
            ) from ex