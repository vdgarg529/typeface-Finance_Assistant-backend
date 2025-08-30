 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.db.session import get_db
from app.schemas.transaction import (
    Transaction, TransactionCreate, TransactionSummary, DateSummary, PaginatedTransactions
)
from app.services.transaction_service import TransactionService
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=Transaction)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return transaction_service.create_transaction(current_user.id, transaction_data)

@router.get("/", response_model=PaginatedTransactions)
def get_transactions(
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
    type: Optional[str] = Query(None, description="Filter by type (income/expense)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return transaction_service.get_transactions(
        current_user.id, start_date, end_date, type, category, page, limit
    )

@router.get("/summary/category", response_model=list[TransactionSummary])
def get_category_summary(
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
    type: Optional[str] = Query(None, description="Filter by type (income/expense)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return transaction_service.get_category_summary(
        current_user.id, start_date, end_date, type
    )

@router.get("/summary/date", response_model=list[DateSummary])
def get_date_summary(
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
    type: Optional[str] = Query(None, description="Filter by type (income/expense)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return transaction_service.get_date_summary(
        current_user.id, start_date, end_date, type
    )