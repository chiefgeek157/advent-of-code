# filename = '2022/day21/test1.txt'
filename = '2022/day21/input.txt'

funcs = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}

inv_funcs = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*'
}

jobs = {}
parents = {}

def get_result(m):
    print(f'Getting results for {m}')
    job = jobs[m]
    if len(job) == 1:
        print(f'  - {m} is const {job[0]}')
        return job[0]
    else:
        arg1 = get_result(job[1])
        arg2 = get_result(job[2])
        res = int(funcs[job[0]](arg1, arg2))
        print(f'  - {m} returns {arg1} {job[0]} {arg2} = {res}')
        parents[job[1]] = m
        parents[job[2]] = m
        return res

with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split(':')
        args = fields[1].split()
        if len(args) == 1:
            job = [int(args[0])]
        else:
            job = [args[1], args[0], args[2]]
        jobs[fields[0]] = job

        line = f.readline()

for k, v in jobs.items():
    print(f'Job {k}: {v}')

res = get_result('root')

print(f'\nPart 1: {res}')

# Re-balance the tree from 'humn'

def get_humn_result(m):
    print(f'Getting INV results for {m}')
    if m in humn_jobs:
        job = humn_jobs[m]
        print(f'  - {m} is an inverse node {job}')
        arg1 = get_humn_result(job[1])
        if job[0] == '=':
            res = arg1
            print(f'  - {m} INV returns = {res}')
        else:
            arg2 = get_humn_result(job[2])
            res = int(funcs[job[0]](arg1, arg2))
            print(f'  - {m} INV returns {arg1} {job[0]} {arg2} = {res}')
    else:
        print(f'  - {m} is a regular node')
        res = get_result(m)

    return res

humn_jobs = {}
name = 'humn'
while name != 'root':
    print(f'Visiting {name}')
    job = jobs[name]
    parent_name = parents[name]
    print(f'  - Parent is {parent_name}')
    parent = jobs[parent_name]
    # Special handling of root
    if parent_name == 'root':
        print(f'  - Handling root')
        if name == parent[1]:
            new_job = ['=', parent[2]]
        else:
            new_job = ['=', parent[1]]
    else:
        if name == parent[1]:
            print(f'  - Child is arg1')
            new_job = [inv_funcs[parent[0]], parent_name, parent[2]]
        else:
            print(f'  - Child is arg2')
            new_job = [inv_funcs[parent[0]], parent_name, parent[1]]
    humn_jobs[name] = new_job
    name = parent_name

res = get_humn_result('humn')

print(f'\nPart 2: {res}')

# # Find 'humn'
# stack = [jobs['root'][1]]
# name = None
# while stack:
#     name = stack.pop()
#     if name == 'humn':
#         print('Found humn')
#         break
#     job = jobs[name]
#     if len(job) > 1:
#         stack.append(job[1])
#         stack.append(job[2])
# if name is None:
#     human_side = jobs['root'][2]
#     other_side = jobs['root'][1]
# else:
#     human_side = jobs['root'][1]
#     other_side = jobs['root'][2]

# res1 = get_result(other_side)
# print(f'Other side {other_side} = {res1}')

