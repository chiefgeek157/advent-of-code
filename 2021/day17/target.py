import math

#filename = '2021/day17/test1.txt'
filename = '2021/day17/input.txt'

class Target:
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def contains(self, point):
        if  point is not None and \
            point[0] >= self.min_x and point[0] <= self.max_x and \
            point[1] >= self.min_y and point[1] <= self.max_y:
            return True
        return False

    def __repr__(self):
        return f'[{self.min_x}][{self.min_y}] to [{self.max_x}][{self.max_y}]'

target = None
with open(filename, 'r') as f:
    line = f.readline()
    values = line.strip().split(':')[1].split(',')
    x_values = values[0].split('=')[1].split('..')
    y_values = values[1].split('=')[1].split('..')
    target = Target(int(x_values[0]), int(y_values[0]), int(x_values[1]), int(y_values[1]))
print(f'Target: {target}')
# We want to the maximum height theprojectile can reach. horizontal velocity does not matter
# so pick the lowest value that hits the target
#
# It is v such that target.min_x = v ( v + 1 ) / 2
# The next largest integer that solves the equation
vx_min = math.ceil((math.sqrt(8 * target.min_x + 1) - 1) / 2)
# For reference, the largest vx is one that lands at the far edge of the target in one step
vx_max = target.max_x
print(f'vx min max = {vx_min} -> {vx_max}')

# For y, It is the same, but the effective initial condition is the maximum height rather
# rather than zero, and the values get larger not smaller, so shift the equation to accomodate
#
# For the upward leg, H = vy(vy+1)/2
# dymin = H - ty_max
# dymax = H - ty_min
# vy2_min = ceil((sqrt(8 * dymin) + 1) - 1) / 2)
# vy2_max = floor((sqrt(8 * dymax) + 1) - 1) / 2)
vy0 = target.min_y
hit = False
while not hit:
    print(f'Starting with {vy0}')
    vy = vy0
    y = 0
    while True:
        vy -= 1
        y += vy
        print(f'{y:3} {vy:3}')
        if target.contains((target.min_x, y)):
            hit = True
            break
        elif y < target.min_y:
            break
    if not hit:
        vy0 += 1
if hit:
    print(f'HIT at {vy0}')

vy0 = -vy0
max_height = vy0 * (vy0 + 1) / 2
print(f'Answer: {max_height}')