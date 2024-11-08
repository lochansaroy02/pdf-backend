# app/api/endpoints/upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PDFDocument
import boto3
import os
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# Initialize the S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_S3_BUCKET")



@router.get("/upload")
async def root():
    return {"message": "Hello from FastAPI on Koyeb!"}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read file content
        file_content = await file.read()

        # Upload the file to S3
        s3_client.put_object(Bucket=BUCKET_NAME,
                             Key=file.filename, Body=file_content)

        # Optionally save metadata to the database
        pdf_doc = PDFDocument(filename=file.filename,
                              upload_date=datetime.now())
        db.add(pdf_doc)
        db.commit()
        db.refresh(pdf_doc)

        return {"filename": file.filename, "id": pdf_doc.id}

    except NoCredentialsError:
        raise HTTPException(
            status_code=403, detail="AWS credentials not found.")
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"AWS error: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
