from copy import copy, deepcopy
import math
import sys

filename = '2015/day24/input.txt'
# filename = '2015/day24/test1.txt'
part2 = True

gifts = []

with open(filename, 'r') as f:
    line = f.readline().strip()
    while line:
        gifts.append(int(line))
        line = f.readline().strip()
# print(f'Gifts: {gifts}')
target = int(sum(gifts) / (4 if part2 else 3))
gifts = sorted(gifts)
print(f'Gifts len:{len(gifts)}, sum:{sum(gifts)}, target:{target}, {gifts}')

def print_groups(all_groups):
    for groups_groups in all_groups.values():
        for groups in groups_groups:
            print(f'{groups[0]}  {groups[1]}  {groups[2]}')

def add_gift(target: int, groups: tuple, gid:int, working_gifts: list[int],
        remaining_gifts: list[int], valid_groups: dict):
    global min_g0_len, min_g0_prod
    if gid == 0 and len(groups[0]) + 1 > min_g0_len:
        # No need to look at longer g0
        return

    group = groups[gid]
    # print(f'add_gift for {gid}: {groups}, {working_gifts}, {remaining_gifts}')
    new_working_gifts = copy(working_gifts)
    for i in range(len(working_gifts)):
        # print(f'   Working gifts: {new_working_gifts}')
        if len(working_gifts) == 0:
            # print(f'   Out of working gifts')
            return
        # Remove gifts from the working set so we don't revit them
        gift = new_working_gifts.pop()
        sum_group = sum(group)

        if sum_group + gift > target:
            # This gift doesn't fit
            # print(f'   Group {gid}: {group} skipping {gift}')
            continue

        # print(f'   Group {gid}: {group} adding {gift}')
        new_groups = deepcopy(groups)
        new_groups[gid].append(gift)
        new_remaining_gifts = copy(remaining_gifts)
        new_remaining_gifts.remove(gift)
        if sum_group + gift == target:
            # This group is filled
            if gid == 0:
                # print(f'   Group 0 filled: {new_groups[0]}')
                if len(new_groups[0]) < min_g0_len:
                    min_g0_len = len(new_groups[0])
                    print(f'New g0 min: {min_g0_len}')
                product = math.prod(new_groups[0])
                if product < min_g0_prod:
                    min_g0_prod = product
                    print(f'New min g0 prod: {min_g0_prod}')
                # add_gift(target, new_groups, 1, new_remaining_gifts, new_remaining_gifts, valid_groups)
            if gid == 1:
                # The remaning gifts by defnintion add up to target
                # print(f'   All groups filled: {new_groups[0]}, {new_groups[1]}, {new_remaining_gifts}')
                # Sanity check
                if sum(new_remaining_gifts) != target:
                    raise Exception('Remaining gifts do not add to target')
                new_groups = (new_groups[0], new_groups[1], new_remaining_gifts)
                size = len(new_groups[0])
                if size not in valid_groups:
                    valid_groups[size] = set()
                valid_groups[size].add(new_groups)
                print(f'   Added valid groups {new_groups}')
                # print_groups(valid_groups)
        else:
            # print(f'   Group {gid}: {new_groups[gid]} Continuing to add to groups')
            add_gift(target, new_groups, gid, new_working_gifts, copy(new_remaining_gifts), valid_groups)
    # print(f'   Out of gifts for group {gid} {group}')

min_g0_len = sys.maxsize
min_g0_prod = sys.maxsize
valid_groups = {}
add_gift(target, ([], [], []), 0, gifts, gifts, valid_groups)

# print(f'Valid groups')
# print_groups(valid_groups)

# min_size_groups = valid_groups[min(valid_groups.keys())]
# min_product = sys.maxsize
# for groups in min_size_groups:
#     product = math.prod(groups[0])
#     min_product = min(min_product, product)

print(f'Part 1: {min_g0_prod}')
