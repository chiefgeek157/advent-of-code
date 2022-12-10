filename = '2022/day10/input.txt'
# filename = '2022/day10/test1.txt'
# filename = '2022/day10/test2.txt'

def render_scan(scan):
    line = ''
    for i in range(len(scan)):
        line += '#' if scan[i] else '.'
    return line

def render_sprite(sprite, w=40):
    line = ''
    for i in range(w):
        line += '#' if i in range(sprite - 1, sprite + 2) else '.'
    return line

def print_screen(screen):
    for scan in screen:
        print(render_scan(scan))

screen = []
print_screen(screen)
x = 1
cycle = 1
scan = 0
pos = 0
instruction = None
with open(filename, 'r') as f:
    print(f'Sprite position: {render_sprite(x)}')
    while True:
        print()
        if instruction == None:
            instruction = f.readline().strip()
            if not instruction:
                break
            print(f'Start  cycle {cycle:3}: begin executing {instruction}')
            fields = instruction.split()
            if fields[0] == 'noop':
                v = 0
                delay = 0
            else:
                v = int(fields[1])
                delay = 1

        if pos == 0:
            screen.append([])

        print(f'During cycle {cycle:3}: CRT draws pixel in position {pos}')
        if pos in range(x - 1, x + 2):
            screen[scan].append(True)
        else:
            screen[scan].append(False)
        print(f'Current CRT row : {render_scan(screen[scan])}')
        if delay == 0:
            x += v
            print(f'End of cycle {cycle:3}: finish executing {instruction} (Register X is now {x})')
            print(f'Sprite position: {render_sprite(x)}')
            instruction = None
        else:
            delay -= 1
        cycle += 1
        pos += 1
        if pos == 40:
            pos = 0
            scan += 1

print_screen(screen)
