 
# Pytesseract Based
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
    
    # Set the path to tesseract executable (for Windows)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except ImportError:
    OCR_AVAILABLE = False
    print("pytesseract not available. OCR functionality disabled.")

import re
from datetime import datetime
import os

def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image using pytesseract"""
    try:
        if not OCR_AVAILABLE:
            raise Exception("pytesseract is not available. Please check the installation.")
        
        # Open the image
        image = Image.open(image_path)
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from image: {str(e)}")

def parse_receipt_text(text: str) -> dict:
    """Parse receipt text to extract transaction information"""
    # Simple regex patterns to extract information
    amount_pattern = r'\$?\d+\.\d{2}'
    date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
    
    # Find amounts (take the largest one as total)
    amounts = re.findall(amount_pattern, text)
    amounts = [float(amount.replace('$', '').replace(',', '')) for amount in amounts]
    
    if not amounts:
        return None
    
    total_amount = max(amounts)
    
    # Find date
    dates = re.findall(date_pattern, text)
    transaction_date = None
    if dates:
        try:
            transaction_date = datetime.strptime(dates[0], '%m/%d/%Y').date()
        except:
            try:
                transaction_date = datetime.strptime(dates[0], '%m-%d-%Y').date()
            except:
                # If we can't parse the date, use today's date
                transaction_date = datetime.now().date()
    else:
        # If no date found, use today's date
        transaction_date = datetime.now().date()
    
    # Try to identify category based on keywords
    category = "Other"
    category_keywords = {
        "Food": ["restaurant", "cafe", "food", "groceries", "supermarket", "dining"],
        "Transport": ["gas", "fuel", "taxi", "uber", "lyft", "transport", "parking"],
        "Shopping": ["store", "shop", "mall", "clothing", "electronics", "amazon"],
        "Entertainment": ["movie", "cinema", "concert", "game", "entertainment"],
        "Utilities": ["electricity", "water", "gas", "internet", "phone", "utility"],
    }
    
    text_lower = text.lower()
    for cat, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            category = cat
            break
    
    return {
        "amount": total_amount,
        "date": transaction_date,
        "category": category,
        "description": "From receipt scan"
    }
