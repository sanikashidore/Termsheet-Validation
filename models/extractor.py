"""
Data extraction module - extracts structured data from term sheets
"""
import re
from datetime import datetime

def extract_data(text):
    """
    Extracts structured data from term sheet text
    
    Args:
        text (str): The term sheet text
        
    Returns:
        dict: Extracted data fields
    """
    # Initialize extracted data structure
    extracted_data = {
        'parties': {
            'issuer': None,
            'investor': None,
        },
        'dates': {
            'effective_date': None,
            'expiry_date': None,
            'closing_date': None,
        },
        'financial_terms': {
            'amount': None,
            'currency': None,
            'valuation': None,
            'share_price': None,
        },
        'legal_terms': {
            'governing_law': None,
            'jurisdiction': None,
            'confidentiality': None,
        },
        'raw_sections': {}
    }
    
    # Extract parties
    issuer_match = re.search(r'(?:issuer|company|seller)[:\s]+([^,\n]+)', text, re.IGNORECASE)
    if issuer_match:
        extracted_data['parties']['issuer'] = issuer_match.group(1).strip()
    
    investor_match = re.search(r'(?:investor|purchaser|buyer)[:\s]+([^,\n]+)', text, re.IGNORECASE)
    if investor_match:
        extracted_data['parties']['investor'] = investor_match.group(1).strip()
    
    # Extract dates
    # Looking for dates in common formats
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})'
    
    effective_match = re.search(r'(?:effective\s+date|date\s+of\s+agreement)[:\s]+' + date_pattern, text, re.IGNORECASE)
    if effective_match:
        extracted_data['dates']['effective_date'] = effective_match.group(1).strip()
    
    expiry_match = re.search(r'(?:expiry\s+date|expiration\s+date|termination\s+date)[:\s]+' + date_pattern, text, re.IGNORECASE)
    if expiry_match:
        extracted_data['dates']['expiry_date'] = expiry_match.group(1).strip()
    
    closing_match = re.search(r'(?:closing\s+date)[:\s]+' + date_pattern, text, re.IGNORECASE)
    if closing_match:
        extracted_data['dates']['closing_date'] = closing_match.group(1).strip()
    
    # Extract financial terms
    # Find currency symbols and amounts
    amount_match = re.search(r'(?:amount|principal|investment)[:\s]+([$€£¥]?\s*\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:million|m|billion|b))?)', text, re.IGNORECASE)
    if amount_match:
        amount_str = amount_match.group(1).strip()
        # Try to separate currency symbol from amount
        currency_match = re.search(r'([$€£¥])', amount_str)
        if currency_match:
            extracted_data['financial_terms']['currency'] = currency_match.group(1)
            amount_str = amount_str.replace(currency_match.group(1), '').strip()
        
        extracted_data['financial_terms']['amount'] = amount_str
    
    valuation_match = re.search(r'(?:valuation|company\s+valuation|pre-money)[:\s]+([$€£¥]?\s*\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:million|m|billion|b))?)', text, re.IGNORECASE)
    if valuation_match:
        extracted_data['financial_terms']['valuation'] = valuation_match.group(1).strip()
    
    share_price_match = re.search(r'(?:share\s+price|price\s+per\s+share)[:\s]+([$€£¥]?\s*\d+(?:,\d{3})*(?:\.\d+)?)', text, re.IGNORECASE)
    if share_price_match:
        extracted_data['financial_terms']['share_price'] = share_price_match.group(1).strip()
    
    # Extract legal terms
    law_match = re.search(r'(?:governing\s+law|law)[:\s]+([^,\n.]+)', text, re.IGNORECASE)
    if law_match:
        extracted_data['legal_terms']['governing_law'] = law_match.group(1).strip()
    
    jurisdiction_match = re.search(r'(?:jurisdiction)[:\s]+([^,\n.]+)', text, re.IGNORECASE)
    if jurisdiction_match:
        extracted_data['legal_terms']['jurisdiction'] = jurisdiction_match.group(1).strip()
    
    # Extract document sections - simple section detection
    section_pattern = r'(?:^|\n)([A-Z][A-Z\s]+)(?::|\.|\n)'
    sections = re.finditer(section_pattern, text)
    current_section = None
    section_starts = []
    
    for match in sections:
        section_name = match.group(1).strip()
        start_pos = match.start()
        if current_section:
            # Save the previous section with text up to this point
            section_text = text[section_starts[-1]:start_pos].strip()
            extracted_data['raw_sections'][current_section] = section_text
        
        current_section = section_name
        section_starts.append(start_pos)
    
    # Don't forget the last section
    if current_section and section_starts:
        section_text = text[section_starts[-1]:].strip()
        extracted_data['raw_sections'][current_section] = section_text
    
    return extracted_data