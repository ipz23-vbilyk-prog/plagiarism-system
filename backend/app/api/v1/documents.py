from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import re

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from backend.app.db.session import SessionLocal
from backend.app.models.document import Document

from backend.app.services.file_service import save_file
from backend.app.services.text_extractor import extract_text

from backend.app.services.plagiarism_service import (
    calculate_similarity,
    get_plagiarism_level,
    find_text_matches
)

router = APIRouter()


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- CLEAN TEXT ----------------
def clean_pdf_text(text: str) -> str:
    if not text:
        return ""

    text = str(text)
    text = re.sub(r"[^\w\s\.,\-\(\):;%]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------- CHECK PLAGIARISM ----------------
@router.post("/documents/check-plagiarism")
def check_plagiarism(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_path = save_file(file)
    new_text = extract_text(file_path)

    existing_docs = db.query(Document).all()
    existing_texts = [d.content for d in existing_docs if d.content]

    similarities = calculate_similarity(new_text, existing_texts)

    max_score = max(similarities) if similarities else 0.0
    level = get_plagiarism_level(max_score)

    matches = find_text_matches(new_text, existing_texts)
    if not isinstance(matches, list):
        matches = []

    doc = Document(
        filename=file.filename,
        file_path=file_path,
        content=new_text,
        max_similarity=max_score,
        level=level,
        matches=matches
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "id": doc.id,
        "filename": file.filename,
        "max_similarity": max_score,
        "level": level,
        "matches": matches
    }


# ---------------- HISTORY ----------------
@router.get("/documents/history")
def history(db: Session = Depends(get_db)):

    docs = db.query(Document).all()

    return [
        {
            "id": d.id,
            "filename": d.filename,
            "max_similarity": d.max_similarity,
            "level": d.level
        }
        for d in docs
    ]


# ---------------- PDF REPORT ----------------
@router.get("/documents/report/{document_id}")
def generate_report(document_id: int, db: Session = Depends(get_db)):

    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        return {"error": "Document not found"}

    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    pdf_path = os.path.join(reports_dir, f"report_{document_id}.pdf")

    pdf = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # ---------------- UNIVERSITY HEADER ----------------
    elements.append(Paragraph(
        "NATIONAL UNIVERSITY OF LIFE AND ENVIRONMENTAL SCIENCES OF UKRAINE",
        styles["Title"]
    ))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        "Faculty of Information Technologies",
        styles["Title"]
    ))

    elements.append(Spacer(1, 20))

    # ---------------- REPORT TITLE ----------------
    elements.append(Paragraph(
        "PLAGIARISM ANALYTICAL REPORT",
        styles["Heading1"]
    ))

    elements.append(Spacer(1, 14))

    # ---------------- BASIC INFO ----------------
    elements.append(Paragraph(
        f"<b>Document:</b> {clean_pdf_text(document.filename)}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"<b>Similarity score:</b> {round(document.max_similarity * 100)}%",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"<b>Plagiarism level:</b> {document.level.upper()}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 20))

    # ---------------- ANALYTICAL REPORT ONLY ----------------
    elements.append(Paragraph(
        "ANALYTICAL REPORT",
        styles["Heading2"]
    ))

    elements.append(Spacer(1, 10))

    match_count = len(document.matches) if document.matches else 0

    if document.level == "low":
        analysis = "The document shows minimal similarity with existing sources."
    elif document.level == "medium":
        analysis = "Moderate similarity detected. Revision is recommended."
    else:
        analysis = "High similarity detected. Significant parts match existing sources."

    elements.append(Paragraph(
        f"<b>Total detected similarities:</b> {match_count}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        f"<b>Conclusion:</b> {analysis}",
        styles["Normal"]
    ))

    # ---------------- BUILD PDF ----------------
    pdf.build(elements)

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"plagiarism_report_{document_id}.pdf"
    )