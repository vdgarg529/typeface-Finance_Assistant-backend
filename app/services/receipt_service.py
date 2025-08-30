 
from sqlalchemy.orm import Session
from app.models.receipt import Receipt
from app.models.transaction import Transaction, TransactionType
from app.utils.ocr_parser import extract_text_from_image, parse_receipt_text
from app.utils.pdf_parser import extract_text_from_pdf, parse_transactions_from_text
import re
from datetime import datetime

class ReceiptService:
    def __init__(self, db: Session):
        self.db = db
    
    def process_receipt(self, user_id: int, file_path: str, file_extension: str) -> Receipt:
        
        if file_extension.lower() in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
            text = extract_text_from_image(file_path)
        elif file_extension.lower() == 'pdf':
            text = extract_text_from_pdf(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        
        receipt = Receipt(
            user_id=user_id,
            file_path=file_path,
            parsed_text=text
        )
        self.db.add(receipt)
        self.db.commit()
        self.db.refresh(receipt)
        
        
        try:
            transaction_data = parse_receipt_text(text)
            if transaction_data:
                transaction = Transaction(
                    user_id=user_id,
                    amount=transaction_data['amount'],
                    type=TransactionType.EXPENSE,
                    category=transaction_data.get('category', 'Other'),
                    description=transaction_data.get('description', 'From receipt'),
                    date=transaction_data.get('date', datetime.now().date())
                )
                self.db.add(transaction)
                self.db.commit()
        except Exception as e:
            
            pass
        
        return receipt
    
    def process_pdf_transactions(self, user_id: int, file_path: str) -> list[Receipt]:
        
        text = extract_text_from_pdf(file_path)
        
        
        receipt = Receipt(
            user_id=user_id,
            file_path=file_path,
            parsed_text=text[:1000]  
        )
        self.db.add(receipt)
        self.db.commit()
        self.db.refresh(receipt)
        
        
        transactions = parse_transactions_from_text(text)
        
        
        created_transactions = []
        for transaction_data in transactions:
            transaction = Transaction(
                user_id=user_id,
                amount=transaction_data['amount'],
                type=TransactionType(transaction_data['type']),
                category=transaction_data.get('category', 'Other'),
                description=transaction_data.get('description', 'From PDF statement'),
                date=transaction_data.get('date', datetime.now().date())
            )
            self.db.add(transaction)
            created_transactions.append(transaction)
        
        self.db.commit()
        
        return [receipt]  