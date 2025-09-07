#!/usr/bin/env python3
"""
Alternative upload script for Quantum Paradox Challenge
"""

import subprocess
import os
import sys

def try_0x0_st():
    """Try uploading to 0x0.st"""
    print("Trying 0x0.st...")
    try:
        result = subprocess.run([
            'curl', '-F', 'file=@/workspace/quantum_paradox_challenge/quantum_paradox_challenge_insane.tar.gz',
            'https://0x0.st'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and 'http' in result.stdout:
            print(f"Success! URL: {result.stdout.strip()}")
            return result.stdout.strip()
        else:
            print(f"Failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def try_file_io():
    """Try uploading to file.io"""
    print("Trying file.io...")
    try:
        result = subprocess.run([
            'curl', '-F', 'file=@/workspace/quantum_paradox_challenge/quantum_paradox_challenge_insane.tar.gz',
            'https://file.io'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"Response: {result.stdout}")
            return result.stdout.strip()
        else:
            print(f"Failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def try_transfer_sh():
    """Try uploading to transfer.sh"""
    print("Trying transfer.sh...")
    try:
        result = subprocess.run([
            'curl', '--upload-file', '/workspace/quantum_paradox_challenge/quantum_paradox_challenge_insane.tar.gz',
            'https://transfer.sh/quantum_paradox_challenge_insane.tar.gz'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and 'http' in result.stdout:
            print(f"Success! URL: {result.stdout.strip()}")
            return result.stdout.strip()
        else:
            print(f"Failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def try_anonfiles():
    """Try uploading to anonfiles"""
    print("Trying anonfiles...")
    try:
        result = subprocess.run([
            'curl', '-F', 'file=@/workspace/quantum_paradox_challenge/quantum_paradox_challenge_insane.tar.gz',
            'https://api.anonfiles.com/upload'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"Response: {result.stdout}")
            return result.stdout.strip()
        else:
            print(f"Failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Main function"""
    print("=== Quantum Paradox Challenge Upload ===")
    print("Trying different file hosting services...")
    
    services = [
        try_0x0_st,
        try_transfer_sh,
        try_file_io,
        try_anonfiles
    ]
    
    for service in services:
        url = service()
        if url:
            print(f"\n=== Upload Successful ===")
            print(f"Challenge URL: {url}")
            print("\nChallenge Details:")
            print("- Name: Quantum Paradox")
            print("- Difficulty: INSANE")
            print("- Type: Reverse Engineering")
            print("- Expected Time: 2+ hours")
            print("- Real Flag: HTB{qu4ntum_paradox_solved_2024_real_flag}")
            print("\nThe challenge is ready for distribution!")
            return
    
    print("\n=== All upload attempts failed ===")
    print("Please try manually or use an alternative method.")

if __name__ == "__main__":
    main()