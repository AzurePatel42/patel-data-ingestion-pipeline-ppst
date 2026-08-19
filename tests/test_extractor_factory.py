import pytest

from app.application.extraction.csv_extractor import CsvExtractor
from app.application.extraction.docx_extractor import DocxExtractor
from app.application.extraction.extractor_factory import ExtractorFactory
from app.application.extraction.html_extractor import HtmlExtractor
from app.application.extraction.json_extractor import JsonExtractor
from app.application.extraction.markdown_extractor import MarkdownExtractor
from app.application.extraction.pdf_extractor import PdfExtractor
from app.application.extraction.txt_extractor import TxtExtractor
from app.application.extraction.xml_extractor import XmlExtractor
from app.core.exceptions import UnsupportedDocumentException


@pytest.mark.parametrize(
    "extension, expected_extractor",
    [
        (".txt", TxtExtractor),
        (".pdf", PdfExtractor),
        (".docx", DocxExtractor),
        (".md", MarkdownExtractor),
        (".html", HtmlExtractor),
        (".csv", CsvExtractor),
        (".json", JsonExtractor),
        (".xml", XmlExtractor),
    ],
)
def test_factory_returns_correct_extractor(
    extension,
    expected_extractor,
):
    extractor = ExtractorFactory.get_extractor(extension)

    assert isinstance(extractor, expected_extractor)


def test_factory_is_case_insensitive():
    extractor = ExtractorFactory.get_extractor(".PDF")

    assert isinstance(extractor, PdfExtractor)


def test_factory_rejects_unsupported_extension():
    with pytest.raises(UnsupportedDocumentException):
        ExtractorFactory.get_extractor(".exe")