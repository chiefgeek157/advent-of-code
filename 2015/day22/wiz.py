from sys import maxsize

wiz_hp = 50
wiz_mana = 500

# boss_hp = 51
boss_hp = 1
boss_damage = 9

spells = 'MDSPR'
costs = {'M': 53, 'D': 73, 'S': 113, 'P': 173, 'R': 229 }

def round(wiz_turn, wizard_hp, boss_hp, mana, spell, shield_t, poison_t,
        recharge_t, cum_cost, cum_spells) -> int:
    """Return additional cost to win"""
    global spells, costs, boss_damage

    # print(f'WT:{wiz_turn}, WHP:{wizard_hp}, BHP:{boss_hp}, M:{mana}, S:{spell}'
    #     f', ST:{shield_t}, PT:{poison_t}, RT:{recharge_t}, CC:{cum_cost}'
    #     f', CS:{cum_spells}')
    cost = costs[spell] if spell is not None else 0

    # Effects apply regardless of whose turn it is
    boss_hp -= 3 if poison_t > 0 else 0
    armor = 7 if shield_t > 0 else 0
    mana += 101 if recharge_t > 0 else 0
    shield_t = max(0, shield_t - 1)
    poison_t = max(0, poison_t - 1)
    recharge_t = max(0, recharge_t - 1)

    if boss_hp <= 0:
        print(f'Won for {cum_cost + cost}')
        return cum_cost + cost

    if wiz_turn:
        boss_hp -= 4 if spell == 'M' else 0
        boss_hp -= 2 if spell == 'D' else 0
        wizard_hp += 2 if spell == 'D' else 0
        shield_t += 6 if spell == 'S' and shield_t == 0 else 0
        poison_t += 6 if spell == 'P' and poison_t == 0 else 0
        recharge_t += 5 if spell == 'R' and recharge_t == 0 else 0
        if boss_hp <= 0:
            print(f'Won for {cum_cost + cost}')
            return cum_cost + cost

        return round(not wiz_turn, wizard_hp, boss_hp, mana - cost,
            None, shield_t, poison_t, recharge_t,
            cum_cost + cost, cum_spells + spell)
    else:
        wizard_hp -= max(1, boss_damage - armor)
        if wizard_hp <= 0:
            # print(f'Lost')
            return maxsize

        min_cost = maxsize
        for next_spell in spells:
            # Keep going if Wizard can afford the next spell and
            # the cummulative cost plus the next spell is less than the
            # minimum cost already found
            next_spell_cost = costs[next_spell]
            if next_spell_cost <= mana and cum_cost + next_spell_cost < min_cost:
                min_cost = min(min_cost,
                    round(not wiz_turn, wizard_hp, boss_hp, mana,
                    next_spell, shield_t, poison_t, recharge_t,
                    cum_cost, cum_spells))
        return min_cost

min_cost = maxsize
for spell in spells:
    min_cost = min(min_cost,
        round(True, wiz_hp, boss_hp, wiz_mana, spell, 0, 0, 0, 0, ''))

print(F'Ans: {min_cost}')