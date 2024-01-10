import numpy as np
from math import ceil, log
# will only consider sequences of lower case and spaces
# no "efficent" deduplication

BASE = 4

table = {}
decoder = {}
# we need to find k such that b^{k+1} - b^k > 27.
k = ceil(log(27/(BASE - 1), BASE)) + 1

for i, ch in enumerate(' abcdefghijklmnopqrstuvwxyz'):
    table[ch] = BASE**k + i
    decoder[BASE**k + i] = ch

# this way we consider all length k+1 lists

def numberToBase(n, b=BASE):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def convert_from(n, b=BASE):
    s = 0
    for i, d in enumerate(n[::-1]):
        s += b**i * d
    return s

def encode(message, b=BASE):
    if not set(message).issubset(set(' qwertyuiopasdfghjklzxcvbnm')):
        raise ValueError('`message` cannot contain any other characters')
    nums = map(lambda x: table[x], message)
    seq = []
    for n in nums:
        seq += numberToBase(n, b) # no seperators...
    return seq

def decode(message, b=BASE):
    seq = ""
    for i in range(0, len(message), k+1):
        num = message[i:i+k+1]
        print(num)
        conv = convert_from(num, BASE)
        seq += decoder[conv]
    return seq

### test
# message = "hello world"
# enc = encode(message)
# print(''.join(map(str, enc)))
# dec = decode(enc)
# print(dec)