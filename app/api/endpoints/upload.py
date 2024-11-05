# app/api/endpoints/upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db 
from app.models import PDFDocument
from app.utils.pdf_processing import extract_text_from_pdf
import shutil
import os  # Import os module
from datetime import datetime

router = APIRouter()

@router.get("/upload")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        upload_directory = "uploads"
        os.makedirs(upload_directory, exist_ok=True)
        file_location = os.path.join(upload_directory, file.filename)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        pdf_text = extract_text_from_pdf(file_location)

        # Save metadata and extracted text to database
        pdf_doc = PDFDocument(filename=file.filename, upload_date=datetime.now(), text_content=pdf_text)
        db.add(pdf_doc)
        db.commit()
        db.refresh(pdf_doc)

        return {"filename": file.filename, "id": pdf_doc.id}
    except Exception as e:
        # Log the exception
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")