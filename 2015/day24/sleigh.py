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
    print(f'Build TGT:{target}, groups:{groups}, id:{group_id}, gifts:{gifts}')
    if len(gifts) == 0:
        save_groups[len(groups[0])] = groups
        return
    if group_id > 3:
        return

    for i in range(len(gifts)):
        if sum(groups[group_id]) + gifts[i] <= target:
            new_groups = deepcopy(groups)
            new_groups[group_id] = np.append(new_groups[group_id], gifts[i])
            if sum(new_groups[group_id]) == target:
                group_id += 1
            build_groups(target, new_groups, group_id, np.delete(gifts, i), save_groups)

groups = {}
build_groups(target, [np.empty(0, dtype=np.int16)] * 3, 0, gifts, groups)
print(f'Group {groups}')
