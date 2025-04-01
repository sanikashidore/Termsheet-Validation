"""
File handling module - processes different file types
"""
import os
import re
import pandas as pd

def get_file_extension(file_path):
    """
    Gets the file extension from a file path
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File extension (without the dot)
    """
    return os.path.splitext(file_path)[1][1:].lower()

def read_file_content(file_path):
    """
    Reads and extracts text content from various file types
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Extracted text content
    """
    if not os.path.exists(file_path):
        return "File not found"
    
    file_ext = get_file_extension(file_path)
    
    try:
        # Plain text files
        if file_ext == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        # PDF files - use PyPDF2 if available
        elif file_ext == 'pdf':
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page_num in range(len(pdf_reader.pages)):
                        text += pdf_reader.pages[page_num].extract_text() + "\n"
                    return text
            except ImportError:
                return "PDF processing requires PyPDF2. Install with: pip install PyPDF2"
        
        # Word documents - use python-docx if available
        elif file_ext in ['doc', 'docx']:
            try:
                import docx
                doc = docx.Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            except ImportError:
                return "Word document processing requires python-docx. Install with: pip install python-docx"
        
        # Excel files - use pandas
        elif file_ext in ['xls', 'xlsx']:
            try:
                df = pd.read_excel(file_path)
                # Convert DataFrame to a string representation
                return df.to_string()
            except Exception as e:
                return f"Error processing Excel file: {str(e)}"
        
        # Image files - these should be handled by OCR
        elif file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
            return "Image file detected. Please use OCR option for processing."
        
        # Unsupported file type
        else:
            return f"Unsupported file type: {file_ext}"
    
    except Exception as e:
        return f"Error reading file: {str(e)}"