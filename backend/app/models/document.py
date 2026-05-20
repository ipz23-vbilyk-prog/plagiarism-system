from sqlalchemy import Column, Integer, String, Text, Float, JSON

from backend.app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    file_path = Column(String, nullable=True)

    content = Column(Text, nullable=True)

    # 🔥 результат перевірки
    max_similarity = Column(Float, default=0)

    # green / yellow / red
    level = Column(String, default="green")

    # список співпадінь
    matches = Column(JSON, nullable=True)