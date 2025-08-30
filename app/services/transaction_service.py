 
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from datetime import date
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionSummary, DateSummary, PaginatedTransactions

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_transaction(self, user_id: int, transaction_data: TransactionCreate) -> Transaction:
        transaction = Transaction(
            user_id=user_id,
            amount=transaction_data.amount,
            type=TransactionType(transaction_data.type),
            category=transaction_data.category,
            description=transaction_data.description,
            date=transaction_data.date
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def get_transactions(
        self,
        user_id: int,
        start_date: Optional[date],
        end_date: Optional[date],
        type: Optional[str],
        category: Optional[str],
        page: int,
        limit: int
    ) -> PaginatedTransactions:
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if type:
            query = query.filter(Transaction.type == TransactionType(type))
        if category:
            query = query.filter(Transaction.category == category)
        
        
        total = query.count()
        
        
        transactions = query.order_by(Transaction.date.desc()).offset((page - 1) * limit).limit(limit).all()
        
        
        pages = (total + limit - 1) // limit
        
        return PaginatedTransactions(
            items=transactions,
            total=total,
            page=page,
            pages=pages
        )
    
    def get_category_summary(
        self,
        user_id: int,
        start_date: Optional[date],
        end_date: Optional[date],
        type: Optional[str]
    ) -> list[TransactionSummary]:
        query = self.db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("total_amount")
        ).filter(Transaction.user_id == user_id)
        
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if type:
            query = query.filter(Transaction.type == TransactionType(type))
        
        results = query.group_by(Transaction.category).all()
        
        return [
            TransactionSummary(category=row.category, total_amount=row.total_amount)
            for row in results
        ]
    
    def get_date_summary(
        self,
        user_id: int,
        start_date: Optional[date],
        end_date: Optional[date],
        type: Optional[str]
    ) -> list[DateSummary]:
        query = self.db.query(
            Transaction.date,
            func.sum(Transaction.amount).label("total_amount")
        ).filter(Transaction.user_id == user_id)
        
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if type:
            query = query.filter(Transaction.type == TransactionType(type))
        
        results = query.group_by(Transaction.date).order_by(Transaction.date).all()
        
        return [
            DateSummary(date=row.date, total_amount=row.total_amount)
            for row in results
        ]