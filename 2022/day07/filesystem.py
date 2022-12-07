filename = '2022/day07/input.txt'
# filename = '2022/day07/test1.txt'
part2 = False

root = {
    'name': '/',
    'size': 0,
    'items': {},
    'parent': None
}

def compute_size(item) -> int:
    # print(f'Item: {item}')
    if 'items' in item:
        for child in item['items'].values():
            item['size'] += compute_size(child)
    return item['size']

def sum_dir(max_size, dir):
    sum = 0
    if dir['size'] <= max_size:
        sum += dir['size']
    for child in dir['items'].values():
        if 'items' in child:
            sum += sum_dir(max_size, child)
    return sum

def min_dir(needed: int, min_size: int, dir: dict):
    print(f'Dir:{dir["name"]} {dir["size"]}')
    if dir['size'] >= needed:
        if dir['size'] < min_size:
            print(f'New min dir: {dir["name"]} {dir["size"]}')
            min_size = dir['size']
        for child in dir['items'].values():
            if 'items' in child:
                min_size = min_dir(needed, min_size, child)
    else:
        print(f'Skipping {dir["name"]} {dir["size"]} as smaller than {needed}')
    return min_size

pwd = root
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        if fields[0] == '$':
            if fields[1] == 'cd':
                if fields[2] == '..':
                    pwd = pwd['parent']
                elif fields[2] == '/':
                    pwd = root
                else:
                    pwd = pwd['items'][fields[2]]
                print(f'pwd:{pwd["name"]}')
            else:
                pass
        elif fields[0] == 'dir':
            pwd['items'][fields[1]] = {
                'name': fields[1],
                'parent': pwd,
                'items': {},
                'size': 0
            }
        else:
            pwd['items'][fields[1]] = {
                'name': fields[1],
                'size': int(fields[0])
            }
        line = f.readline()

compute_size(root)
# print(f'{root}')

print(f'Part 1: {sum_dir(100000, root)}')

needed = 30000000 - (70000000 - root['size'])
print(f'Needed: {needed}')
min_size = min_dir(needed, 70000000, root)
print(f'Part 2: {min_size}')
