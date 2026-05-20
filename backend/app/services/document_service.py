from sqlalchemy.orm import Session
from backend.app.models.document import Document


def create_document(db: Session, filename: str, content: str):
    document = Document(
        filename=filename,
        content=content
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def save_results(db: Session, document: Document, max_similarity: float, level: str):
    document.max_similarity = max_similarity
    document.level = level

    db.commit()
    db.refresh(document)

    return document