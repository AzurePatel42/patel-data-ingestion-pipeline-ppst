import json

from app.application.extraction.csv_extractor import CsvExtractor
from app.application.extraction.html_extractor import HtmlExtractor
from app.application.extraction.json_extractor import JsonExtractor
from app.application.extraction.markdown_extractor import MarkdownExtractor
from app.application.extraction.xml_extractor import XmlExtractor


def test_csv_extractor(tmp_path):
    file_path = tmp_path / "sample.csv"

    file_path.write_text(
        "name,age\nMahesh,53\nJohn,30\n",
        encoding="utf-8",
    )

    result = CsvExtractor().extract(file_path)

    assert result == "name | age\nMahesh | 53\nJohn | 30"


def test_html_extractor(tmp_path):
    file_path = tmp_path / "sample.html"

    file_path.write_text(
        """
        <html>
            <body>
                <h1>Hello World</h1>
                <p>This is a test document.</p>
            </body>
        </html>
        """,
        encoding="utf-8",
    )

    result = HtmlExtractor().extract(file_path)

    assert "Hello World" in result
    assert "This is a test document." in result
    assert "<h1>" not in result
    assert "<p>" not in result


def test_json_extractor_valid_json(tmp_path):
    file_path = tmp_path / "sample.json"

    data = {
        "name": "Mahesh",
        "project": "Data Ingestion Pipeline",
        "active": True,
    }

    file_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    result = JsonExtractor().extract(file_path)

    parsed = json.loads(result)

    assert parsed == data


def test_json_extractor_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"

    content = '{"name": "Mahesh", invalid}'

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    result = JsonExtractor().extract(file_path)

    assert result == content


def test_markdown_extractor(tmp_path):
    file_path = tmp_path / "sample.md"

    content = """# Data Ingestion Pipeline

This is a test document.

- Chunking
- Embeddings
- pgvector
"""

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    result = MarkdownExtractor().extract(file_path)

    assert result == content


def test_xml_extractor(tmp_path):
    file_path = tmp_path / "sample.xml"

    content = """<?xml version="1.0"?>
<document>
    <title>Data Ingestion Pipeline</title>
    <description>Test XML document</description>
    <items>
        <item>Chunking</item>
        <item>Embeddings</item>
    </items>
</document>
"""

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    result = XmlExtractor().extract(file_path)

    assert "Data Ingestion Pipeline" in result
    assert "Test XML document" in result
    assert "Chunking" in result
    assert "Embeddings" in result
    assert "<document>" not in result