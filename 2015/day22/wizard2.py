import copy
import sys
from types import SimpleNamespace

class Effect:
    def __init__(self, duration: int, damage: int=0, armor: int=0, heal: int=0, mana: int=0) -> None:
        self.duration = duration
        self.damage = damage
        self.armor = armor
        self.heal = heal
        self.mana = mana

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

class SpellGenerator:

    _cls_index: int = 0
    _spells: list[Spell] = []
    _fixed: bool = False

    @classmethod
    def config(cls, spell_list: list[Spell], fixed: bool) -> None:
        cls._spells = spell_list
        cls._fixed = fixed

    def __init__(self) -> None:
        self._inst_index = 0

    def __iter__(self) -> 'SpellGenerator':
        return self

    def __next__(self) -> Spell:
        if self.index == len(self._spells):
            raise StopIteration
        spell = SpellGenerator._spells[self.index]
        self._incr_index()
        return spell

    @property
    def index(self) -> int:
        return SpellGenerator._cls_index if SpellGenerator._fixed else self._inst_index

    def _incr_index(self) -> None:
        if SpellGenerator._fixed:
            SpellGenerator._cls_index += 1
        else:
            self._inst_index += 1

def copy_boss(boss) -> object:
    new_boss = SimpleNamespace()
    new_boss.hp = boss.hp
    new_boss.damage = boss.damage
    return new_boss

def apply_effects(wizard: object, effects: dict) -> None:
    wizard.effects = {}
    for name, effect in effects.items():
        print(f'Applying effect {name}')
        wizard.hp += effect.heal
        wizard.mana += effect.mana
        wizard.damage += effect.damage
        wizard.armor += effect.armor
        if effect.duration > 1:
            wizard.effects[name] = Effect(effect.duration - 1, effect.damage, effect.armor, effect.heal, effect.mana)
            print(f'Effect {name} timer is now {effect.duration - 1}')
        else:
            print(f'Effect {name} wore off')

def wizard_turn(wizard: object, boss: object, spell: object) -> tuple:

    new_wizard = SimpleNamespace()
    new_wizard.hp = wizard.hp + spell.heal
    new_wizard.mana = wizard.mana - spell.cost + spell.mana
    new_wizard.damage = spell.damage
    new_wizard.armor = spell.armor

    # Apply wizard effects
    apply_effects(new_wizard, wizard.effects)

    # Add new spell to new effects if applicable
    if spell.effect is not None:
        # Sanity check
        if spell.name in new_wizard.effects:
            raise Exception(f'Trying to add effects spell {spell.name} twice')
        new_wizard.effects[spell.name] = Effect(spell.effect.duration, spell.effect.damage,
            spell.effect.armor, spell.effect.heal, spell.effect.mana)
        print(f'Added effect {spell.name} with timer {spell.effect.duration}')

    # Now attack Boss
    new_boss = SimpleNamespace()
    new_boss.hp = boss.hp - new_wizard.damage
    new_boss.damage = boss.damage
    if new_boss.hp <= 0:
        new_boss = None
    # print(f'{" "*level}New {new_boss}')

    return (new_wizard, new_boss)

def boss_turn(wizard: object, boss: object) -> tuple:

    new_wizard = SimpleNamespace()
    new_wizard.hp = wizard.hp
    new_wizard.mana = wizard.mana
    new_wizard.damage = 0
    new_wizard.armor = 0

    # Apply wizard effects
    apply_effects(new_wizard, wizard.effects)

    # Now attack the Boss with effects damage
    new_boss = SimpleNamespace()
    new_boss.hp = boss.hp - new_wizard.damage
    new_boss.damage = boss.damage
    if new_boss.hp <= 0:
        new_boss = None
    # print(f'{" "*level}New {new_boss}')

    if new_boss is not None:
        # Now attack Wizard
        new_wizard.hp -= max(1, new_boss.damage - new_wizard.armor)
        if new_wizard.hp <= 0:
            new_wizard = None

    return (new_wizard, new_boss)

def play_round(wizard: object, boss: object, cum_mana: int, min_mana: int, spell_path: str) -> int:
    for spell in SpellGenerator():
        new_cum_mana = cum_mana + spell.cost
        new_spell_path = spell_path + spell.name[0]
        if new_cum_mana < min_mana and spell.cost <= wizard.mana and (
                spell.name not in wizard.effects or wizard.effects[spell.name].duration == 1):
            new_wizard, new_boss = wizard_turn(wizard, boss, spell)
            if new_boss is None:
                print(f'Wizard won {new_cum_mana} {new_spell_path}')
                min_mana = min(min_mana, new_cum_mana)
            else:
                new_wizard, new_boss = boss_turn(new_wizard, new_boss)
                if new_boss is None:
                    print(f'Wizard won {new_cum_mana} {new_spell_path}')
                    min_mana = min(min_mana, new_cum_mana)
                elif new_wizard is not None:
                    min_mana = play_round(new_wizard, new_boss, new_cum_mana, min_mana, new_spell_path)
    return min_mana

all_spells = [
    Spell('Magic Missle', cost=53, damage=4),
    Spell('Drain', cost=73, damage=2, heal=2),
    Spell('Shield', cost=113, effect=Effect(duration=6, armor=7)),
    Spell('Poison', cost=173, effect=Effect(duration=6, damage=3)),
    Spell('Recharge', cost=229, effect=Effect(duration=5, mana=101))
]

wizard = SimpleNamespace()
wizard.effects = {}

boss = SimpleNamespace()

# Input
wizard.hp = 50
wizard.mana = 500
boss.hp = 51
boss.damage = 8
spell_list = [0, 1, 2, 3, 4]
fixed = False

# Test 1
# wizard.hp = 10
# wizard.mana = 250
# boss.hp = 13
# boss.damage = 8
# spell_list = [3, 0]
# fixed = True

# Test 2
# wizard.hp = 10
# wizard.mana = 250
# boss.hp = 14
# boss.damage = 8
# spell_list = [4, 2, 1, 3, 0]
# fixed = True

# Test 3
# wizard.hp = 50
# wizard.mana = 500
# boss.hp = 51
# boss.damage = 8
# spell_list = [3, 4, 0, 3, 0, 0, 0]
# fixed = True

SpellGenerator.config(list(map(lambda x: all_spells[x], spell_list)), fixed)

min_mana = play_round(wizard, boss, 0, sys.maxsize, '')

print(f'Ans: {min_mana}')