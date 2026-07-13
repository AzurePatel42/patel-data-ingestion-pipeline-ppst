class DocumentRules:

    @staticmethod
    def is_supported_file(filename: str) -> bool:

        allowed = [
            ".pdf",
            ".docx",
            ".txt"
        ]

        return any(filename.lower().endswith(ext) for ext in allowed)