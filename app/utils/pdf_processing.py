# app/utils/pdf_processing.py
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts and returns text content from a PDF file using pypdf."""
    text = ""
    with open(file_path, "rb") as file:
        pdf = PdfReader(file)
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text() or ""
    print(text)
    return text
