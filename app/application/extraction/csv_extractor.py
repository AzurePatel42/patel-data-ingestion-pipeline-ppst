import csv
from pathlib import Path

from app.application.extraction.base_extractor import BaseExtractor


class CsvExtractor(BaseExtractor):
    """
    Extracts text from .csv files.
    """

    def extract(self, file_path: Path) -> str:
        """
        Extract CSV content and return it as plain text.

        Args:
            file_path: Path to the CSV file.

        Returns:
            CSV rows represented as newline-delimited text.
        """

        rows: list[str] = []

        with file_path.open(
            mode="r",
            encoding="utf-8",
            errors="ignore",
            newline="",
        ) as file:

            reader = csv.reader(file)

            for row in reader:
                rows.append(" | ".join(row))

        return "\n".join(rows)