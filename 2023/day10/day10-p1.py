filename = '2023/day10/input.txt'
# filename = '2023/day10/test1.txt'
# filename = '2023/day10/test2.txt'

start_first_pipes = {
    0: '-7J',
    1: '|JL',
    2: '-LF',
    3: '|F7',
}

pipe_next_dirs = {
    ('-', 0): 0,
    ('-', 2): 2,
    ('|', 1): 1,
    ('|', 3): 3,
    ('L', 1): 0,
    ('L', 2): 3,
    ('F', 2): 1,
    ('F', 3): 0,
    ('J', 0): 3,
    ('J', 1): 2,
    ('7', 0): 1,
    ('7', 3): 2,
}

# Dirs clockwise from right
dir_offsets = [[1, 0], [0, 1], [-1, 0], [0, -1]]

def point_add(p1: list, p2: list) -> list:
    return list(map(sum, zip(p1, p2)))

def grid_get(grid: list, p: list[int], default=None) -> any:
    # print(f'grid_get({grid}, {p})')
    sub = grid
    for i in reversed(range(len(p))):
        # print(f'Dim:{i} Sub is: {sub}')
        if p[i] < 0 or p[i] >= len(sub):
            # print(f'Out of bounds at {p}')
            return default
        if i > 0:
            sub = sub[p[i]]
        else:
            # print(f'Returning {sub[p[0]]}')
            return sub[p[0]]

def main() -> int:
    # Grid is an array of strings
    grid = []
    start = None
    with open(filename, 'r') as f:
        line = f.readline()
        row = 0
        while line:
            grid.append(line.strip())
            if start is None:
                col = line.find('S')
                if col >= 0:
                    start = [col, row]
                    print(f'Start is {start}: {grid_get(grid, start)}')
            line = f.readline()
            row += 1

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid_get(grid, [x, y]), end='')
        print()

    loop = []
    # Find first pipe next to start
    print(f'Starting at {start}, finding first pipe')
    found = False
    for d in range(4):
        print(f'  Checking d:{d}')
        next_pos = point_add(start, dir_offsets[d])
        next_pipe = grid_get(grid, next_pos)
        print(f'    grid[{next_pos}]: {next_pipe}')
        if next_pipe is None:
            print(f'    Out of bounds')
            continue
        if next_pipe == '.':
            print(f'    Not a pipe')
            continue
        if next_pipe in start_first_pipes[d]:
            # Found the next pipe
            print(f'    Found the next pipe {next_pipe} at {next_pos}')
            found = True
            break
    if not found:
        print(f'Did not find a pipe next to {start}')
        exit(1)

    loop.append(start)

    pos = next_pos
    pipe = next_pipe
    dir = d
    while pos != start:
        print(f'pos: {pos}, pipe: {pipe}')
        loop.append(pos)

        next_dir = pipe_next_dirs[(pipe, dir)]
        next_pos = point_add(pos, dir_offsets[next_dir])
        next_pipe = grid_get(grid, next_pos)
        print(f'  next dir: {next_dir}, pos: {next_pos}, pipe: {next_pipe}')
        dir = next_dir
        pos = next_pos
        pipe = next_pipe

        if len(loop) > 100000:
            print(f'Abort loop {loop}')
            exit(1)

    return len(loop) // 2

if __name__ == '__main__':
    print(f'Answer: {main()}')
