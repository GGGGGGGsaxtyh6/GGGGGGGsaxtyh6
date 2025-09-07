#!/usr/bin/env python3
"""
Simple CAPTCHA test script to verify our setup works
"""

import requests
import base64
import re
import subprocess
import time
from PIL import Image
import pytesseract
import io

def test_tesseract():
    """Test if tesseract is working"""
    try:
        # Create a simple test image with text
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a white image
        img = Image.new('RGB', (200, 50), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Draw some text
        draw.text((10, 15), "TEST123", fill='black', font=font)
        img.save('test_image.png')
        
        # Test OCR
        text = pytesseract.image_to_string(img)
        print(f"Tesseract test result: '{text.strip()}'")
        return True
        
    except Exception as e:
        print(f"Tesseract test failed: {e}")
        return False

def test_gocr():
    """Test if gocr is working"""
    try:
        # Use the test image we created
        result = subprocess.run(['gocr', 'test_image.png'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print(f"GOCR test result: '{result.stdout.strip()}'")
            return True
        else:
            print(f"GOCR test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"GOCR test failed: {e}")
        return False

def main():
    print("Testing OCR tools...")
    
    print("\n1. Testing Tesseract:")
    tesseract_ok = test_tesseract()
    
    print("\n2. Testing GOCR:")
    gocr_ok = test_gocr()
    
    print(f"\nResults:")
    print(f"Tesseract: {'OK' if tesseract_ok else 'FAILED'}")
    print(f"GOCR: {'OK' if gocr_ok else 'FAILED'}")
    
    if tesseract_ok or gocr_ok:
        print("\nOCR tools are ready for CAPTCHA solving!")
    else:
        print("\nOCR tools need configuration!")

if __name__ == "__main__":
    main()