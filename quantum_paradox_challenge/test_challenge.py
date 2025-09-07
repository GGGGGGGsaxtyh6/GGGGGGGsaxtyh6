#!/usr/bin/env python3
"""
Test script for Quantum Paradox Challenge
This script demonstrates the fake flags and shows how the challenge works
"""

import subprocess
import sys
import os

def test_challenge():
    """Test the challenge binary"""
    print("=== Quantum Paradox Challenge Test ===")
    print("Testing the challenge binary...")
    
    # Test with different inputs
    test_inputs = [
        "test",
        "quantum_paradox_2024",
        "12345678901234567890123456789012",  # 32 chars
        "fake_key",
        "debug"
    ]
    
    for i, test_input in enumerate(test_inputs):
        print(f"\nTest {i+1}: Input = '{test_input}'")
        try:
            # Run the binary with test input
            result = subprocess.run(
                ['./quantum_paradox'],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 133:
                print("  Result: Anti-debugging triggered (INT3)")
            elif result.returncode == 1:
                print("  Result: Debugger detected")
            else:
                print(f"  Result: Exit code {result.returncode}")
                if result.stdout:
                    print(f"  Output: {result.stdout.strip()}")
                if result.stderr:
                    print(f"  Error: {result.stderr.strip()}")
                    
        except subprocess.TimeoutExpired:
            print("  Result: Timeout (binary hung)")
        except Exception as e:
            print(f"  Result: Error - {e}")

def show_fake_flags():
    """Show all the fake flags in the challenge"""
    print("\n=== Fake Flags in Challenge ===")
    print("These are the fake flags that participants might find:")
    print("(DO NOT SUBMIT THESE - THEY ARE FAKE!)")
    
    fake_flags = [
        "HTB{f4k3_fl4g_1_qu4ntum_3rr0r}",
        "HTB{f4k3_fl4g_2_paradox}",
        "HTB{qu4ntum_3nt4ngl3m3nt_s0lv3d}",
        "HTB{asm_puzzle_1_solved}",
        "HTB{crypto_analysis_complete}",
        "HTB{quantum_algorithm_solved_paradox}"
    ]
    
    for i, flag in enumerate(fake_flags, 1):
        print(f"Fake Flag {i}: {flag}")
    
    print("\n=== Real Flag ===")
    print("The real flag is: HTB{qu4ntum_paradox_solved_2024_real_flag}")
    print("This flag is hidden in the getRealFlag() function")
    print("and must be extracted through memory analysis!")

def show_challenge_info():
    """Show challenge information"""
    print("\n=== Challenge Information ===")
    print("Challenge Name: Quantum Paradox")
    print("Difficulty: INSANE")
    print("Expected Time: 2+ hours")
    print("Type: Reverse Engineering")
    print("Skills Required:")
    print("- Binary analysis")
    print("- Anti-debugging bypass")
    print("- Memory analysis")
    print("- Code obfuscation")
    print("- Assembly understanding")
    
    print("\n=== Files in Challenge ===")
    if os.path.exists('build'):
        files = os.listdir('build')
        for file in sorted(files):
            if file.endswith('.txt') or file.endswith('.json') or file.endswith('.md'):
                print(f"- {file}")
    
    print("\n=== Main Binary ===")
    if os.path.exists('build/quantum_paradox'):
        size = os.path.getsize('build/quantum_paradox')
        print(f"- quantum_paradox ({size} bytes)")
        print("- Heavily obfuscated and protected")
        print("- Anti-debugging measures enabled")
        print("- Multiple fake flags included")

def main():
    """Main function"""
    if not os.path.exists('build/quantum_paradox'):
        print("Error: Challenge binary not found!")
        print("Please run the build script first.")
        return
    
    show_challenge_info()
    show_fake_flags()
    
    print("\n=== Testing Challenge ===")
    os.chdir('build')
    test_challenge()
    
    print("\n=== Challenge Ready ===")
    print("The challenge is ready for distribution!")
    print("Package: quantum_paradox_challenge_insane.tar.gz")

if __name__ == "__main__":
    main()