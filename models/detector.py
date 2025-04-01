"""
Term sheet detection module - determines if a document is likely a term sheet
"""
import re

# List of common term sheet keywords and phrases
TERM_SHEET_INDICATORS = [
    'term sheet', 'termsheet', 'terms and conditions', 
    'binding agreement', 'non-binding agreement',
    'investment terms', 'financing terms',
    'purchase price', 'valuation', 'pre-money valuation',
    'shares', 'equity', 'preferred stock', 'series',
    'closing conditions', 'representations', 'warranties',
    'governing law', 'confidentiality', 'exclusivity',
    'board of directors', 'board composition',
    'liquidation preference', 'dividends',
    'maturity date', 'interest rate', 'principal amount'
]

def is_term_sheet(text):
    """
    Determines if the given text is likely a term sheet based on keyword presence
    
    Args:
        text (str): The document text to analyze
        
    Returns:
        bool: True if the document is likely a term sheet, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Count how many term sheet indicators are present
    indicator_count = sum(1 for indicator in TERM_SHEET_INDICATORS if indicator in text_lower)
    
    # Check for common term sheet headers
    has_term_sheet_header = bool(re.search(r'\b(term\s*sheet|termsheet|term\s*of\s*agreement)\b', text_lower))
    
    # A document is considered a term sheet if it has either:
    # 1. A clear term sheet header, or
    # 2. Multiple term sheet indicators (at least 3)
    return has_term_sheet_header or indicator_count >= 3