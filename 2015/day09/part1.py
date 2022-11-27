filename = '2015/day09/input.txt'
# filename = '2015/day09/test1.txt'

from tsp import traveling_salesman

cities = {}
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()

        print(f'Adding {fields[0]} to {fields[2]} = {fields[4]}')
        if fields[0] in cities:
            city1 = cities[fields[0]]
        else:
            city1 = {}
            cities[fields[0]] = city1

        if fields[2] in cities:
            city2 = cities[fields[2]]
        else:
            city2 = {}
            cities[fields[2]] = city2

        city1[fields[2]] = int(fields[4])
        city2[fields[0]] = int(fields[4])

        line = f.readline()
print(f'Cities: {cities}')

# city names
names = list(sorted(cities))
print(f'Names: {names}')

# Extract dists
dists = [[0] * len(names) for i in range(len(names))]
print(f'Dists: {dists}')
c1 = 0
for name in names:
    city1 = cities[name]
    for city2 in city1:
        c2 = names.index(city2)
        print(f'c1: {c1} to c2: {c2} is {city1[city2]}')
        dists[c1][c2] = city1[city2]
    c1 += 1
print(f'Dists: {dists}')

min_dist, min_route = traveling_salesman(dists, home=False, maxdist=True)

print(f'Min route: {min_route}')
total = 0
prev_city = None
for city in min_route:
    dist = cities[prev_city][names[city]] if prev_city is not None else 0
    total += dist
    label = '' if dist == 0 else f'+{dist} = '
    print(f'   {names[city]} [{label}{total}]')
    prev_city = names[city]
print(f'Answer: {min_dist}')
