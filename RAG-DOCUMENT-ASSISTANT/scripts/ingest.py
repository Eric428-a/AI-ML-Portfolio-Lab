import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from app.db.database import create_tables
from app.db.database import SessionLocal
from app.db.models import Document
from app.services.ingestion_service import ingestion_service


def main() -> None:
    create_tables()

    db = SessionLocal()

    try:
        documents = db.query(Document).all()

        for document in documents:
            if document.status != "processed":
                print(
                    f"Ingesting: {document.filename}"
                )

                ingestion_service.ingest(
                    document.id
                )

                print(
                    f"Completed: {document.filename}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()