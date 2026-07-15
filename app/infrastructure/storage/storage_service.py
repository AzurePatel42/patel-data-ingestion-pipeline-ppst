from pathlib import Path
import shutil

from app.core.config import settings


class StorageService:

    def __init__(self, upload_dir: str | None = None):
        self.upload_dir = Path(
            upload_dir if upload_dir is not None else settings.UPLOAD_DIRECTORY
        )
        self.upload_dir.mkdir(exist_ok=True)

    def save(self, file):

        destination = self.upload_dir / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return str(destination)