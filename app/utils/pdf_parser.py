 
import pdfplumber
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def parse_transactions_from_text(text: str) -> list[dict]:
    """Parse transaction data from bank statement text"""
    transactions = []
    
    transaction_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4})\s+(.*?)\s+(-?\$?\d+\.\d{2})'
    
    matches = re.findall(transaction_pattern, text)
    
    for match in matches:
        date_str, description, amount_str = match
        
        try:
            
            transaction_date = datetime.strptime(date_str, '%m/%d/%Y').date()
            
            
            amount = float(amount_str.replace('$', '').replace(',', ''))
            transaction_type = "expense" if amount < 0 else "income"
            amount = abs(amount)
            
            
            category = "Other"
            description_lower = description.lower()
            
            if any(word in description_lower for word in ['restaurant', 'cafe', 'food', 'groceries']):
                category = "Food"
            elif any(word in description_lower for word in ['gas', 'fuel', 'taxi', 'uber', 'transport']):
                category = "Transport"
            elif any(word in description_lower for word in ['electricity', 'water', 'gas', 'internet', 'phone']):
                category = "Utilities"
            elif any(word in description_lower for word in ['salary', 'payment', 'deposit']):
                category = "Income"
            
            transactions.append({
                "amount": amount,
                "type": transaction_type,
                "category": category,
                "description": description.strip(),
                "date": transaction_date
            })
        except Exception as e:
            continue
    
    return transactions