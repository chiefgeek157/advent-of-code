import re
import sys

# INPUT = 'vzbxkghb'
INPUT = 'vzbxxyzz'
# MAX_TRIES = sys.maxsize

# INPUT = 'abcdefgh'
# INPUT = 'ghjaaaaa'
MAX_TRIES = 1000000

CHARS = 'abcdefghjkmnpqrstuvwxyz'
MAX_INDEX = len(CHARS) - 1

def increment(char: str) -> tuple:
    carry = False
    index = CHARS.index(char)
    if index == MAX_INDEX:
        index = -1
        carry = True
    index += 1
    return (CHARS[index], carry)

def rotate(pwd: str):
    # print(f'Rotating {pwd}')
    new = ''
    i = 0
    carry = True
    while carry:
        # print(f'Checking char {pwd[i]}')
        char, carry = increment(pwd[i])
        new += char
        # print(f'New now {new}')
        i += 1
    new += pwd[i:]
    # print(f'New now {new}')
    return new

RESEQ = re.compile('(zyx|yxw|xwv|wvu|vut|uts|tsr|srq|rqp|qpn|pnm|nmk|mkj|kjh|jhg|hgf|fed|edc|dcb|cba)')
REDBL = re.compile(r'((.)\2).*(?!\1)((.)\4)')
def is_valid(pwd: str):
    return RESEQ.search(pwd) and REDBL.search(pwd)

pwd = INPUT[::-1]
tries = 0
found = False
while tries < MAX_TRIES:
    pwd = rotate(pwd)
    # print(f'Trying: {pwd}')
    if is_valid(pwd):
        found = True
        break
    tries += 1

pwd = pwd[::-1]
print(f'Ans: Found {found} {pwd} in {tries} tries')