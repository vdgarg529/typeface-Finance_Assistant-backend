 
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReceiptBase(BaseModel):
    file_path: str

class ReceiptCreate(ReceiptBase):
    pass

class Receipt(ReceiptBase):
    id: int
    user_id: int
    parsed_text: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True