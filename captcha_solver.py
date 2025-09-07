#!/usr/bin/env python3
"""
CAPTCHA Solver for Root-Me Challenge
Solves the CAPTCHA challenge in less than 3 seconds
"""

import requests
import base64
import re
import subprocess
import time
from PIL import Image
import pytesseract
import io
import os

class CaptchaSolver:
    def __init__(self):
        self.url = 'http://challenge01.root-me.org/programmation/ch8/'
        self.session = requests.Session()
        
    def get_captcha_image(self):
        """Get the CAPTCHA image from the challenge page"""
        try:
            response = self.session.get(self.url)
            response.raise_for_status()
            html = response.text
            
            # Look for base64 encoded image
            match = re.search(r'data:image/png;base64,(.*?)"', html)
            if not match:
                # Try alternative patterns
                match = re.search(r'data:image/jpeg;base64,(.*?)"', html)
                if not match:
                    match = re.search(r'data:image/gif;base64,(.*?)"', html)
            
            if not match:
                print("No CAPTCHA image found in HTML")
                return None
                
            # Decode base64 image
            image_data = base64.b64decode(match.group(1))
            return image_data
            
        except Exception as e:
            print(f"Error getting CAPTCHA image: {e}")
            return None
    
    def preprocess_image(self, image_data):
        """Preprocess the image for better OCR recognition"""
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Resize image for better OCR (make it larger)
            width, height = image.size
            new_size = (width * 3, height * 3)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save processed image for debugging
            image.save('captcha_processed.png')
            
            return image
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def solve_with_tesseract(self, image):
        """Solve CAPTCHA using Tesseract OCR"""
        try:
            # Configure tesseract for better recognition
            custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            
            # Extract text
            text = pytesseract.image_to_string(image, config=custom_config)
            
            # Clean up the text
            text = re.sub(r'[^a-zA-Z0-9]', '', text.strip())
            
            print(f"Tesseract result: '{text}'")
            return text
            
        except Exception as e:
            print(f"Error with Tesseract: {e}")
            return None
    
    def solve_with_gocr(self, image_data):
        """Solve CAPTCHA using gocr as backup"""
        try:
            # Save image to file
            with open('captcha_gocr.png', 'wb') as f:
                f.write(image_data)
            
            # Run gocr
            result = subprocess.run(['gocr', '-C', '0-9A-Za-z', 'captcha_gocr.png'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                text = result.stdout.strip()
                # Clean up the text
                text = re.sub(r'[^a-zA-Z0-9]', '', text)
                print(f"GOCR result: '{text}'")
                return text
            else:
                print(f"GOCR error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Error with GOCR: {e}")
            return None
    
    def submit_solution(self, captcha_text):
        """Submit the CAPTCHA solution"""
        try:
            data = {'cametu': captcha_text}
            response = self.session.post(self.url, data=data)
            
            print(f"Response status: {response.status_code}")
            
            # Check for success indicators
            if 'Felicitaciones' in response.text or 'Congratulations' in response.text:
                print("SUCCESS! CAPTCHA solved!")
                return True
            elif 'password' in response.text.lower():
                # Look for password in response
                password_match = re.search(r'password[:\s]+([a-zA-Z0-9_]+)', response.text, re.IGNORECASE)
                if password_match:
                    print(f"Password found: {password_match.group(1)}")
                    return True
            
            print("CAPTCHA not solved, trying again...")
            return False
            
        except Exception as e:
            print(f"Error submitting solution: {e}")
            return False
    
    def solve_captcha(self):
        """Main method to solve the CAPTCHA"""
        start_time = time.time()
        
        print("Starting CAPTCHA solving process...")
        
        # Get CAPTCHA image
        image_data = self.get_captcha_image()
        if not image_data:
            print("Failed to get CAPTCHA image")
            return False
        
        # Try Tesseract first
        processed_image = self.preprocess_image(image_data)
        if processed_image:
            captcha_text = self.solve_with_tesseract(processed_image)
            if captcha_text and len(captcha_text) > 0:
                if self.submit_solution(captcha_text):
                    elapsed = time.time() - start_time
                    print(f"Solved in {elapsed:.2f} seconds")
                    return True
        
        # Try GOCR as backup
        print("Trying GOCR as backup...")
        captcha_text = self.solve_with_gocr(image_data)
        if captcha_text and len(captcha_text) > 0:
            if self.submit_solution(captcha_text):
                elapsed = time.time() - start_time
                print(f"Solved in {elapsed:.2f} seconds")
                return True
        
        elapsed = time.time() - start_time
        print(f"Failed to solve CAPTCHA in {elapsed:.2f} seconds")
        return False

def main():
    solver = CaptchaSolver()
    
    # Try multiple times if needed
    max_attempts = 5
    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}/{max_attempts}")
        if solver.solve_captcha():
            break
        time.sleep(1)  # Wait a bit before retrying

if __name__ == "__main__":
    main()