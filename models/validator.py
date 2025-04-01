"""
Validation module - validates extracted term sheet data
"""
import re
import difflib
from datetime import datetime

def validate_term_sheet(extracted_data, reference_template=None):
    """
    Validates the extracted term sheet data against rules and reference template
    
    Args:
        extracted_data (dict): Extracted data from the term sheet
        reference_template (str, optional): Reference template text
        
    Returns:
        dict: Validation results
    """
    validation_results = {
        'status': 'PASS',  # Overall status (PASS/FAIL)
        'errors': [],      # List of validation errors
        'warnings': [],    # List of validation warnings
        'missing_fields': [],  # List of required fields that are missing
        'reference_comparison': None  # Comparison with reference template
    }
    
    # Validate required fields
    required_fields = [
        ('parties.issuer', 'Issuer/Company name'),
        ('parties.investor', 'Investor name'),
        ('financial_terms.amount', 'Investment amount')
    ]
    
    for field_path, field_name in required_fields:
        # Navigate the nested dictionary
        parts = field_path.split('.')
        value = extracted_data
        for part in parts:
            value = value.get(part, None) if isinstance(value, dict) else None
            if value is None:
                break
        
        if value is None or value == '':
            validation_results['missing_fields'].append(field_name)
            validation_results['errors'].append(f"Missing required field: {field_name}")
            validation_results['status'] = 'FAIL'
    
    # Validate dates if present
    for date_key, date_value in extracted_data.get('dates', {}).items():
        if date_value:
            try:
                # Try to parse various date formats
                formats = ['%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y', 
                           '%d %b %Y', '%d %B %Y', '%b %d, %Y', '%B %d, %Y']
                parsed = False
                for fmt in formats:
                    try:
                        datetime.strptime(date_value, fmt)
                        parsed = True
                        break
                    except ValueError:
                        continue
                
                if not parsed:
                    validation_results['warnings'].append(f"Date format for {date_key} may be invalid: {date_value}")
            except Exception:
                validation_results['warnings'].append(f"Could not validate date format for {date_key}: {date_value}")
    
    # Validate financial terms
    amount = extracted_data.get('financial_terms', {}).get('amount')
    if amount:
        # Remove currency symbol, commas, and convert million/billion abbreviations
        cleaned_amount = re.sub(r'[$€£¥,]', '', amount)
        cleaned_amount = cleaned_amount.lower()
        
        if 'million' in cleaned_amount or 'm' in cleaned_amount:
            cleaned_amount = cleaned_amount.replace('million', '').replace('m', '').strip()
            try:
                numeric_amount = float(cleaned_amount) * 1000000
            except ValueError:
                validation_results['warnings'].append(f"Could not parse amount value: {amount}")
        elif 'billion' in cleaned_amount or 'b' in cleaned_amount:
            cleaned_amount = cleaned_amount.replace('billion', '').replace('b', '').strip()
            try:
                numeric_amount = float(cleaned_amount) * 1000000000
            except ValueError:
                validation_results['warnings'].append(f"Could not parse amount value: {amount}")
        else:
            try:
                numeric_amount = float(cleaned_amount)
            except ValueError:
                validation_results['warnings'].append(f"Could not parse amount value: {amount}")
    
    # Compare with reference template if provided
    if reference_template:
        similarity = difflib.SequenceMatcher(None, 
                                           str(extracted_data).lower(), 
                                           reference_template.lower()).ratio()
        
        validation_results['reference_comparison'] = {
            'similarity_score': round(similarity * 100, 2),
            'compliance': 'High' if similarity > 0.8 else 'Medium' if similarity > 0.5 else 'Low'
        }
        
        if similarity < 0.5:
            validation_results['warnings'].append("Low similarity to reference template")
    
    # Count errors and warnings
    validation_results['error_count'] = len(validation_results['errors'])
    validation_results['warning_count'] = len(validation_results['warnings'])
    
    # Update overall status if there are errors
    if validation_results['errors']:
        validation_results['status'] = 'FAIL'
    
    return validation_results