

class ChunkingService:
    @staticmethod
    def chunk(text: str, chunk_size: int = 1000) -> list[str]:
        """
        Splits the input text into chunks of specified size.

        Args:
            text (str): The input text to be chunked.
            chunk_size (int): The maximum size of each chunk.

        Returns:
            list[str]: A list of text chunks.
        """
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]