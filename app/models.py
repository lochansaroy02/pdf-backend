# backend/app/models.py

from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime




class PDFDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    text_content = Column(String) #check
    # Add other fields as necessary


