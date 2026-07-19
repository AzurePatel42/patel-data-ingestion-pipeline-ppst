from pathlib import Path

class TextExtractor:


    @staticmethod

    def extract( file_path: Path) -> str:
        
        path = Path(file_path)

        if path.suffix == ".txt":

            return path.read_text(encoding="utf-8")
        
        raise ValueError(f"Unsupported file type: {path.suffix}. Only .txt files are supported.")
    
    