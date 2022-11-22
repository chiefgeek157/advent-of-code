import hashlib

seed = 'ckczppom'

val = 1
while True:
    input = seed + str(val)
    hash = hashlib.md5((seed + str(val)).encode()).hexdigest()
    # print(f'input={input} hash={hash}')
    if hash.startswith('000000'): break
    val += 1

print(f'val={val}')