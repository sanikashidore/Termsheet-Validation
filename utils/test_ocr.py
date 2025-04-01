"""
Test script for OCR module
"""
import sys
import os
from ocr import perform_ocr

def test_ocr():
    if len(sys.argv) < 2:
        print("Usage: python test_ocr.py <path_to_image>")
        return
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found")
        return
    
    print(f"Processing: {image_path}")
    print("-" * 50)
    
    # Run OCR
    print("Performing OCR (first run may take time to download models)...")
    text = perform_ocr(image_path)
    
    print("\nExtracted Text:")
    print("-" * 50)
    print(text)
    print("-" * 50)
    
    # Basic verification
    keywords = ['TERM SHEET', 'Investment', 'Valuation', 'Investor', 'Company']
    found_keywords = [keyword for keyword in keywords if keyword.lower() in text.lower()]
    
    print(f"\nFound {len(found_keywords)} out of {len(keywords)} keywords:")
    for keyword in keywords:
        present = "✓" if keyword.lower() in text.lower() else "✗"
        print(f"  {present} {keyword}")

if __name__ == "__main__":
    test_ocr()