 
# Pytesseract Based

# import pytesseract
# from PIL import Image
# import re
# from datetime import datetime

# def extract_text_from_image(image_path: str) -> str:
#     """Extract text from an image using OCR"""
#     try:
#         image = Image.open(image_path)
#         text = pytesseract.image_to_string(image)
#         return text
#     except Exception as e:
#         raise Exception(f"Failed to extract text from image: {str(e)}")

# def parse_receipt_text(text: str) -> dict:
#     """Parse receipt text to extract transaction information"""
    
#     amount_pattern = r'\$?\d+\.\d{2}'
#     date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
    
    
#     amounts = re.findall(amount_pattern, text)
#     amounts = [float(amount.replace('$', '')) for amount in amounts]
    
#     if not amounts:
#         return None
    
#     total_amount = max(amounts)
    
#     dates = re.findall(date_pattern, text)
#     transaction_date = None
#     if dates:
#         try:
#             transaction_date = datetime.strptime(dates[0], '%m/%d/%Y').date()
#         except:
#             try:
#                 transaction_date = datetime.strptime(dates[0], '%m-%d-%Y').date()
#             except:
#                 pass
    
    
#     category = "Other"
#     category_keywords = {
#         "Food": ["restaurant", "cafe", "food", "groceries", "supermarket", "dining"],
#         "Transport": ["gas", "fuel", "taxi", "uber", "lyft", "transport", "parking"],
#         "Shopping": ["store", "shop", "mall", "clothing", "electronics", "amazon"],
#         "Entertainment": ["movie", "cinema", "concert", "game", "entertainment"],
#         "Utilities": ["electricity", "water", "gas", "internet", "phone", "utility"],
#     }
    
#     text_lower = text.lower()
#     for cat, keywords in category_keywords.items():
#         if any(keyword in text_lower for keyword in keywords):
#             category = cat
#             break
    
#     return {
#         "amount": total_amount,
#         "date": transaction_date,
#         "category": category,
#         "description": "From receipt scan"
#     }


# EasyOCR Based

import easyocr
from PIL import Image
import re
from datetime import datetime
import os


try:
    reader = easyocr.Reader(['en'])
    OCR_AVAILABLE = True
except Exception as e:
    print(f"EasyOCR initialization failed: {e}")
    OCR_AVAILABLE = False
    reader = None

def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image using EasyOCR"""
    try:
        if not OCR_AVAILABLE:
            raise Exception("EasyOCR is not available. Please check the installation.")
        
        
        results = reader.readtext(image_path)
        
        
        text = " ".join([result[1] for result in results])
        
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from image: {str(e)}")


def parse_receipt_text(text: str) -> dict:
    """Parse receipt text to extract transaction information"""
    
    amount_pattern = r'\$?\d+\.\d{2}'
    date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
    
    
    amounts = re.findall(amount_pattern, text)
    amounts = [float(amount.replace('$', '').replace(',', '')) for amount in amounts]
    
    if not amounts:
        return None
    
    total_amount = max(amounts)
    
    
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
       
        transaction_date = datetime.now().date()
    
   
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