#!/usr/bin/env python3
import json, subprocess, os, sys

if len(sys.argv) < 3:
    print("Uso: python3 enviar_flag.py <challenge_id> <flag>")
    sys.exit(1)

token = open('.env').read().split('HTB_TOKEN=')[1].split('\n')[0]
env = {'HTB_TOKEN': token}

p = subprocess.Popen(['./htb-mcp-server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=env, text=True)
p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
p.stdin.flush()
p.stdout.readline()

challenge_id = sys.argv[1]
flag = sys.argv[2]
p.stdin.write(f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"submit_challenge_flag","arguments":{{"challenge_id":{challenge_id},"flag":"{flag}"}}}}}}\n')
p.stdin.flush()
print(p.stdout.readline())
p.terminate()
