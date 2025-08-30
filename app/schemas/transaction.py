 
from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Optional

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionBase(BaseModel):
    amount: float
    type: TransactionType
    category: str
    description: Optional[str] = None
    date: date

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionSummary(BaseModel):
    category: str
    total_amount: float

class DateSummary(BaseModel):
    date: date
    total_amount: float

class PaginatedTransactions(BaseModel):
    items: list[Transaction]
    total: int
    page: int
    pages: int