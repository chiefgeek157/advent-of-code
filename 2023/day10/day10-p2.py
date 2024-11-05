from typing import Sequence

filename = '2023/day10/input.txt'
# filename = '2023/day10/test1.txt'
# filename = '2023/day10/test2.txt'
# filename = '2023/day10/test3.txt'
# filename = '2023/day10/test4.txt'
# filename = '2023/day10/test5.txt'
# filename = '2023/day10/test6.txt'

start_first_pipes = {
    0: '-7J',
    1: '|JL',
    2: '-LF',
    3: '|F7',
}

# Next pipe, from dir => dir change
# Assme CW rotation, so right turn +, left turn -
pipe_dir_incr = {
    ('-', 0): 0,
    ('-', 2): 0,
    ('|', 1): 0,
    ('|', 3): 0,
    ('L', 2): 1,
    ('L', 1): -1,
    ('F', 2): -1,
    ('F', 3): 1,
    ('J', 0): -1,
    ('J', 1): 1,
    ('7', 0): 1,
    ('7', 3): -1,
}

prev_dirs = {
    ('-', 0): 2,
    ('-', 2): 0,
    ('|', 1): 3,
    ('|', 3): 1,
    ('L', 2): 3,
    ('L', 3): 0,
    ('F', 0): 1,
    ('F', 1): 0,
    ('J', 2): 3,
    ('J', 3): 2,
    ('7', 2): 1,
    ('7', 1): 2,
}

# Dirs clockwise from right
dir_offsets = [[1, 0], [0, 1], [-1, 0], [0, -1]]

# Start pipes
start_pipes = {
    0: {
        1: 'F',
        2: '-',
        3: 'L',
    },
    1: {
        2: '7',
        3: '|',
    },
    2: {
        3: 'J',
    },
}

def point_add(p1: Sequence, p2: Sequence) -> Sequence:
    return tuple(map(sum, zip(p1, p2)))

def grid_get(grid: Sequence, p: Sequence[int], default=None) -> any:
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

def print_grid(grid: Sequence, loop: Sequence) -> None:


def main() -> int:
    # Grid is an array of strings
    grid = []
    start_pos = None
    with open(filename, 'r') as f:
        line = f.readline()
        row = 0
        while line:
            grid.append(line.strip())
            if start_pos is None:
                col = line.find('S')
                if col >= 0:
                    start_pos = (col, row)
                    print(f'Start is {start_pos}')
            line = f.readline()
            row += 1

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid_get(grid, (x, y)), end='')
        print()

    # Detect type of pipe at start_pos
    print(f'Detecting pipe at {start_pos}')
    dir1 = None
    dir2 = None
    for d in range(4):
        # print(f'  Checking d:{d}')
        next_pos = point_add(start_pos, dir_offsets[d])
        next_pipe = grid_get(grid, next_pos)
        # print(f'    grid[{next_pos}]: {next_pipe}')
        if next_pipe is None:
            # print(f'    Out of bounds')
            continue
        if next_pipe == '.':
            # print(f'    Not a pipe')
            continue
        if next_pipe in start_first_pipes[d]:
            # Found the next pipe
            # print(f'    Found pipe {next_pipe} at {next_pos}')
            if dir1 is None:
                # print(f'      Setting dir1 to {d}')
                dir1 = d
            else:
                # print(f'      Setting dir2 to {d}')
                dir2 = d
                break
    if dir1 is None or dir2 is None:
        print(f'Did not detect type of pipe at {start_pos}')
        exit(1)
    start_pipe = start_pipes[dir1][dir2]
    print(f'Start pipe is {start_pipe}')
    # Replace start pipe
    row_list = list(grid[start_pos[1]])
    row_list[start_pos[0]] = start_pipe
    grid[start_pos[1]] = ''.join(row_list)
    # print(f'Start pipe now {grid_get(grid, start_pos)}')

    # Loop is a list of (pos, dir1, dir2) around the loop
    # Dir 1 is CW if looping dir is CW, else CCW
    loop = []
    loop_pos = set()

    pos = start_pos
    pipe = start_pipe
    dir = dir1
    prev_dir = dir2

    # Travel in dir1 direction, but we still have to detect if this is CW or CCW
    # by counting the number of left and right turns. MOre right turns means
    # CW, more left means CCW. The difference should be exactly 4.
    right_turns = 0
    left_turns = 0

    while (right_turns + left_turns) == 0 or pos != start_pos:
        print(f'Loop: pos: {pos}, pipe: {pipe}, dir: {dir}, prev_dir: {prev_dir}', end=' ')
        next_pos = point_add(pos, dir_offsets[dir])
        next_pipe = grid_get(grid, next_pos)
        dir_incr = pipe_dir_incr[(next_pipe, dir)]
        next_dir = (dir + dir_incr) % 4
        print(f'  next_pos: {next_pos}, next_pipe: {next_pipe}, '
              f'dir_incr: {dir_incr}, next_dir: {next_dir}, '
              f'prev_dir: {prev_dir}')
        if dir_incr > 0:
            right_turns += 1
        elif dir_incr < 0:
            left_turns += 1

        loop.append((pos, dir, prev_dir))
        loop_pos.add(pos)

        pos = next_pos
        pipe = next_pipe
        prev_dir = (dir + 2) % 4
        dir = next_dir

        if len(loop) > 100000:
            print(f'Abort loop {loop}')
            exit(1)
    print(f'Loop[{len(loop)}]')
    print(loop)

    cw = (right_turns > left_turns)
    print(f'Loop in clockwise: {cw} (right: {right_turns}, left: {left_turns})')
    if abs(left_turns - right_turns) != 4:
        print(f'ERROR: difference is not 4')
        exit(1)

    # Count positions inside the loop
    # Look right if cw, left if ccw
    # First get inside cells adjacent to loop
    inside_pos = set()
    work = set()
    visited = set()
    for i in range(len(loop)):
        # pos is cell, dir1 is loop forward, dir2 is loopbackward wrt CW dir
        # when emerging from this cell
        pos, dir1, dir2 = loop[i]
        cw_dir = dir1 if cw else dir2
        print(f'loop[{i}]: pos: {pos}, cw_dir: {cw_dir}, pipe: {grid_get(grid, pos)}', end=' ')

        side_dir = (cw_dir + 1) % 4
        side_pos = point_add(pos, dir_offsets[side_dir])
        side_pipe = grid_get(grid, side_pos)
        print(f'  side_dir: {side_dir}, side_pos: {side_pos}, side_pipe: {side_pipe}', end=' ')
        if side_pipe is not None and side_pos not in loop_pos:
            # The side pos is valid and not on the loop
            print(f'INISIDE')
            inside_pos.add(side_pos)
            work.add(side_pos)
        else:
            print('OFF GRID' if side_pipe is None else 'LOOP')

        # Step the next pos in CW dir
        pos = point_add(pos, dir_offsets[cw_dir])

    steps = 0
    while work:
        # print(f'Inside[{len(inside_pos)}]')
        # print(inside_pos)
        # print(f'  Work[{len(work)}]')
        # print(work)
        # print(f'  Visited[{len(visited)}]')
        # print(visited)
        pos = work.pop()
        # print(f'  Visiting {pos}')
        visited.add(pos)
        for d in range(4):
            other_pos = point_add(pos, dir_offsets[d])
            other_pipe = grid_get(grid, other_pos)
            # print(f'  Checking {other_pos}: {other_pipe}')
            if (other_pipe is not None
                    and other_pos not in visited
                    and other_pos not in work
                    and other_pos not in loop_pos):
                print(f'  Adding inside pos {other_pos}')
                inside_pos.add(other_pos)
                work.add(other_pos)
        steps += 1
        if steps > 10000:
            print(f'Early exit')
            exit(0)

    return len(inside_pos)

if __name__ == '__main__':
    print(f'Answer: {main()}')
