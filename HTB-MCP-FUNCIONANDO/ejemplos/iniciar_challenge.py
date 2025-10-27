#!/usr/bin/env python3
import json, subprocess, os, sys

token = open('.env').read().split('HTB_TOKEN=')[1].split('\n')[0]
env = {'HTB_TOKEN': token}

p = subprocess.Popen(['./htb-mcp-server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=env, text=True)
p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
p.stdin.flush()
p.stdout.readline()

challenge_id = sys.argv[1] if len(sys.argv) > 1 else "500"
p.stdin.write(f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"start_challenge","arguments":{{"challenge_id":{challenge_id}}}}}}}\n')
p.stdin.flush()
print(p.stdout.readline())
p.terminate()
