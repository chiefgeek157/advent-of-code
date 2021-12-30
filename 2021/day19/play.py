import math
import numpy as np
import transforms3d as t3d
import transforms3d.affines as aff
import transforms3d.euler as eul

m = aff.compose([0,0,0], np.eye(3,3), [1,1,1])
print(f'{m}')

m = eul.euler2mat(0, 0, 0, 'rxyz')
print(f'{m}')

z = np.zeros(3)
print(f'zeros={z}')
o = np.ones(3)
print(f'ones={o}')
aff.compose(z, m, o)

m = eul.euler2mat(math.pi / 2, 0, 0, 'rxyz')
a = aff.compose(o, m, o)
print(f'{a}')

l2 = [[1, 2, 3], [4, 5, 6]]
print(f'l2\n{l2}')
a = np.array(l2)
print(f'a\n{a}')
print(f'np.asarray(a)\n{np.asarray(a)}')
print(f'np.asarray(a, tuple)\n{np.asarray(a, tuple)}')

l3 = [[4, 5, 6], [7, 8, 9]]
b = np.array(l3)
print(f'b\n{b}')
c = np.vstack((a, b))
print(f'c\n{c}')
d = np.unique(c, axis=0)
print(f'd\n{d}')
