import math
import sys

player_hp = 100
boss_hp = 104
boss_damage = 8
boss_armor = 1

# Test
# player = Player(100, 0, 0)
# boss = Player(103, 9, 2)

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
    ('None', 0, 0, 0),
    ('Damage +1', 25, 1, 0),
    ('Damage +2', 50, 2, 0),
    ('Damage +3', 100, 3, 0),
    ('Defense +1', 20, 0, 1),
    ('Defense +2', 40, 0, 2),
    ('Defense +3', 80, 0, 3)
]

max_cost = 0
for weapon in range(len(weapons)):
    for armor in range(len(armors)):
        for l_ring in range(len(rings)):
            for r_ring in range(len(rings)):
                cost = weapons[weapon][1] + armors[armor][1] + rings[l_ring][1] + rings[r_ring][1]
                player_damage = weapons[weapon][2] + armors[armor][2] + rings[l_ring][2] + rings[r_ring][2]
                player_armor = weapons[weapon][3] + armors[armor][3] + rings[l_ring][3] + rings[r_ring][3]

                boss_killed_rounds = math.ceil(boss_hp / max(1, (player_damage - boss_armor)))
                player_killed_rounds = math.ceil(player_hp / max(1, (boss_damage - player_armor)))
                if player_killed_rounds < boss_killed_rounds:
                    if cost > max_cost:
                        print(f'New max cost {cost}')
                        max_cost = cost

print(f'Ans: player lost with {max_cost} gold')