from sys import maxsize

part2 = True

wiz_hp = 50
wiz_mana = 500

boss_hp = 51
boss_damage = 9

spells = 'MDSPR'
costs = {'M': 53, 'D': 73, 'S': 113, 'P': 173, 'R': 229 }

def round(min_cost, wiz_turn,
        wizard_hp, boss_hp, mana, spell,
        shield_t, poison_t, recharge_t,
        cum_cost, cum_spells) -> int:
    """Return additional cost to win"""
    global spells, costs, boss_damage, part2

    cum_spells += spell if spell is not None else ''
    # print(f'{cum_spells} MC:{min_cost} WT:{wiz_turn}, WHP:{wizard_hp}, BHP:{boss_hp}, M:{mana}, S:{spell}'
    #     f', ST:{shield_t}, PT:{poison_t}, RT:{recharge_t}, CC:{cum_cost}')

    if part2 and wiz_turn:
        wizard_hp -= 1
        if wizard_hp <= 0:
            # Wizard lost
            # print(f'{cum_spells} Lost')
            return (maxsize, cum_spells)

    cost = costs[spell] if spell is not None else 0
    if wiz_turn:
        if cost > mana:
            # Truncate this branch based on cost
            # print(f'{cum_spells} Lost not enough mana')
            return (maxsize, cum_spells)
        if wiz_turn and cum_cost + cost > min_cost:
            # Truncate this branch based on cost
            # print(f'{cum_spells} Lost greater than min cost {cum_cost + cost}')
            return (maxsize, cum_spells)

    # Effects apply regardless of whose turn it is
    boss_hp -= 3 if poison_t > 0 else 0
    if boss_hp <= 0:
        # Wizard won, candidate min cost is cum cost + cost
        # print(f'{cum_spells} Won for {cum_cost + cost}')
        return (min(min_cost, cum_cost + cost), cum_spells)

    armor = 7 if shield_t > 0 else 0
    mana += 101 if recharge_t > 0 else 0
    shield_t = max(0, shield_t - 1)
    poison_t = max(0, poison_t - 1)
    recharge_t = max(0, recharge_t - 1)

    if wiz_turn:
        boss_hp -= 4 if spell == 'M' else 0
        boss_hp -= 2 if spell == 'D' else 0
        if boss_hp <= 0:
            # Wizard won, candidate min cost is cum cost + cost
            # print(f'{cum_spells} Won for {cum_cost + cost}')
            return (min(min_cost, cum_cost + cost), cum_spells)

        wizard_hp += 2 if spell == 'D' else 0
        shield_t += 6 if spell == 'S' and shield_t == 0 else 0
        poison_t += 6 if spell == 'P' and poison_t == 0 else 0
        recharge_t += 5 if spell == 'R' and recharge_t == 0 else 0

        return round(min_cost, not wiz_turn,
            wizard_hp, boss_hp, mana - cost, None,
            shield_t, poison_t, recharge_t,
            cum_cost + cost, cum_spells)
    else:
        wizard_hp -= max(1, boss_damage - armor)
        if wizard_hp <= 0:
            # Wizard lost
            # print(f'{cum_spells} Lost')
            return (maxsize, cum_spells)

        min_spells = cum_spells
        for next_spell in spells:
            next_min_cost, next_min_spells = round(min_cost, not wiz_turn,
                    wizard_hp, boss_hp, mana,
                    next_spell, shield_t, poison_t, recharge_t,
                    cum_cost, cum_spells)
            if next_min_cost < min_cost:
                min_cost = next_min_cost
                min_spells = next_min_spells
                print(f'{cum_spells} NEW MIN {min_cost}')
        return (min_cost, min_spells)

min_cost = maxsize
min_spells = ''
for spell in spells:
    if costs[spell] <= min_cost:
        next_min_cost, next_min_spells = round(min_cost, True,
            wiz_hp, boss_hp, wiz_mana, spell,
            0, 0, 0, 0, '')
        if next_min_cost < min_cost:
            min_cost = next_min_cost
            min_spells = next_min_spells
            print(f'NEW MIN {min_cost} @ {min_spells}')

print(F'Ans: {min_cost} @ {min_spells}')