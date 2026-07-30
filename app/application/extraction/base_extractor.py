from abc import ABC, abstractmethod
from pathlib import Path


class BaseExtractor(ABC):
    """
    Base interface for all document extractors.
    """

    @abstractmethod
    def extract(self, file_path: Path) -> str:
        """
        Extract text from a document.

        Args:
            file_path: Path to the document.

        Returns:
            Extracted plain text.
        """
        pass