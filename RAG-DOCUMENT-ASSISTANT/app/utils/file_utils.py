from pathlib import Path

from app.core.config import settings


def ensure_data_directories() -> None:
    directories = (
        settings.upload_dir,
        settings.document_dir,
        settings.processed_dir,
        settings.vector_store_path,
    )

    for directory in directories:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def file_exists(path: str | Path) -> bool:
    return Path(path).is_file()