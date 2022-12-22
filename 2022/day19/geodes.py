filename = '2022/day19/test1.txt'
# filename = '2022/day19/input.txt'

blueprints = {}
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split(':')
        id = int(fields[0].split()[1])
        params = fields[1].split()
        costs = [int(params[4]), int(params[10]), [int(params[16]), int(params[19])],
            [int(params[25]), int(params[28])]]
        blueprints[id] = costs

        line = f.readline()

print(f'Blueprints: {blueprints}')

def search_max(start, t_limit, next_f, value_f):
    max_value = 0
    max_state = None
    t = 0
    work = set()
    work.add(start)
    while t < t_limit:
        print(f't={t}: work={len(work)}')
        next_work = set()
        for state in work:
            value = value_f(state)
            if value > max_value:
                max_value = value
                max_state = state
            next_states = next_f(state)
            next_work.update(next_states)
        work = next_work
        t += 1
    return (max_value, max_state)

def buy_robots(state, bp):
    """Return the list of all possible purchases before adding this
    round's new resources."""
    # print(f'buy_robots({state})')
    next_states = []
    if state[1] >= bp[0]:
        # print(f'  - Purchase an ore robot')
        state = (
                state[0],
                state[1] - bp[0],
                state[2],
                state[3],
                state[4],
                state[5] + 1,
                state[6],
                state[7],
                state[8]
        )
        next_states.append(state)
        next_states += buy_robots(state, bp)
    if state[1] >= bp[1]:
        # print(f'  - Purchase a clay robot')
        state = (
                state[0],
                state[1] - bp[1],
                state[2],
                state[3],
                state[4],
                state[5],
                state[6] + 1,
                state[7],
                state[8]
        )
        next_states.append(state)
        next_states += buy_robots(state, bp)
    if state[1] >= bp[2][0] and state[2] >= bp[2][1]:
        # print(f'  - Purchase an obsidian robot')
        state = (
                state[0],
                state[1] - bp[2][0],
                state[2] - bp[2][1],
                state[3],
                state[4],
                state[5],
                state[6],
                state[7] + 1,
                state[8]
        )
        next_states.append(state)
        next_states += buy_robots(state, bp)
    if state[1] >= bp[3][0] and state[3] >= bp[2][1]:
        print(f'  - Purchase a geode robot')
        state = (
                state[0],
                state[1] - bp[3][0],
                state[2],
                state[3] - bp[3][1],
                state[4],
                state[5],
                state[6],
                state[7],
                state[8] + 1
        )
        next_states.append(state)
        next_states += buy_robots(state, bp)

    return next_states

def get_next_states(state):
    global blueprints
    # print(f'get_next_states({state})')
    bp = blueprints[state[0]]
    buy_states = buy_robots(state, bp)
    # print(f'  - Add buy nothing state')
    buy_states.append((
            state[0],
            state[1],
            state[2],
            state[3],
            state[4],
            state[5],
            state[6],
            state[7],
            state[8]
    ))

    # Add resoruces to all next states
    next_states = []
    for buy_state in buy_states:
        next_state = (
            buy_state[0],
            buy_state[1] + state[5],
            buy_state[2] + state[6],
            buy_state[3] + state[7],
            buy_state[4] + state[8],
            buy_state[5],
            buy_state[6],
            buy_state[7],
            buy_state[8]
        )
        next_states.append(next_state)

    return next_states

def get_value(state):
    return state[4]

# State = (bp_id, ore, clay, obsidian, geodes, ore_robots, clay_robots,
#   obsidian_robots, geode_robots)
total_value = 0
for id in blueprints:
    state = (id, 0, 0, 0, 0, 1, 0, 0, 0)
    max_value, max_state = search_max(state, 24, get_next_states, get_value)
    total_value += id * max_value

print(f'Part 1: {total_value}')