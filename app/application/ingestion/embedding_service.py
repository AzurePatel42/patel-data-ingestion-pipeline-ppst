class EmbeddingService:

    @staticmethod
    def generate(chunks: list[str]) -> list[list[float]]:
        """
        Placeholder embedding generator.

        This will later be replaced by OpenAI or another
        embedding model without changing the pipeline.
        """

        embeddings = []

        for chunk in chunks:
            embeddings.append([
                float(len(chunk))
            ])

        return embeddings