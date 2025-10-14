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

def main():
    host,port = 'e9ea7c6b519c45be.247ctf.com', 50188
    s = socket.create_connection((host,port), timeout=6)
    print(recv_until(s, b"Enter command:").decode(errors='replace'))

    def make(kind: str, data: bytes):
        sendline(s, kind)
        recv_until(s, f"Enter the size of your {kind} note:".encode())
        sendline(s, str(len(data)))
        recv_until(s, f"Enter {kind} note data:".encode())
        s.sendall(data)
        # wait prompt
        recv_until(s, b"Enter command:")

    msg = b"MATCH_ME\n"  # include newline in payload
    make('small', msg)
    make('medium', msg)
    make('large', msg)

    sendline(s, 'print')
    out = recv_until(s, b"Enter command:")
    print(out.decode(errors='replace'))

    sendline(s, 'flag')
    flag = recv_until(s, b"Enter command:")
    print(flag.decode(errors='replace'))

if __name__=='__main__':
    main()
