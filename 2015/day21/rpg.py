from itertools import combinations

class Player:
    def __init__(self, hit_points: int, damage: int, armor: int) -> None:
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor

player = Player(100, 0, 0)
boss = Player(104, 8, 1)

# player = Player(8, 5, 5)
# boss = Player(12, 7, 2)

weapons = [
    ('Dagger', 8, 4, 0),
    ('Shortsword', 10, 5, 0),
    ('Warhammer', 25, 6, 0),
    ('Longsword', 40, 7, 0),
    ('Greataxe', 74, 8, 0)
]

armors = [
    ('None', 0, 0, 0),
    ('Leather', 13, 0, 1),
    ('Chainmail', 31, 0, 2),
    ('Splintmail', 53, 0, 3),
    ('Bandedmail', 75, 0, 4),
    ('Platemail',102, 0, 5)
]

rings = [
    ('Empty Left', 0, 0, 0),
    ('Empty Right', 0, 0, 0),
    ('Damage +1', 25, 1, 0),
    ('Damage +2', 50, 2, 0),
    ('Damage +3', 100, 3, 0),
    ('Defense +1', 20, 0, 1),
    ('Defense +2', 40, 0, 2),
    ('Defense +3', 80, 0, 3)
]

# Iterator state
weapon = 0
armor = 0
ring_iter = combinations(rings, 2)

def next_combo() -> tuple:
    global ring_iter, weapon, armor
    ring_combo = next(ring_iter, False)
    if not ring_combo:
        # Reset rings
        ring_iter = combinations(rings, 2)
        ring_combo = next(ring_iter, False)

        # Advance armor
        armor += 1
        if armor >= len(armors):
            armor = 0

            # Advance weapon
            weapon += 1
            if weapon >= len(weapons):
                # Out of combos
                return None
    return (weapons[weapon], armors[armor], ring_combo[0], ring_combo[1])

iter = 1000
winner = boss
min_cost = None
combo = next_combo()
while combo and iter >= 0:

    cost = sum(x[1] for x in combo)
    player.damage = sum(x[2] for x in combo)
    player.armor = sum(x[3] for x in combo)

    player_rounds = boss.hit_points / max(1, (player.damage - boss.armor))
    boss_rounds = player.hit_points / max(1, (boss.damage - player.armor))
    if player_rounds <= boss_rounds:
        if min_cost is None or cost < min_cost:
            print(f'New min cost {cost}')
            print(f'Combo {combo} cost {cost}')
            print(f'Player damage {player.damage} armor {player.armor}')
            print(f'Rounds boss {boss_rounds}, player {player_rounds}')
            min_cost = cost

    combo = next_combo()
    iter -= 1

print(f'Ans: player won with {min_cost} gold spent with {iter} iters left')