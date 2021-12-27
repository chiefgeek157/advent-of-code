# Generalizing this for target in any other quadrant than x > 0 and y < 0 got so complex that
# I decided to simplify for just the one quadrant
# That means range is xmin -> xmax and ymax -> ymin

import math

# filename = '2021/day17/test1.txt'; results_filename = '2021/day17/results1.txt'
filename = '2021/day17/input.txt'; results_filename = None

xmin = None
ymin = None
xmax = None
ymax = None
with open(filename, 'r') as f:
    line = f.readline()
    values = line.strip().split(':')[1].split(',')
    x_values = values[0].split('=')[1].split('..')
    y_values = values[1].split('=')[1].split('..')
    xmin = int(x_values[0])
    ymin = int(y_values[0])
    xmax = int(x_values[1])
    ymax = int(y_values[1])
print(f'Target: [{xmin}][{ymin}] -> [{xmax}][{ymax}]')

results = None
if results_filename is not None:
    results = []
    with open(results_filename, 'r') as f:
        line = f.readline()
        while line:
            pairs = line.strip().split()
            for pair in pairs:
                coords = pair.split(',')
                results.append((int(coords[0]), int(coords[1])))
            line = f.readline()

def print_grid(path):
    path_xmax = max([x for x, y in path])
    path_ymin = min([y for x, y in path])
    path_ymax = max([y for x, y in path])
    minx = x0
    maxx = max(path_xmax, xmax)
    miny = min(y0, path_ymin, ymin)
    maxy = max(x0, path_ymax, ymax)
    for y in range(maxy, miny - 1, -1):
        for x in range(minx, maxx + 1):
            if (x, y) in path:
                print('O', end='')
            elif x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                print('#', end='')
            else:
                print('.', end='')
        print()

# def shoot_single_axis(p0, v0, vstep_f, pmin, pmax, vmin):
#     p = p0
#     v = v0
#     # Distance from p0 to pmin and pmax
#     dpmin = min(abs(pmin - p0), abs(pmax - p0))
#     dpmax = max(abs(pmin - p0), abs(pmax - p0))
#     hit = False
#     while True:
#         dp = abs(p - p0)
#         # Stop if we have overshot the target
#         # if p if farther from p0 than pmax is from p0
#         # Works for both positive and negative pmax
#         if dp > dpmax:
#             break
#         elif vmin is not None and v == vmin:
#             break
#         elif dp >= dpmin and dp <= dpmax:
#             hit = True
#             break
#         p += v
#         v = vstep_f(v)

#     return hit

def shoot(px0, py0, vx0, vy0, vxstep_f, vystep_f, txmin, tymin, txmax, tymax):
    # print(f'Checking ({vx0}, {vy0})')
    px = px0
    py = py0
    vx = vx0
    vy = vy0
    path = []
    hit = False
    while True:
        # print(f'P: [{px}, {py}] V: [{vx}, {vy}]')
        path.append((px, py))
        # Overshoot x if px > txmax
        # Overshoot y if py < tymin
        if  px > txmax or py < tymin:
            # print_grid(path)
            # print(f'OVERSHOT vx={vx} py={py}')
            # input('Enter...')
            break
        elif px >= txmin and px <= txmax and py >= tymin and py <= tymax:
            # print_grid(path)
            # print(f'HIT at [{px}, {py}]')
            # input('Enter...')
            hit = True
            break
        px += vx
        py += vy
        vx = vxstep_f(vx)
        vy = vystep_f(vy)

    return hit

# Drag and gravity
# Vx always moves toward zero
def vx_step(vx):
    return int(math.copysign(max(0, (abs(vx) - 1)), vx))

# Vy always decreases
def vy_step(vy):
    return vy - 1

# Starting coords are fixed
x0 = 0
y0 = 0

# Minimum Vx0 is the value so that vx is 0 just as we reach xmin
# It is the solution of sum = n(n + 1)/2 for n
vx0min = math.ceil((math.sqrt(8 * xmin + 1) - 1) / 2)
# Maximum Vx0 hits xmax in one step
vx0max = xmax
# Minimum Vy0 hits ymin in one step (and is negative here)
vy0min = ymin
# Maximum Vy0 is |vy0min| - 1 since on the return downward the
# the next step is one larger in magnitude
vy0max = -ymin - 1
print(f'Vx0 range {vx0min} to {vx0max} Vy0 range {vy0min} to {vy0max}')

hits = []
for vx0 in range(vx0min, vx0max + 1):
    for vy0 in range(vy0min, vy0max + 1):
        if shoot(x0, y0, vx0, vy0, vx_step, vy_step, xmin, ymin, xmax, ymax):
            hits.append((vx0, vy0))
print(f'Hits: {hits}')

# vx0_candidates = []
# for vx0 in range(vx0min, vx0max + 1):
#     if shoot_single_axis(x0, vx0, vx_step, xmin, xmax, vx0min):
#         vx0_candidates.append(vx0)
# print(f'vx0 candidates {vx0_candidates}')

# vy0_candidates = []
# for vy0 in range(vy0min, vy0max + 1):
#     if shoot_single_axis(y0, vy0, vy_step, ymin, ymax, None):
#         vy0_candidates.append(vy0)
# print(f'vy0 candidates {vy0_candidates}')

# hits = []
# for vx0 in vx0_candidates:
#     for vy0 in vy0_candidates:
#         if shoot(x0, y0, vx0, vy0, vx_step, vy_step, xmin, ymin, xmax, ymax):
#             hits.append((vx0, vy0))
# print(f'Hits: {hits}')

if results is not None:
    for hit in hits:
        if hit not in results:
            print(f'{hit} not in results')
    for hit in results:
        if hit not in hits:
            print(f'{hit} not in hits')

print(f'Answer: {len(hits)}')
# x_max_steps = math.floor(math.sqrt(xmin))
# vxs = set()
# for step in range(1, x_max_steps + 1):
#     print(f'step {step}')
#     vxmax = math.floor(xmax / step)
#     vxmin = math.floor(xmin / step)
#     print(f'vxmax {vxmax} vxmin {vxmin}')
#     for vx in range(vxmax, vxmin - 1, -1):
#         print(f'Adding vx {vx}')
#         vxs.add(vx)
# print(f'vxs {vxs}')

# We want to the maximum height theprojectile can reach. horizontal velocity does not matter
# so pick the lowest value that hits the target
#
# It is v such that target.min_x = v ( v + 1 ) / 2
# The next largest integer that solves the equation
# vx_min = math.ceil((math.sqrt(8 * xmin + 1) - 1) / 2)
# For reference, the largest vx is one that lands at the far edge of the target in one step
# vx_max = xmax
# print(f'vx min max = {vx_min} -> {vx_max}')

# vxs = []
# for vx0 in range(vx_min, vx_max + 1):
#     hit = False
#     x = 0
#     vx = vx0
#     while x <= target.max_x and vx >= 0:
#         x += vx
#         if x >= target.min_x and x <= target.max_x:
#             hit = True
#             break
#         vx -= 1
#     if hit:
#         vxs.append(vx0)
# print(f'vxs: {vxs}')

# For y, It is the same, but the effective initial condition is the maximum height rather
# rather than zero, and the values get larger not smaller, so shift the equation to accomodate
#
# For the upward leg, H = vy(vy+1)/2
# dymin = H - ty_max
# dymax = H - ty_min
# vy2_min = ceil((sqrt(8 * dymin) + 1) - 1) / 2)
# vy2_max = floor((sqrt(8 * dymax) + 1) - 1) / 2)
# vy0 = target.min_y
# hit = False
# while not hit:
#     print(f'Starting with {vy0}')
#     vy = vy0
#     y = 0
#     while True:
#         vy -= 1
#         y += vy
#         print(f'{y:3} {vy:3}')
#         if target.contains((target.min_x, y)):
#             hit = True
#             break
#         elif y < target.min_y:
#             break
#     if not hit:
#         vy0 += 1
# if hit:
#     print(f'HIT at {vy0}')

# vy0 = -vy0
# max_height = vy0 * (vy0 + 1) / 2
# print(f'Answer: {max_height}')