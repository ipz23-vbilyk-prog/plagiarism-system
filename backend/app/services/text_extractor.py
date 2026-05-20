from pypdf import PdfReader
import docx
import os


def extract_text_from_pdf(path: str) -> str:
    try:
        reader = PdfReader(path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        raise ValueError(f"PDF extraction error: {e}")


def extract_text_from_docx(path: str) -> str:
    try:
        doc = docx.Document(path)

        text = "\n".join(
            p.text for p in doc.paragraphs if p.text and p.text.strip()
        )

        return text.strip()

    except Exception as e:
        raise ValueError(f"DOCX extraction error: {e}")


def extract_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    if ext == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(f"Unsupported file format: {ext}")