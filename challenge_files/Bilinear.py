import random
from SUPERSECRET import flag

def enc(val,key):
    for i in range(32):
        val = (key + (val ^ key)) % 256
    return val

key = [random.getrandbits(8) for _ in range(256)]

e = [enc(i,key[0]) for i in flag]

for j in key[1:]:
    e = [enc(i,j) for i in e]


print(bytes(e))
#output is b'\xe9c\xb4&{t\xa4\x84\xb1.g+\xedp2\xe5_o\xb032\xe1\x94\xc9o.\xb5>\xb1s\x0e\x94_\xe1\xacw\xc1\xf9S_s\xb4\x12p.g\xc52\xfd'

