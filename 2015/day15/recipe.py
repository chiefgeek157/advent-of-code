from itertools import permutations

# filename = '2015/day15/input.txt'
filename = '2015/day15/test1.txt'

data = """Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3
Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3
Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8
Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8"""

# data = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
# Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

TOTAL_WEIGHT = 100
PART_2 = True
CALORIES = 500

ingredients = []
property_names = set()
for line in data.splitlines():
    fields = line.split(':')
    ingredient = {}
    ingredients.append(ingredient)
    ingredient['name'] = fields[0]
    fields = fields[1].split(',')
    for field in fields:
        subfields = field.split()
        property_names.add(subfields[0])
        ingredient[subfields[0]] = int(subfields[1])

# Remove calories
property_names.remove('calories')

print(f'Ingredients: {ingredients}')
num_ingr = len(ingredients)

max_score = 0
max_weights = None
for weights in permutations(range(TOTAL_WEIGHT + 1), num_ingr):

    # Discard combos that do not add to TOTAL_WEIGHT
    if sum(weights) != TOTAL_WEIGHT:
        continue

    if PART_2:
        # Discard combos that do not add to CALORIES
        calories = 0
        for i in range(num_ingr):
            calories += ingredients[i]['calories'] * weights[i]
        if calories != CALORIES:
            continue

    total = 1
    # print(f'{weights}')
    for prop in property_names:
        value = 0
        for i in range(len(weights)):
            value += ingredients[i][prop] * weights[i]
        value = max(0, value)
        # print(f'{weights} {prop} = {value}')
        total *= value
    # print(f'Total: {total}')
    if total > max_score:
        max_score = total
        max_weights = weights
        print(f'New max: {max_score} at {weights}')

print(f'Max score {max_score} at {max_weights}')