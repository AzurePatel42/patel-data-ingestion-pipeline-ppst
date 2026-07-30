from app.application.extraction.base_extractor import BaseExtractor
from app.application.extraction.csv_extractor import CsvExtractor
from app.application.extraction.docx_extractor import DocxExtractor
from app.application.extraction.html_extractor import HtmlExtractor
from app.application.extraction.json_extractor import JsonExtractor
from app.application.extraction.markdown_extractor import MarkdownExtractor
from app.application.extraction.pdf_extractor import PdfExtractor
from app.application.extraction.txt_extractor import TxtExtractor
from app.application.extraction.xml_extractor import XmlExtractor
from app.core.exceptions import UnsupportedDocumentException


class ExtractorFactory:
    """
    Factory responsible for creating document extractors
    based on file extension.
    """

    _extractors: dict[str, type[BaseExtractor]] = {
        ".txt": TxtExtractor,
        ".pdf": PdfExtractor,
        ".docx": DocxExtractor,
        ".md": MarkdownExtractor,
        ".html": HtmlExtractor,
        ".csv": CsvExtractor,
        ".json": JsonExtractor,
        ".xml": XmlExtractor,
    }

    @classmethod
    def get_extractor(cls, file_extension: str) -> BaseExtractor:
        """
        Return the appropriate extractor for a file extension.

        Args:
            file_extension: File extension including the leading dot
                            (e.g. ".pdf", ".txt").

        Returns:
            A document extractor instance.

        Raises:
            UnsupportedDocumentException:
                If the file extension is not supported.
        """

        extractor_class = cls._extractors.get(file_extension.lower())

        if extractor_class is None:
            raise UnsupportedDocumentException(
                f"Unsupported document type: {file_extension}"
            )

        return extractor_class()