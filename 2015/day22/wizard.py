import copy
import functools
import sys

class Effect:
    def __init__(self, duration: int, damage: int=0, armor: int=0, heal: int=0, mana: int=0) -> None:
        self.duration = duration
        self.damage = damage
        self.armor = armor
        self.heal = heal
        self.mana = mana

    def use(self) -> tuple:
        """Return a tuple of (duration, damage, armor, heal, mana).

        Duration is the new duration. If zero, then no longer valid."""
        return (self.duration - 1, self.damage, self.armor, self.heal, self.mana)

    def __repr__(self) -> str:
        return f'Dur:{self.duration} Dam:{self.damage} Arm:{self.armor} Hea:{self.heal} Man:{self.mana}'


class Spell:
    def __init__(self, name: str, cost: int, damage: int=0, armor: int=0, heal: int=0, mana: int=0,
            effect: Effect=None) -> None:
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor
        self.heal = heal
        self.mana = mana
        self.effect = effect

    def __repr__(self) -> str:
        return f'{self.name}'


class Boss:
    def __init__(self, hp: int, damage: int) -> None:
        self.hp = hp
        self.damage = damage

    def attack(self, level: int, wizard: 'Wizard') -> 'Wizard':
        """Return a new Wizard with attack applied of None if Wizard lost"""
        # print(f'{" "*level}{self} attacking {wizard}')

        new_boss = copy.copy(self)

        # Clone the Wizard and apply effects
        new_wizard = wizard.clone()
        effects_damage, effects_armor = new_wizard.apply_effects()

        # Wizard effects cause damage every melee
        new_boss.hp -= effects_damage
        if new_boss.hp <= 0:
            new_boss = None
        else:
            # Attack the new Wizard
            new_wizard.hp -= max(1, new_boss.damage - effects_armor)
            if new_wizard.hp <= 0:
                new_wizard = None

        return (new_wizard, new_boss)

    def __repr__(self) -> str:
        return f'Boss: hp:{self.hp} d:{self.damage}'


class Wizard:
    def __init__(self, hp: int, mana: int) -> None:
        self.hp = hp
        self.mana = mana
        self.armor = 0
        self.effects = {}

    def clone(self) -> 'Wizard':
        new_self = Wizard(self.hp, self.mana)
        new_self.armor = self.armor
        new_self.effects = copy.deepcopy(self.effects)
        return new_self

    def attack(self, level: int, spell: Spell, boss: Boss) -> tuple:
        """Return a tuple of (Boss, Wizard) after attack.

        Boss is None if lost."""
        # print(f'{" "*level}{wizard} attacking {boss} with {spell}')
        new_boss = copy.copy(boss)
        new_self = self.clone()

        # Apply immediate effects to self
        new_self.mana = max(0, new_self.mana - spell.cost)
        new_self.hp += spell.heal
        new_self.armor = spell.armor
        new_self.mana += spell.mana

        # Apply effects
        effects_damage, effects_armor = new_self.apply_effects()
        new_self.armor += effects_armor

        # Add spell to new effects
        if spell.effect is not None:
            # Sanity check
            if spell.name in new_self.effects:
                raise Exception(f'Spell with effect {spell.name} already in list')
            new_self.effects[spell.name] = spell.effect

        # Now attack Boss
        new_boss.hp -= spell.damage + effects_damage
        if new_boss.hp <= 0:
            new_boss = None
        # print(f'{" "*level}New {new_boss}')

        return (new_boss, new_self)

    def apply_effects(self) -> tuple:
        effects_damage = 0
        effects_armor = 0
        new_effects = {}
        for name, effect in self.effects.items():
            duration, damage, armor, heal, mana = effect.use()

            self.hp += heal
            self.mana += mana
            effects_damage += damage
            effects_armor += armor
            if duration > 0:
                new_effects[name] = Effect(duration, damage, armor, heal, mana)
        self.effects = new_effects

        return (effects_damage, effects_armor)

    def __repr__(self) -> str:
        return f'Wizard: hp:{self.hp} m:{self.mana} e:{self.effects}'

def play_round(level: int, wizard: Wizard, boss: Boss, spell: Spell, cum_mana: int) -> tuple:
    """Play a round, Wizard then Boss.

    Return (wizard, boss, total_mana)"""
    # print(f'{" "*level}Round: {wizard}, {boss}, {spell}, cum_mana {cum_mana}')

    # Wizard turn
    new_mana = cum_mana + spell.cost
    new_boss, new_wizard = wizard.attack(level, spell, boss)
    # print(f'{" "*level}New {new_boss} {new_wizard}')
    if new_boss:
        new_wizard, new_boss = new_boss.attack(level, new_wizard)
    return (new_wizard, new_boss, new_mana)

def try_spells(level: int, spell_path: list[str], wizard: Wizard, boss: Boss, cum_mana: int):
    """Cast all possible spells in order."""
    global min_mana, min_spell_path

    # print(f'Try spells at {functools.reduce(lambda x, y: x + y[0], spell_path)}')

    spell_index = 0
    spell_index, spell = next_spell(spell_index)
    while spell:
        if cum_mana + spell.cost < min_mana and spell.name not in wizard.effects:
            new_spell_path = spell_path + [spell.name]
            new_wizard, new_boss, new_cum_mana = play_round(level, wizard, boss, spell, cum_mana)
            if not new_boss:
                # print(f'{" "*level}Wizard won')
                if new_cum_mana < min_mana:
                    print(f'{" "*level}New min mana {new_cum_mana}')
                    min_mana = new_cum_mana
                    min_spell_path = new_spell_path
            elif not new_wizard:
                # print(f'{" "*level}Boss won')
                pass
            else:
                try_spells(level + 1, new_spell_path, new_wizard, new_boss, new_cum_mana)
        spell_index, spell = next_spell(spell_index)

spells = [
    Spell('Magic Missle', cost=53, damage=4),
    Spell('Drain', cost=73, damage=2, heal=2),
    Spell('Shield', cost=113, effect=Effect(duration=6, armor=7)),
    Spell('Poison', cost=173, effect=Effect(duration=6, damage=3)),
    Spell('Recharge', cost=229, effect=Effect(duration=5, mana=101))
]

def spell_round_robin(index: int) -> tuple:
    """Return the tuple (new_idex, spell)"""
    global spells, spell_list
    spell = None
    if index < len(spell_list):
        spell = spells[spell_list[index]]
    return (index + 1, spell)

spell_index = 0
def spell_sequence(index: int) -> tuple:
    """Return a global sequence, ignoring local index"""
    global spells, spell_list, spell_index
    spell = None
    if spell_index < len(spell_list):
        spell = spells[spell_list[spell_index]]
    spell_index += 1
    return (index, spell)

# Input
# play_hp = 50
# play_mana = 500
# boss_hp = 51
# boss_damage = 9
# spell_list = [0, 1, 2, 3, 4]
# next_spell = spell_round_robin
# End Input

# Test 1
# play_hp = 10
# play_mana = 250
# boss_hp = 13
# boss_damage = 8
# spell_list = [3, 0]
# next_spell = spell_sequence
# End Test 1

# Test 2
play_hp = 10
play_mana = 250
boss_hp = 14
boss_damage = 8
spell_list = [4, 2, 1, 3, 0]
next_spell = spell_sequence
# End Test 1

# Test 3
# play_hp = 50
# play_mana = 500
# boss_hp = 51
# boss_damage = 9
# spell_list = [0, 3, 0, 0, 2, 3, 0, 0]
# next_spell = spell_sequence
# End Test 1

min_mana = sys.maxsize
min_spell_path = None

wizard = Wizard(play_hp, play_mana)
boss = Boss(boss_hp, boss_damage)
print(f'START: {wizard} {boss}')

try_spells(0, [''], wizard, boss, 0)

print(f'Ans: {min_mana} with {min_spell_path}')
