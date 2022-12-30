# filename = '2020/day07/test1.txt'
# filename = '2020/day07/test2.txt'
filename = '2020/day07/input.txt'

# Names of bags
bags = set()

# Values are a list of bags
parents = {}

# Values are list of bags
children = {}

# Keys are (parent, child)
child_counts = {}

with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        bag = ' '.join([fields[0], fields[1]])
        bags.add(bag)
        children[bag] = []
        for n in range(int((len(fields) - 4) / 4)):
            pos = 4 * n + 4
            child_bag = ' '.join([fields[pos + 1], fields[pos + 2]])
            bags.add(child_bag)
            children[bag].append(child_bag)
            child_counts[(bag, child_bag)] = int(fields[pos])
            if child_bag in parents:
                child_parents = parents[child_bag]
            else:
                child_parents = []
                parents[child_bag] = child_parents
            child_parents.append(bag)
        line = f.readline()

work = ['shiny gold']
visited = []
results = set()
while work:
    bag = work.pop()
    visited.append(bag)
    parent_bags = parents.get(bag, [])
    results.update(parent_bags)
    for parent_bag in parent_bags:
        if parent_bag not in visited:
            work.append(parent_bag)

print(f'\nPart 1: {len(results)}')

def sum_children(bag):
    count = 0
    child_bags = children.get(bag, [])
    for child_bag in child_bags:
        child_count = child_counts[(bag, child_bag)]
        count += child_count * (sum_children(child_bag) + 1)
    return count

result = sum_children('shiny gold')

print(f'\nPart 2: {result}')
