 
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.schemas.receipt import Receipt
from app.services.receipt_service import ReceiptService
from app.services.auth_service import get_current_user
from app.models.user import User
import os
import uuid

router = APIRouter(prefix="/receipts", tags=["receipts"])

@router.post("/upload", response_model=Receipt)
async def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    os.makedirs("uploads", exist_ok=True)
    

    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join("uploads", filename)
    

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    

    receipt_service = ReceiptService(db)
    return receipt_service.process_receipt(current_user.id, file_path, file_extension)

@router.post("/upload-pdf", response_model=list[Receipt])
async def upload_pdf_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    os.makedirs("uploads", exist_ok=True)
    

    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join("uploads", filename)
    

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    

    receipt_service = ReceiptService(db)
    return receipt_service.process_pdf_transactions(current_user.id, file_path)