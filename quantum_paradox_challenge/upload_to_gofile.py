#!/usr/bin/env python3
"""
Script to upload the Quantum Paradox Challenge to gofile.io
"""

import requests
import os
import sys

def upload_to_gofile(file_path):
    """Upload file to gofile.io"""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found!")
        return None
    
    print(f"Uploading {file_path} to gofile.io...")
    
    # Get upload server
    try:
        response = requests.get("https://api.gofile.io/getServer")
        if response.status_code == 200:
            server = response.json()["data"]["server"]
            print(f"Using server: {server}")
        else:
            print("Error getting server from gofile.io")
            return None
    except Exception as e:
        print(f"Error getting server: {e}")
        return None
    
    # Upload file
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            upload_url = f"https://{server}.gofile.io/uploadFile"
            response = requests.post(upload_url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "ok":
                    download_url = result["data"]["downloadPage"]
                    file_id = result["data"]["fileId"]
                    print(f"Upload successful!")
                    print(f"File ID: {file_id}")
                    print(f"Download URL: {download_url}")
                    return download_url
                else:
                    print(f"Upload failed: {result}")
                    return None
            else:
                print(f"Upload failed with status code: {response.status_code}")
                return None
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def main():
    """Main function"""
    file_path = "/workspace/quantum_paradox_challenge/quantum_paradox_challenge_insane.tar.gz"
    
    if not os.path.exists(file_path):
        print(f"Error: Challenge file not found at {file_path}")
        print("Please make sure the challenge has been built successfully.")
        return
    
    print("=== Quantum Paradox Challenge Upload ===")
    print("Uploading challenge to gofile.io...")
    
    download_url = upload_to_gofile(file_path)
    
    if download_url:
        print("\n=== Upload Successful ===")
        print(f"Challenge URL: {download_url}")
        print("\nChallenge Details:")
        print("- Name: Quantum Paradox")
        print("- Difficulty: INSANE")
        print("- Type: Reverse Engineering")
        print("- Expected Time: 2+ hours")
        print("- Real Flag: HTB{qu4ntum_paradox_solved_2024_real_flag}")
        print("\nThe challenge is ready for distribution!")
    else:
        print("\n=== Upload Failed ===")
        print("Please try again or use an alternative method.")

if __name__ == "__main__":
    main()