import numpy as np

target = 34000000
max_house = 10000000

def factors(n):
    r = np.arange(1, int(n ** 0.5) + 1)
    x = r[np.mod(n, r) == 0]
    return set(np.concatenate((x, n / x), axis=None))

reached_target = False
for house in range(1, max_house + 1):
    facts = factors(house)
    # print(f'Factors {house}: {facts}')
    # num_presents = 0
    # for elf in range(1, house + 1):
    #     if house % elf == 0:
    #         num_presents += 10 * elf
    # print(f'House {house} presents {num_presents}')
    # if num_presents >= target:
    num_presents = sum(facts) * 10
    if num_presents >= target:
        print(f'Ans: {house} received {num_presents}')
        reached_target = True
        break
print(f'Reached target: {reached_target}')