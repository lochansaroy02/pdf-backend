# backend/app/api/endpoints/ask.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import PDFDocument
from app.utils.nlp_processing import answer_question

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ask")
async def ask_question(document_id: int, question: str, db: Session = Depends(get_db)):
    pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == document_id).first()
    if not pdf_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Process the question using NLP (placeholder for LangChain/LlamaIndex usage)
    answer = answer_question(pdf_doc.text_content, question)  # Custom function to be implemented

    return {"answer": answer}
