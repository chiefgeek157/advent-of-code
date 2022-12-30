import heapq

filename = '2022/day19/test1.txt'
# filename = '2022/day19/input.txt'

time_limit = 24

# Blueprint: costs of robots: [ore_r, clay_r, obs_r, geo_r]
# [ore, ore, [ore, clay], [ore, clay]]
blueprints = {}
bp_values = {}
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split(':')
        id = int(fields[0].split()[1])
        params = fields[1].split()
        costs = [int(params[4]), int(params[10]), [int(params[16]), int(params[19])],
            [int(params[25]), int(params[28])]]
        blueprints[id] = costs
        ore_value = 1
        clay_value = ore_value * costs[1]
        obsidian_value = ore_value * costs[2][0] + clay_value * costs[2][1]
        geode_value = ore_value * costs[3][0] + obsidian_value * costs[3][1]
        bp_values[id] = (ore_value, clay_value, obsidian_value, geode_value)

        line = f.readline()

print(f'Blueprints: {blueprints}')

push_count = 0
def pushitem(queue, value, item):
    global push_count
    heapq.heappush(queue, (-value, push_count, item))
    push_count += 1

def popitem(queue):
    value, count, item = heapq.heappop(queue)
    return (-value, count, item)

# State = (bp_id, time, ore, clay, obsidian, geodes, ore_robots, clay_robots,
#   obsidian_robots, geode_robots)
def best_first(start, next_f, objective_f):
    priority_queue = []
    max_objective = 0
    max_node = None
    predecessors = {start: None}
    best_scores = {start: 0}

    pushitem(priority_queue, 0, start)
    while priority_queue:
        score, count, node = popitem(priority_queue)
        print(f'Visiting {node} with value {score} count {count}')
        obejctive = objective_f(node)
        if obejctive > max_objective:
            print(f'  - New max objective {obejctive} at {node}')
            max_objective = obejctive
            max_node = node
        next_items = next_f(node, max_node)
        for next_item in next_items:
            next_node, score = next_item
            best_score = best_scores.get(next_node, -1)
            if score > best_score:
                best_scores[next_node] = score
                predecessors[next_node] = node
                print(f'Queueing item {next_node} with score {score}')
                pushitem(priority_queue, score, next_node)

    max_path = []
    node = max_node
    while node is not None:
        max_path.append(node)
        node = predecessors[node]

    return (max_objective, max_path)

# State = (bp_id, time, ore, clay, obsidian, geodes, ore_robots, clay_robots,
#   obsidian_robots, geode_robots)
def buy_robots(state, next_t, bp):
    """Return the list of all possible purchases before adding this
    round's new resources."""
    # print(f'buy_robots({state})')
    bp_id, t, ore, cla, obs, geo, ore_r, cla_r, obs_r, geo_r = state
    next_states = []
    if ore >= bp[0]:
        # print(f'  - Purchase an ore robot')
        state = (bp_id, next_t, ore - bp[0], cla, obs, geo, ore_r + 1, cla_r, obs_r, geo_r)
        next_states.append(state)
        next_states += buy_robots(state, next_t, bp)
    if ore >= bp[1]:
        # print(f'  - Purchase a clay robot')
        state = (bp_id, next_t, ore - bp[1], cla, obs, geo, ore_r, cla_r + 1, obs_r, geo_r)
        next_states.append(state)
        next_states += buy_robots(state, next_t, bp)
    if ore >= bp[2][0] and cla >= bp[2][1]:
        # print(f'  - Purchase an obsidian robot')
        state = (bp_id, next_t, ore - bp[2][0], cla - bp[2][1], obs, geo, ore_r, cla_r, obs_r + 1, geo_r)
        next_states.append(state)
        next_states += buy_robots(state, next_t, bp)
    if ore >= bp[3][0] and obs >= bp[3][1]:
        print(f'  - Purchase a geode robot')
        state = (bp_id, next_t, ore - bp[3][0], cla, obs - bp[3][1], geo, ore_r, cla_r, obs_r, geo_r + 1)
        next_states.append(state)
        next_states += buy_robots(state, next_t, bp)
    return next_states

# State = (bp_id, time, ore, clay, obsidian, geodes, ore_robots, clay_robots,
#   obsidian_robots, geode_robots)
def get_next_states(state, best_state):
    """Return a list of (state, value)."""
    global blueprints
    # print(f'get_next_states({state})')
    bp_id, t, ore, cla, obs, geo, ore_r, cla_r, obs_r, geo_r = state
    bp = blueprints[bp_id]
    next_t = t + 1
    if next_t == time_limit:
        # Out of time
        return []
    if best_state is not None:
        best_bp_id, best_t, best_ore, best_cla, best_obs, best_geo, best_ore_r, best_cla_r, best_obs_r, best_geo_r = best_state
        if (
            geo <= best_geo
            and (geo + geo_r * (time_limit - next_t)) < (best_geo + best_geo_r * (time_limit - best_t))
        ):
            return []

    buy_states = buy_robots(state, next_t, bp)
    # print(f'  - Add buy nothing state')
    next_state = (bp_id, next_t, ore, cla, obs, geo, ore_r, cla_r, obs_r, geo_r)
    buy_states.append(next_state)

    # Add resoruces to all next states and get value
    next_states = []
    for bs in buy_states:
        next_state = (bs[0], bs[1], bs[2] + ore_r, bs[3] + cla_r, bs[4] + obs_r, bs[5] + geo_r, bs[6], bs[7], bs[8], bs[9])
        value = get_value(next_state)
        next_states.append((next_state, value))

    return next_states

# State = (bp_id, time, ore, clay, obsidian, geodes, ore_robots, clay_robots,
#   obsidian_robots, geode_robots)
def get_value(state):
    global bp_values
    bp_id, t, ore, cla, obs, geo, ore_r, cla_r, obs_r, geo_r = state
    bp = blueprints[bp_id]
    values = bp_values[bp_id]
    # value = (
    #     ore * values[0]
    #     + cla * values[1]
    #     + obs * values[2]
    #     + geo * values[3]
    #     + (
    #             ore_r * values[0]
    #             + cla_r * values[1]
    #             + obs_r * values[2]
    #             + geo_r * values[3]
    #         ) * (time_limit - t)
    #     )
    # value = (geo + geo_r * (time_limit - t)
    #     + (obs + obs_r) / bp[3][1] * max(0, (time_limit - t - 1))
    #     + (cla + cla_r) / bp[3][1] / bp[2][1] * max(0, time_limit - t - 2)
    #     + (ore + ore_r) / bp[3][1] / bp[2][1] / bp[1] * max(0, time_limit - t - 3)
    #     )
    value = (
        geo + geo_r * (time_limit - t - 1)
        + (obs / bp[3][1] + obs_r / bp[3][1] * max(0, time_limit - t - 1)) * max(0, time_limit - t - 2)
        + (cla / bp[3][1] / bp[2][1] + cla_r / bp[3][1] / bp[2][1] * max(0, time_limit - t - 2)) * max(0, time_limit - t - 3)
        + (ore / bp[3][1] / bp[2][1] / bp[1] + ore_r / bp[3][1] / bp[2][1] / bp[1] * max(0, time_limit - t - 3)) * max(0, time_limit - t - 4)
    ) / (time_limit - t)
    return value

def objective(state):
    return state[5]

# State = (bp_id, time, ore, clay, obsidian, geodes, ore_robots, clay_robots,
#   obsidian_robots, geode_robots)
total_value = 0
for id in blueprints:
    state = (id, 0, 0, 0, 0, 0, 1, 0, 0, 0)
    max_value, max_path = best_first(state, get_next_states, objective)
    total_value += id * max_value

print(f'Part 1: {total_value}')