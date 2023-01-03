"""A bunch of utilities"""

from copy import copy
import math


def round_int(x: float) -> int:
    if x < 0:
        return math.trunc(x) if -x % 1 < 0.5 else math.floor(x)
    else:
        return math.trunc(x) if  x % 1 < 0.5 else math.ceil(x)

def round_complex(c: complex) -> complex:
    return complex(round_int(c.real), round_int(c.imag))

def mod_inverse(a: int, m: int) -> int:
    """Return the inverse mod for m given b.

    FInd x such that
    a * x === 1 mod m
    """
    a1 = a % m
    for i in range(m):
        if (i * a1) % m == 1:
            print(f'Found mod inverse of {a} and {m}: {i}')
            return i
    print(f'NO mod inverse of {a} and {m}')
    return 0

def chinese_remainder(n: list[int], b: list[int]) -> int:
    """Return the lowest number, n, such that n % n[i] = b[i].

    See https://www.youtube.com/watch?v=zIFehsBHB8o

    Bases must be co-prime.
    """
    print(f'Finding Chinese Reaminder of {n} with remainders {b}')
    count = len(n)
    N0 = math.prod(n)
    print(f'   - N0: {N0}')
    N = []
    for i in range(count):
        N.append(int(N0 / n[i]))
        print(f'   - N[{i}]: {N[-1]}')
    sum_bNx = 0
    for i in range(count):
        xi = mod_inverse(N[i], n[i])
        sum_bNx += b[i] * N[i] * xi
    result = sum_bNx % N0
    print(f'  - Found solution at {result}')
    for i in range(count):
        print(f'    - Check that {result} % {n[i]} = {b[i]}: {result % n[i] == b[i]}')
    return result
