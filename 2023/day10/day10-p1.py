# filename = '2023/day10/input.txt'
filename = '2023/day10/test1.txt'
# filename = '2023/day10/test2.txt'

pipe_map = {
    0: '-7J',
    1: '|JL',
    2: '-LF',
    3: '|F7'
}

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
                    start = (row, col)
            line = f.readline()
            row += 1

    steps = 0
    pos = start
    dir = 2
    next = None
    while steps > pos != start:
        # Search for other pipe
        for d in range(4):
            if d == dir:
                continue
            if d == 0:
                next = (pos[0], pos[1] + 1)
            elif d == 1:
                next = (pos[0] + 1, pos[1])
            elif d == 2:
                next = (pos[0], pos[1] - 1)
            else:
                next = (pos[0] - 1, pos[1])
            if next[0] < 0 or next[0] >= len(grid[0]) or next[1] < 0 or next[1] >= len(grid):
                # Out of bounds
                continue
            if grid[next[0]][next[1]] in pipe_map[d]:
                break
        dir = d
        pos = next

    return 0

if __name__ == '__main__':
    print(f'Answer: {main()}')
