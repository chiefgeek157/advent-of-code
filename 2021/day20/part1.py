from enhancer import Enhancer
from image import Image

# filename = '2021/day20/test1.txt'
# filename = '2021/day20/test2.txt'
filename = '2021/day20/input.txt'

e = Enhancer()
i = Image()
with open(filename, 'r') as f:
    e.read(f)
    f.readline()
    i.read(f)

i2 = e.enhance(i, 2)
print(f'{i2}')
print(f'Answer is {i2.lit_count()}')