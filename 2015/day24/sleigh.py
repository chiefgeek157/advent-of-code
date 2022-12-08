from copy import deepcopy
import numpy as np

filename = '2015/day24/input.txt'
# filename = '2015/day24/test1.txt'

gifts = np.empty(0, dtype=int)

with open(filename, 'r') as f:
    line = f.readline().strip()
    while line:
        gifts = np.append(gifts, int(line))
        line = f.readline().strip()
print(f'Gifts: {gifts}')
target = int(sum(gifts) / 3)
gifts = np.flip(np.sort(gifts))
print(f'Gifts len:{len(gifts)}, sum:{sum(gifts)}, target:{target}, {gifts}')

def find_groups(target: int, current: list[int], candidates: list[int]) -> tuple:
    """Get a group of candidates that sum to the target. Cnadidates
    must be sorted in descneding order for effeciency assumptions to
    work."""
    print(f'TGT:{target} CUR:{current} CAN:{candidates}')
    new_candidates = []
    group = list(current)
    sum_group = sum(group)
    for i in range(len(candidates)):
        if sum_group == target:
            break
        if sum_group + candidates[i] <= target:
            new_group, new_candidates = find_groups(target, group + [candidates[i]], candidates[i + 1:])
            print(f'Adding {candidates[i]} to group')
            group = np.append(group, candidates[i])
            sum_group = sum(group)
        else:
            new_candidates.append(candidates[i])

    return (group, new_candidates)

def build_groups(target: int, groups: list[np.array], group_id: int, gifts: np.array,
        save_groups: dict):
    print_groups(groups)
    print(f'Build TGT:{target}, groups:{groups}, id:{group_id}, gifts:{gifts}')
    if len(gifts) == 0 and sum(groups[2]) == target:
        print(f'Found candidate groups set')
        if len(groups[0]) not in save_groups:
            save_groups[len(groups[0])] = []
        save_groups[len(groups[0])].append(groups)
        return
    if group_id >= 3:
        print(f'Dead end')
        return

    new_gifts = np.copy(gifts)
    for i in range(len(gifts)):
        if sum(groups[group_id]) + gifts[i] <= target:
            print(f'Using gift {gifts[i]}')
            new_gifts = new_gifts[new_gifts != gifts[i]]
            new_groups = deepcopy(groups)
            new_groups[group_id] = np.append(new_groups[group_id], gifts[i])
            if sum(new_groups[group_id]) == target:
                group_id += 1
            build_groups(target, new_groups, group_id, new_gifts, save_groups)
        else:
            print(f'Skipping gift {gifts[i]}')


def build_group(target: int, gifts: np.array) -> np.array:
    print(f'Gifts: {gifts}')
    if sum(gifts) < target:
        # Cannot build a group from this list of gifts
        print('Not eoung gifts left')
        return (None, gifts)
    new_gifts = np.copy(gifts)
    group = np.empty(0, np.int16)
    for gift in gifts:
        if gift <= target - sum(group):
            # Still room for this gift
            group = np.append(group, gift)
            new_gifts = new_gifts[new_gifts != gift]
    if sum(group) == target:
        return (group, new_gifts)
    else:
        # Exhausted all option but did not build a group
        print('Did not match target')
        return (None, gifts)

def use_gift(group: np.array, gifts: np.array) -> tuple:
    print(f'Use gift group: {group} gifts: {gifts}')
    new_gifts = np.copy(gifts)
    for gift in gifts:
        if gift <= target - sum(group):
            # Still room for this gift
            print('Using gift {gift}')
            group = np.append(group, gift)
            new_gifts = new_gifts[new_gifts != gift]
            return (group, new_gifts)
        else:
            print('Skipping gift {gift}')
    # Did not add a gift to the group
    return (None, gifts)

def build_group(target: int, gifts: np.array):
    group = np.empty(0, np.int16)
    new_gifts = np.copy(gifts)
    while group is not None and sum(group) < target:
        group, new_gifts = use_gift(group, new_gifts)
    if group is None:
        print(f'Failed to build group')
        return (None, gifts)
    print(f'Built group {group} {new_gifts}')
    return (group, new_gifts)

def build_group_set(target: int, gifts: np.array):
    groups = []
    new_gifts = np.copy(gifts)
    for i in range(3):
        group, new_gifts = build_group(target, new_gifts)
        if group is not None:
            groups.append(group)
        else:
            return None
    return groups

def print_groups(groups: list[np.array]) -> None:
    for group in groups:
        print(f'Group: {group}')

def find_group_sets(target: int, groups: list[np.array], gid: int,
        gifts: np.array, valid_groups: dict) -> None:
    """gifts is the current working set of available gifts
    Each recursion, gifts reflects the now-available gifts to work with
    If a valid group_set is found, it is added to valid_groups
    It is assumed that the working groups is not a complete set
    """
    print(f'find_groups: gifts: {gifts} gid {gid}')
    print_groups(groups)
    # Last group, so sum of remaning gifts must equal target
    if gid == 2:
        if sum(gifts) == target:
            print(f'Found group set')
            groups[gid] = np.copy(gifts)
            print_groups(groups)
            size = len(groups[0])
            if size not in valid_groups:
                valid_groups[size] = []
            valid_groups[size].append(groups)
            return
        else:
            print('Remaining gifts do not equal target for last group')
            return

    # Try all remaining gifts
    if len(groups) == gid:
        groups.append(np.empty(0, np.int16))

    while len(gifts) > 0:
        gift = gifts[0]
        gifts = gifts[gifts != gift]
        print(f'Group {gid} {groups[gid]} checking gift {gift}')
        if sum(groups[gid]) + gift <= target:
            print(f'Group {gid} {groups[gid]} adding {gift} to {groups[gid]}')
            # We can add this gift
            new_groups = deepcopy(groups)
            new_gid = gid
            # Append gift to current group
            new_groups[gid] = np.append(new_groups[gid], gift)
            # Remove gift from working gifts
            new_gifts = gifts[gifts != gift]
            if sum(new_groups[new_gid]) == target:
                # Move to the next group
                new_groups.append(np.empty(0, np.int16))
                new_gid += 1
            print(f'Group {gid} {new_groups[gid]} about to visit gid {new_gid} with gifts {new_gifts}')
            find_group_sets(target, new_groups, new_gid, new_gifts, valid_groups)
            print(f'Group {gid} {groups[gid]} back from gift {gift} with gifts {gifts}')
            print_groups(groups)
        else:
            print(f'Group {gid} {groups[gid]} skipping gift {gift} gifts {gifts}')

# valid_groups = {}
# groups = []
# find_group_sets(target, groups, 0, gifts, valid_groups)

def add_gift(target, group, gifts, min_g_len, min_g_product):
    new_gifts = np.copy(gifts)
    for i in range(len(gifts)):
        new_gifts = new_gifts[new_gifts != gifts[i]]
        new_group = np.append(group, gifts[i])
        sum_g = sum(new_group)
        if sum_g == target:
            group1 = np.append(group1, gifts[i])
            print(f'Found candidate {group1}')
            if len(group1) <= min_g1_len:
                product = np.product(group1)
                print(f'Product {product}')
                if product < min_g1_value:
                    min_g1_value = product
        elif sum_g1 + gifts[i] < target:
            group1 = np.append(group1, gifts[i])
            print(f'Adding to group1 {group1}')
        else:
            continue

min_g1_len = 100000000000
min_g1_value = 100000000000
group1 = []
for i in range(len(gifts)):
    sum_g1 = sum(group1)
    if sum_g1 + gifts[i] == target:
        group1 = np.append(group1, gifts[i])
        print(f'Found candidate {group1}')
        if len(group1) <= min_g1_len:
            product = np.product(group1)
            print(f'Product {product}')
            if product < min_g1_value:
                min_g1_value = product
    elif sum_g1 + gifts[i] < target:
        group1 = np.append(group1, gifts[i])
        print(f'Adding to group1 {group1}')
    else:
        continue
print(f'Ans: {min_g1_value}')


# new_gifts = np.copy(gifts)
# group_set = []
# for i in range(3):
#     group, new_gifts = build_group(target, new_gifts)
#     if group is not None:
#         group_set.append(group)
#     else:

# if len(group_set[0]) not in groups:
#     groups[len(group_set[0])] = []
# groups[len(group_set[0])].append(group_set)

# print(f'Groups: {groups}')
# build_groups(target, [np.empty(0, dtype=np.int16)] * 3, 0, gifts, groups)
# print_groups(groups)
