filename = '2022/day10/input.txt'
# filename = '2022/day10/test1.txt'
# filename = '2022/day10/test2.txt'

measure_at = [20, 60, 100, 140, 180, 220]

sum_signals = 0
x = 1
cycle = 1
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        print(f'Cycle {cycle} read {line.strip()}')
        fields = line.split()
        if fields[0] == 'noop':
            v = 0
            counter = 1
        else:
            v = int(fields[1])
            counter = 2

        for i in range(counter):
            if cycle in measure_at:
                signal = x * cycle
                print(f'At special cycle {cycle} signal: {signal}')
                sum_signals += signal
            print(f'End of repeat {cycle}')
            cycle += 1
        x += v
        print(f'At end of cycle {cycle - 1} x {x}')
        line = f.readline()

print(f'Part 1: {sum_signals}')