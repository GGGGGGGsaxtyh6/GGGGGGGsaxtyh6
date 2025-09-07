#!/usr/bin/env python3
"""
Final CAPTCHA Solver for Root-Me Challenge
Handles authentication and solves CAPTCHA in less than 3 seconds
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
        # Set user agent to avoid detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def check_authentication(self):
        """Check if we can access the challenge"""
        try:
            response = self.session.get(self.url)
            print(f"Response status: {response.status_code}")
            
            if "not authorized" in response.text.lower():
                print("Authentication required. Please authenticate on https://www.root-me.org/ first.")
                return False
            
            if "captcha" in response.text.lower() or "data:image" in response.text:
                print("CAPTCHA challenge found!")
                return True
                
            print("Unexpected response. Full response:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            return False
            
        except Exception as e:
            print(f"Error checking authentication: {e}")
            return False
    
    def get_captcha_image(self):
        """Get the CAPTCHA image from the challenge page"""
        try:
            response = self.session.get(self.url)
            response.raise_for_status()
            html = response.text
            
            print("Looking for CAPTCHA image in HTML...")
            
            # Look for base64 encoded image with various patterns
            patterns = [
                r'data:image/png;base64,(.*?)"',
                r'data:image/jpeg;base64,(.*?)"',
                r'data:image/gif;base64,(.*?)"',
                r'data:image/jpg;base64,(.*?)"',
                r'<img[^>]*src="data:image/[^;]+;base64,([^"]+)"',
                r'base64,([A-Za-z0-9+/=]+)'
            ]
            
            image_data = None
            for pattern in patterns:
                matches = re.findall(pattern, html)
                for match in matches:
                    try:
                        # Try to decode the base64 data
                        decoded = base64.b64decode(match)
                        # Check if it looks like an image (PNG, JPEG, GIF headers)
                        if (decoded.startswith(b'\x89PNG') or 
                            decoded.startswith(b'\xff\xd8\xff') or 
                            decoded.startswith(b'GIF8')):
                            image_data = decoded
                            print(f"Found image with pattern: {pattern}")
                            break
                    except:
                        continue
                if image_data:
                    break
            
            if not image_data:
                print("No valid CAPTCHA image found")
                # Save HTML for debugging
                with open('debug.html', 'w') as f:
                    f.write(html)
                print("HTML saved to debug.html for inspection")
                return None
                
            return image_data
            
        except Exception as e:
            print(f"Error getting CAPTCHA image: {e}")
            return None
    
    def preprocess_image(self, image_data):
        """Preprocess the image for better OCR recognition"""
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(image_data))
            
            print(f"Original image size: {image.size}, mode: {image.mode}")
            
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Resize image for better OCR (make it larger)
            width, height = image.size
            new_size = (width * 4, height * 4)  # Make it 4x larger
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Apply some image enhancement
            from PIL import ImageEnhance
            
            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Save processed image for debugging
            image.save('captcha_processed.png')
            print("Processed image saved as captcha_processed.png")
            
            return image
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def solve_with_tesseract(self, image):
        """Solve CAPTCHA using Tesseract OCR with multiple configurations"""
        try:
            # Try different configurations
            configs = [
                r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                r'--oem 3 --psm 8',
                r'--oem 3 --psm 7',
                r'--oem 3 --psm 6'
            ]
            
            best_result = ""
            best_confidence = 0
            
            for config in configs:
                try:
                    # Extract text
                    text = pytesseract.image_to_string(image, config=config)
                    
                    # Clean up the text
                    clean_text = re.sub(r'[^a-zA-Z0-9]', '', text.strip())
                    
                    if len(clean_text) > 0:
                        print(f"Tesseract config '{config[:30]}...': '{clean_text}'")
                        
                        # Simple confidence check (longer text is usually better)
                        if len(clean_text) > len(best_result):
                            best_result = clean_text
                            
                except Exception as e:
                    print(f"Error with config {config}: {e}")
                    continue
            
            if best_result:
                print(f"Best Tesseract result: '{best_result}'")
                return best_result
            else:
                print("No valid text found with Tesseract")
                return None
            
        except Exception as e:
            print(f"Error with Tesseract: {e}")
            return None
    
    def solve_with_gocr(self, image_data):
        """Solve CAPTCHA using gocr as backup"""
        try:
            # Save image to file
            with open('captcha_gocr.png', 'wb') as f:
                f.write(image_data)
            
            # Try different gocr options
            gocr_options = [
                ['gocr', '-C', '0-9A-Za-z', 'captcha_gocr.png'],
                ['gocr', '-C', '0-9A-Za-z', '-d', '2', 'captcha_gocr.png'],
                ['gocr', '-C', '0-9A-Za-z', '-d', '1', 'captcha_gocr.png'],
                ['gocr', 'captcha_gocr.png']
            ]
            
            for options in gocr_options:
                try:
                    result = subprocess.run(options, capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0:
                        text = result.stdout.strip()
                        # Clean up the text
                        clean_text = re.sub(r'[^a-zA-Z0-9]', '', text)
                        if clean_text:
                            print(f"GOCR result with {options}: '{clean_text}'")
                            return clean_text
                    else:
                        print(f"GOCR error with {options}: {result.stderr}")
                        
                except Exception as e:
                    print(f"Error with GOCR options {options}: {e}")
                    continue
            
            print("No valid text found with GOCR")
            return None
                
        except Exception as e:
            print(f"Error with GOCR: {e}")
            return None
    
    def submit_solution(self, captcha_text):
        """Submit the CAPTCHA solution"""
        try:
            print(f"Submitting solution: '{captcha_text}'")
            data = {'cametu': captcha_text}
            response = self.session.post(self.url, data=data)
            
            print(f"Response status: {response.status_code}")
            
            # Check for success indicators
            response_text = response.text.lower()
            if any(word in response_text for word in ['felicitaciones', 'congratulations', 'success', 'valid']):
                print("SUCCESS! CAPTCHA solved!")
                return True
            elif 'password' in response_text:
                # Look for password in response
                password_match = re.search(r'password[:\s]+([a-zA-Z0-9_]+)', response.text, re.IGNORECASE)
                if password_match:
                    print(f"Password found: {password_match.group(1)}")
                    return True
            
            # Save response for debugging
            with open('response.html', 'w') as f:
                f.write(response.text)
            print("Response saved to response.html for inspection")
            print("CAPTCHA not solved, trying again...")
            return False
            
        except Exception as e:
            print(f"Error submitting solution: {e}")
            return False
    
    def solve_captcha(self):
        """Main method to solve the CAPTCHA"""
        start_time = time.time()
        
        print("Starting CAPTCHA solving process...")
        
        # Check authentication first
        if not self.check_authentication():
            return False
        
        # Get CAPTCHA image
        image_data = self.get_captcha_image()
        if not image_data:
            print("Failed to get CAPTCHA image")
            return False
        
        # Save original image for debugging
        with open('captcha_original.png', 'wb') as f:
            f.write(image_data)
        print("Original image saved as captcha_original.png")
        
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
    print("CAPTCHA Solver for Root-Me Challenge")
    print("=" * 50)
    
    solver = CaptchaSolver()
    
    # Try multiple times if needed
    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}/{max_attempts}")
        if solver.solve_captcha():
            break
        if attempt < max_attempts - 1:
            print("Waiting 2 seconds before retry...")
            time.sleep(2)

if __name__ == "__main__":
    main()