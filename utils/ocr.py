"""
OCR module - extracts text from images and scanned documents using EasyOCR
"""
import os
import tempfile
import re
import cv2
import numpy as np
from PIL import Image

def perform_ocr(file_path):
    """
    Extracts text from images and scanned documents using OCR
    
    Args:
        file_path (str): Path to the image or PDF file
        
    Returns:
        str: Extracted text
    """
    # Check file existence
    if not os.path.exists(file_path):
        return "File not found"
    
    file_ext = os.path.splitext(file_path)[-1].lower()
    
    try:
        # Import easyocr here so the module can still be imported
        # even if easyocr isn't installed yet
        import easyocr
        
        # Create a reader instance (first time will download language models)
        reader = easyocr.Reader(['en'])
        
        # For PDFs, we would need to convert to images first
        if file_ext == '.pdf':
            try:
                # Try to use pdf2image if available
                from pdf2image import convert_from_path
                
                # Convert first page of PDF to image
                pages = convert_from_path(file_path, first_page=1, last_page=1)
                if not pages:
                    return "Failed to extract image from PDF"
                
                # Save first page to temp file
                temp_img_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
                pages[0].save(temp_img_path, 'PNG')
                
                # Use the temp image for OCR
                image_path = temp_img_path
            except ImportError:
                return "PDF processing requires pdf2image library. Please install it with: pip install pdf2image"
        else:
            # Use the original file path for image files
            image_path = file_path
        
        # Preprocess the image to enhance text readability
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to handle variations in brightness
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Additional preprocessing for better results
        # Noise removal
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        # Save processed image to a temporary file
        temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        cv2.imwrite(temp_path, denoised)
        
        # Perform OCR
        results = reader.readtext(temp_path, detail=0, paragraph=True)
        
        # Clean up temporary files
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        
        if file_ext == '.pdf' and 'temp_img_path' in locals():
            if os.path.exists(temp_img_path):
                os.unlink(temp_img_path)
        
        # Combine results into a single string
        text = '\n'.join(results)
        
        # Post-process the text to fix common OCR issues
        text = post_process_text(text)
        
        return text
    
    except ImportError:
        return "EasyOCR is not installed. Please install it with: pip install easyocr"
    except Exception as e:
        return f"OCR processing error: {str(e)}"

def post_process_text(text):
    """
    Clean up the OCR output to make it more usable for term sheets
    """
    # Replace multiple newlines with a single one
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Fix common OCR errors in term sheets
    text = text.replace('l.', '1.')  # Replace lowercase L with number 1
    text = text.replace('S.', '$.')  # Replace S with dollar sign
    text = text.replace('S ', '$ ')  # Replace S with dollar sign
    
    # Fix spacing issues
    text = re.sub(r'(\d),(\d)', r'\1,\2', text)  # Fix comma spacing in numbers
    
    # Ensure "TERM SHEET" appears at the top if it's likely a term sheet
    if 'term sheet' in text.lower() and not text.strip().lower().startswith('term sheet'):
        # Find "TERM SHEET" (case insensitive) and move it to the top
        pattern = re.compile(r'term\s+sheet', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            term_sheet_text = text[match.start():match.end()]
            # Remove the original occurrence
            text = text[:match.start()] + text[match.end():]
            # Add it to the top
            text = term_sheet_text.upper() + '\n' + text.strip()
    
    return text