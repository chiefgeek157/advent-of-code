from copy import copy, deepcopy

# filename = '2015/day24/input.txt'
filename = '2015/day24/test1.txt'

gifts = []

with open(filename, 'r') as f:
    line = f.readline().strip()
    while line:
        gifts.append(int(line))
        line = f.readline().strip()
# print(f'Gifts: {gifts}')
target = int(sum(gifts) / 3)
gifts = sorted(gifts, reverse=True)
print(f'Gifts len:{len(gifts)}, sum:{sum(gifts)}, target:{target}, {gifts}')

def add_gift(target: int, groups: tuple, gid:int, gifts: list[int],
        valid_groups: dict):
    group = groups[gid]
    for i in range(len(gifts)):
        gift = gifts[i]
        sum_group = sum(group)
        if sum_group + gift > target:
            # This gift doesn't fit
            print(f'Group {gid}: {group} skipping {gift}')
            continue
        # Add gift to new group and remove from gifts
        print(f'Group {gid}: {group} Adding {gift} to group {gid}')
        new_groups = deepcopy(groups)
        new_groups[gid].append(gift)
        if sum_group + gift == target:
            # This group is filled
            new_gifts = copy(gifts)
            new_gifts.remove(gift)
            if gid == 0:
                print(f'Group 0 filled: {new_groups[0]}')
                add_gift(target, new_groups, 1, new_gifts, valid_groups)
            if gid == 1:
                # The remaning gifts by defnintion add up to target
                print(f'Group 1 filled: {new_groups[1]}')
                print(f'Group 2 filled: {new_gifts}')
                new_groups = (new_groups[0], new_groups[1], new_gifts)
                size = len(new_groups[0])
                if size not in valid_groups:
                    valid_groups[size] = []
                valid_groups[size].append(new_groups)
                print(f'Added valid groups {new_groups}, {valid_groups}')
        else:
            print(f'Group {gid}: {new_groups[gid]} Continuing to add to groups')
            add_gift(target, new_groups, gid, gifts[i + 1:], valid_groups)

valid_groups = {}
add_gift(target, ([], [], []), 0, gifts, valid_groups)

print(f'Valid groups')
for groups in valid_groups.values():
    print(groups)