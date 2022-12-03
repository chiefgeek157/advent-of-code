from abc import ABC, abstractmethod
import copy
import sys

# Djikstra's search
#
# A state is a string consisting of the name of each spell capable
# of a duration in the array order along with it's remaining duration (may be zero)
#
# The 'none' state has all durations at zero
#
# The objective function is the cost to reach the state plus
# the boss's remaining hit points to prefer the states that
# are closer to winning first

# A state is composed of
#
# play_turn (bool)
# play_hp
# boss_hp
# mana
# shield_dur
# poison_dur
# recharge_dur
#
# A state has a cost to have reached it
#
# The state's sort order is cost + boss_hp
#
# Allowed arcs are to cast no spell or any spell
# which is affordable and which has a duration of zero
#
# The cost of an arc is the cost of the spell cast


class Effect:
    def __init__(self, duration: int, damage: int, armor: int, heal: int, mana: int) -> None:
        self.duration = duration
        self.damage = damage
        self.armor = armor
        self.heal = heal
        self.mana = mana

    def use(self) -> tuple:
        """return a tuple of (damage, armor, heal, mana, still_valid)"""
        self.duration -= 1
        return (self.damage, self.armor, self.heal, self.mana, (self.duration > 0))

    def __repr__(self) -> str:
        return f'Dur:{self.duration} Dam:{self.damage} Arm:{self.armor} Hea:{self.heal} Man:{self.mana}'


class Spell:
    def __init__(self, name: str, cost: int, damage: int, armor: int, heal: int, mana: int,
            effect: Effect) -> None:
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


class Player(ABC):
    def __init__(self, name: str, hp: int, damage: int) -> None:
        self.name = name
        self.hp = hp
        self.damage = damage
        self.armor = 0

    @abstractmethod
    def attack(self, other: 'Player', spell: Spell=None) -> 'Player':
        """Attack the other player and inclit change to its hp."""
        return other


class Boss(Player):
    def __init__(self, hp: int, damage: int) -> None:
        super().__init__('Boss', hp, damage)

    def attack(self, other: 'Player', spell: Spell=None) -> 'Player':
        new_player = copy.deepcopy(other)
        new_player.hp -= max(1, self.damage - new_player.armor)
        return new_player


class Wizard(Player):
    def __init__(self, hp: int, mana: int) -> None:
        super().__init__('Wizard', hp, 0)
        self.mana = mana
        self.effects = []

    def attack(self, other: 'Player') -> 'Player':
        new_player = copy.deepcopy(other)
        new_effects = []
        for effect in self.effects:
            damage, armor, heal, mana, valid = effect.use()



class State:

    def __init__(self, play_turn: bool, play_hp: int, boss_hp:int, mana: int,
            shield: Effect, poison: Effect, recharge: Effect) -> None:
        self.visited = False
        self.cost = cost
        self.play_turn = play_turn
        self.play_hp = play_hp
        self.boss_hp = boss_hp
        self.mana = mana
        self.shield = shield
        self.poison = poison
        self.recharge = recharge

    def weight(self):
        return self.cost + self.boss_hp

    def __repr__(self) -> str:
        return (f'Cost:{self.cost} Turn:{self.play_turn} PHP:{self.play_hp} BHP: {self.boss_hp}'
            f' Mana:{self.mana} Shield:{self.shield} Poison:{self.poison} Recharge:{self.recharge}')

    def __hash__(self) -> int:
        return hash((self.play_turn, self.play_hp, self.boss_hp, self.mana,
            self.shield.duration, self.poison.duration, self.recharge.duration))
class Node:

    __nodes = set()

    @classmethod
    def get(cls, cost, play_turn: bool, play_hp: int, boss_hp:int, mana: int,
            shield: Effect, poison: Effect, recharge: Effect) -> 'Node':
        node = Node(cost, play_turn, play_hp, boss_hp, mana, shield, poison, rechargey)
        if node not in cls.__nodes:
            cls.__nodes.add(node)
        return node

    def __init__(self, cost, play_turn: bool, play_hp: int, boss_hp:int, mana: int,
            shield: Effect, poison: Effect, recharge: Effect) -> None:
        self.visited = False
        self.cost = cost
        self.play_turn = play_turn
        self.play_hp = play_hp
        self.boss_hp = boss_hp
        self.mana = mana
        self.shield = shield
        self.poison = poison
        self.recharge = recharge

    def weight(self):
        return self.cost + self.boss_hp

    def __repr__(self) -> str:
        return (f'Cost:{self.cost} Turn:{self.play_turn} PHP:{self.play_hp} BHP: {self.boss_hp}'
            f' Mana:{self.mana} Shield:{self.shield} Poison:{self.poison} Recharge:{self.recharge}')

    def __hash__(self) -> int:
        return hash((self.play_turn, self.play_hp, self.boss_hp, self.mana,
            self.shield.duration, self.poison.duration, self.recharge.duration))

play_hp = 50
play_mana = 500

boss_hp = 51
boss_damage = 9

spells = [
    Spell('Magic Missle', cost=53, damage=4),
    Spell('Drain', cost=73, damage=2, heal=2),
    Spell('Shield', cost=113, effect=Effect(duration=6, armor=7)),
    Spell('Poison', cost=173, effect=Effect(duration=6, damage=3)),
    Spell('Recharge', cost=229, effect=Effect(duration=5, mana=101))
]

min_mana = sys.maxsize
# Initialize work to a None spell
work = set()
initial = Node.get(True, play_hp, boss_hp, play_mana, 0, 0, 0)
print(f'INitial state: {initial}')
work.add(initial)
while work:
    # Get the least expensive option
    node = sorted(work, key=lambda x: x.weight())[0]
    work.remove(node)
    print(f'Node: {node}')
    node.visited = True

    for spell in spells:
        neighbor = Node.get()