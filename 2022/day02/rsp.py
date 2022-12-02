filename = '2022/day02/input.txt'
# filename = '2022/day02/test1.txt'

values = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

scores = {
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3
}

outcomes = {
    ('A', 'X'): 'Z',
    ('A', 'Y'): 'X',
    ('A', 'Z'): 'Y',
    ('B', 'X'): 'X',
    ('B', 'Y'): 'Y',
    ('B', 'Z'): 'Z',
    ('C', 'X'): 'Y',
    ('C', 'Y'): 'Z',
    ('C', 'Z'): 'X'
}

def get_score(them, us) -> int:
    global values, scores, outcomes
    us_item = outcomes[(them, us)]
    return values[us_item] + scores[(them, us_item)]

total_score = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        fields = line.split()
        score = get_score(fields[0], fields[1])
        print(f'For {fields[0]}, {fields[1]} score {score}')
        total_score += score
        line = f.readline()

print(f'Ans: {total_score}')
