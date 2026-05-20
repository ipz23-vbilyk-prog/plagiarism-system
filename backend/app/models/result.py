from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text
from datetime import datetime
from backend.app.db.base import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"))

    similarity_score = Column(Float, default=0.0)
    unique_score = Column(Float, default=100.0)

    matched_fragments = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)