
target = (2981, 3075)
# target = (6, 6)

c1 = 20151125
f = 252533
q = 33554393

r = 1
c = 1
d = 1
value = None
for i in range(1, 2000000000 + 1):
    if value is None:
        value = c1
    else:
        value = (value * f) % q
    # print(f'{i}: [{r}, {c}] (d:{d}) {value}')
    if (r, c) == target:
        break
    r -= 1
    c += 1
    if r == 0:
        d += 1
        r = d
        c = 1
print(f'Part 1: {value} after {i} iterations')