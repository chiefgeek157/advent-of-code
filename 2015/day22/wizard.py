import copy
import sys

play_hp = 50
play_mana = 500

boss_hp = 51
boss_damage = 9


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
        return (self.druation - 1, self.damage, self.armor, self.heal, self.mana)

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

    def cast(self) -> tuple:
        """Return the immediate effects on damage, armor, hp, and mana
        and any Effect."""
        return (self.damage, self.armor, self.heal, self.mana, self.effect)


class Boss:
    def __init__(self, hp: int, damage: int) -> None:
        self.hp = hp
        self.damage = damage

    def attack(self, wizard: 'Wizard') -> 'Wizard':
        """Return a new Wizard with attack applied of None if Wizard lost"""
        new_wizard = wizard.clone()
        new_wizard.hp -= max(1, self.damage - new_wizard.armor)
        if new_wizard.hp <= 0:
            new_wizard = None
        return new_wizard

    def __repr__(self) -> str:
        return f'Boss: hp:{self.hp} d:{self.damage}'


class Wizard:
    def __init__(self, hp: int, mana: int) -> None:
        self.hp = hp
        self.mana = mana
        self.damage = 0
        self.armor = 0
        self.effects = []

    def clone(self) -> 'Wizard':
        new_self = Wizard(self.hp, self.mana)
        new_self.damage = self.damage
        new_self.armor = self.armor
        new_self.effects = copy.deepcopy(self.effects)
        return new_self

    def attack(self, spell: Spell, boss: Boss) -> tuple:
        """Return a tuple of (Boss, Wizard) after attack.

        Boss is None if lost."""
        new_boss = copy.copy(boss)
        new_self = Wizard(self.hp, self.mana)

        # Apply wizard effects
        for effect in self.effects:
            duration, damage, armor, heal, mana = effect.use()

            # Apply to new Boss
            new_boss.hp -= damage
            if new_boss.hp <= 0:
                new_boss = None

            # Apply to new self
            new_self.hp += heal
            new_self.damage = damage
            new_self.armor = armor
            new_self.mana += mana
            if duration > 0:
                new_self.effects.append(Effect(duration, damage, armor, heal, mana))

        return (new_boss, new_self)

    def __repr__(self) -> str:
        return f'Wizard: hp:{self.hp} d:{self.damage} a:{self.armor} m:{self.mana} e:{self.effects}'

def play_round(wizard_turn: bool, wizard: Wizard, boss: Boss, total_mana):
    """Play a round, returning the amount of mana used if Wizard won, or None."""
    print(f'Round: {wizard_turn} {wizard}, {boss}, mana:{total_mana}')
    if wizard_turn:
        for spell in spells:
            if wizard.mana >= spell.cost:
                total_mana += spell.cost
                new_boss, new_wizard = wizard.attack(spell, boss)
                if not new_boss:
                    print('Wizard won')
                elif not new_wizard:
                    print(f'Boss won with {total_mana} mana')
                else:
                    play_round(not wizard_turn, new_wizard, new_boss, total_mana)
    else:
        new_wizard = boss.attack(wizard)
        if not new_wizard:
            print("Boss won")
        else:
            play_round(not wizard_turn, new_wizard, boss, total_mana)

spells = [
    Spell('Magic Missle', cost=53, damage=4),
    Spell('Drain', cost=73, damage=2, heal=2),
    Spell('Shield', cost=113, effect=Effect(duration=6, armor=7)),
    Spell('Poison', cost=173, effect=Effect(duration=6, damage=3)),
    Spell('Recharge', cost=229, effect=Effect(duration=5, mana=101))
]

wizard = Wizard(play_hp, play_mana)
boss = Boss(boss_hp, boss_damage)
print(f'START: {wizard} {boss}')

play_round(True, wizard, boss, 0)

# min_mana = sys.maxsize


# work = set()
# initial = Node.get(True, play_hp, boss_hp, play_mana, 0, 0, 0)
# print(f'INitial state: {initial}')
# work.add(initial)
# while work:
#     # Get the least expensive option
#     node = sorted(work, key=lambda x: x.weight())[0]
#     work.remove(node)
#     print(f'Node: {node}')
#     node.visited = True

#     for spell in spells:
#         neighbor = Node.get()

# class State:

#     def __init__(self, play_turn: bool, play_hp: int, boss_hp:int, mana: int,
#             shield: Effect, poison: Effect, recharge: Effect) -> None:
#         self.visited = False
#         self.cost = cost
#         self.play_turn = play_turn
#         self.play_hp = play_hp
#         self.boss_hp = boss_hp
#         self.mana = mana
#         self.shield = shield
#         self.poison = poison
#         self.recharge = recharge

#     def weight(self):
#         return self.cost + self.boss_hp

#     def __repr__(self) -> str:
#         return (f'Cost:{self.cost} Turn:{self.play_turn} PHP:{self.play_hp} BHP: {self.boss_hp}'
#             f' Mana:{self.mana} Shield:{self.shield} Poison:{self.poison} Recharge:{self.recharge}')

#     def __hash__(self) -> int:
#         return hash((self.play_turn, self.play_hp, self.boss_hp, self.mana,
#             self.shield.duration, self.poison.duration, self.recharge.duration))
# class Node:

#     __nodes = set()

#     @classmethod
#     def get(cls, cost, play_turn: bool, play_hp: int, boss_hp:int, mana: int,
#             shield: Effect, poison: Effect, recharge: Effect) -> 'Node':
#         node = Node(cost, play_turn, play_hp, boss_hp, mana, shield, poison, rechargey)
#         if node not in cls.__nodes:
#             cls.__nodes.add(node)
#         return node

#     def __init__(self, cost, play_turn: bool, play_hp: int, boss_hp:int, mana: int,
#             shield: Effect, poison: Effect, recharge: Effect) -> None:
#         self.visited = False
#         self.cost = cost
#         self.play_turn = play_turn
#         self.play_hp = play_hp
#         self.boss_hp = boss_hp
#         self.mana = mana
#         self.shield = shield
#         self.poison = poison
#         self.recharge = recharge

#     def weight(self):
#         return self.cost + self.boss_hp

#     def __repr__(self) -> str:
#         return (f'Cost:{self.cost} Turn:{self.play_turn} PHP:{self.play_hp} BHP: {self.boss_hp}'
#             f' Mana:{self.mana} Shield:{self.shield} Poison:{self.poison} Recharge:{self.recharge}')

#     def __hash__(self) -> int:
#         return hash((self.play_turn, self.play_hp, self.boss_hp, self.mana,
#             self.shield.duration, self.poison.duration, self.recharge.duration))
