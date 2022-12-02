import numpy as np

target = 34000000
max_house = 10000000

def factors(n):
    r = np.arange(1, int(n ** 0.5) + 1)
    x = r[np.mod(n, r) == 0]
    return set(np.concatenate((x, n / x), axis=None))

reached_target = False
deliveries = {}
for house in range(1, max_house + 1):
    elves = factors(house)
    # print(f'Elves {elves}')
    # print(f'Deliveries {deliveries}')
    working_elves = elves.copy()
    for elf in elves:
        if elf in deliveries:
            if deliveries[elf] == 50:
                # print(f'Removing {elf}')
                working_elves.remove(elf)
            else:
                deliveries[elf] += 1
        else:
            deliveries[elf] = 1
    num_presents = sum(working_elves) * 11
    if num_presents >= target:
        print(f'Ans: {house} received {num_presents}')
        reached_target = True
        break
print(f'Reached target: {reached_target}')