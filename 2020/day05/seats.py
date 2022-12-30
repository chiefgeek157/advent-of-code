# filename = '2020/day05/test1.txt'
filename = '2020/day05/input.txt'

seats = []
for r in range(128):
    for c in range(8):
        seats.append(8 * r + c)

max_seat = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        r1 = 0
        r2 = 127
        # print(f'Ticket {line} starting with {r1}-{r2}')
        for i in range(7):
            if line[i] == 'F':
                r2 = int((r2 - r1 + 1) / 2) + r1 - 1
                # print(f'  - Front half: {r1} - {r2}')
            else:
                r1 = r1 + int((r2 - r1 + 1) / 2)
                # print(f'  - Back  half: {r1} - {r2}')
        # print(f'  - Row is {r1}')
        s1 = 0
        s2 = 7
        for i in range(7, 10):
            if line[i] == 'L':
                s2 = int((s2 - s1 + 1) / 2) + s1 - 1
                # print(f'  - Left  half: {s1} - {s2}')
            else:
                s1 = s1 + int((s2 - s1 + 1) / 2)
                # print(f'  - Right half: {s1} - {s2}')
        # print(f'  - Col is {s1}')
        seat = 8 * r1 + s1
        print(f'  - Seat is {seat}')
        max_seat = max(max_seat, seat)
        seats.remove(seat)
        line = f.readline()

print(f'Part 1: {max_seat}')

print(f'Available seats: {seats}')
seat = 0
prev_seat = seats[0]
for i in range(1, len(seats)):
    if seats[i] - 1 > prev_seat:
        seat = seats[i]
        break
    prev_seat = seats[i]

print(f'Part 2: {seat}')