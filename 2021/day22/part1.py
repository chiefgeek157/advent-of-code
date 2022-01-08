from space import Prism, Space

p1 = Prism((1,2,3),(7,8,9),True)
p2 = Prism((4,5,6),(10,11,12),True)

print(f'p1 {p1}')
print(f'p1 vol={p1.volume()}')
print(f'p2 {p2}')
print(f'p2 vol={p2.volume()}')

plist = p1.combine(p2)
for p in plist:
    print(f'{p}')