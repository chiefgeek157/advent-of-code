import copy
import math
import colorama
from colorama import Back, Fore, Style

colorama.init()

class SnailNum():

    LEFT_FACTOR = 3
    RIGHT_FACTOR = 2
    EXPLODE_DEPTH = 5
    SPLIT_THRESHHOLD = 10

    final = None

    def largest_mag(nums):
        print()
        max_mag = None
        for i in range(len(nums)):
            for j in range(len(nums)):
                # print(f'{nums[i]} + {nums[j]}')
                sum = nums[i] + nums[j]
                mag = sum.magnitude()
                if max_mag is None or mag > max_mag:
                    # print(f'\nMAX {nums[i]} {nums[j]}, {sum} {mag}')
                    max_num1 = nums[i]
                    max_num2 = nums[j]
                    max_sum = sum
                    max_mag = mag
        return max_num1, max_num2, max_sum, max_mag

    # Create a SnailNum from a string
    def read(s):
        # print(f'SnailNum.read(): parsing {s}')
        stack = []
        top = None
        for char in s:
            current = None if len(stack) == 0 else stack[-1]
            match char:
                case '[':
                    # print(f'Creating new num')
                    new = SnailNum(current)
                    if current is not None:
                        if current.left is None:
                            current.left = new
                        else:
                            current.right = new
                    stack.append(new)
                    if top is None: top = new
                case ',':
                    pass
                case ']':
                    final = stack.pop()
                    # print(f'closed {final}')
                case _:
                    digit = int(char)
                    if current.left is None:
                        # print(f'Setting left to {digit}')
                        current.left = digit
                    else:
                        # print(f'Setting right to {digit}')
                        current.right = digit
            # print(f'top={top}')
        return final

    # Creating a string starting at the top given any num in a tree
    def str_top(num):
        while num.parent is not None:
            num = num.parent
        return str(num)

    def __init__(self, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right

    def left_is_value(self):
        return True if isinstance(self.left, int) else False

    def right_is_value(self):
        return True if isinstance(self.right, int) else False

    def magnitude(self):
        # print(f'Magnitude of {self}')
        lmag = self.left if self.left_is_value() else self.left.magnitude()
        rmag = self.right if self.right_is_value() else self.right.magnitude()
        # print(f'lmag={lmag} rmag={rmag} for {self}')
        return SnailNum.LEFT_FACTOR * lmag + SnailNum.RIGHT_FACTOR * rmag

    def depth(self):
        depth = 1
        if self.parent is not None:
            depth += self.parent.depth()
        return depth

    def pretty(self):
        s = ''
        if self.depth() >= SnailNum.EXPLODE_DEPTH:
            s += f'{Fore.YELLOW}{Style.BRIGHT}'
        s += f'['
        if self.left_is_value() and self.left >= SnailNum.SPLIT_THRESHHOLD:
            s += f'{Back.BLUE}'
        s += f'{self.left}{Back.RESET},'
        if self.right_is_value() and self.right >= SnailNum.SPLIT_THRESHHOLD:
            s += f'{Back.BLUE}'
        s+= f'{self.right}{Back.RESET}]{Style.RESET_ALL}'
        return s

    def __str__(self):
        return f'[{self.left},{self.right}]'

    def __repr__(self):
        return f'SnailNum(parent={self.parent}, left={self.left}, right={self.right})'

    def __add__(self, other):
        # print(f'Adding {self} and {other}')
        if isinstance(other, SnailNum):
            new_self = copy.deepcopy(self)
            new_other = copy.deepcopy(other)
            new = SnailNum(None, new_self, new_other)
            new_self.parent = new
            new_other.parent = new
            new._reduce()
            # print(f'Sum={new}')
            # input('Enter...')
            return new
        else:
            return NotImplemented

    def _reduce(self):
        # print(f'_reduce({self})')
        changed = True
        while changed:
            changed = self._explode()
            if not changed:
                changed = self._split()
            # print(f'TOP: {SnailNum.str_top(self)}')
            # input('Enter...')

    def _explode(self):
        # print(f'_explode({self}, depth={self.depth()})')
        changed = False
        if self.depth() < SnailNum.EXPLODE_DEPTH:
            if not self.left_is_value():
                changed = self.left._explode()
            if not changed and not self.right_is_value():
                changed = self.right._explode()
        else:
            # print(f'EXPLODE: {self}')
            # By definition self must have a parent
            # and this left is a value
            self.parent._add_left(self.left, self)
            self.parent._add_right(self.right, self)
            self.parent._replace(self, 0)
            # print(f'    After explode: {SnailNum.str_top(self)}')
            changed = True
        return changed

    def _add_left(self, value, child=None):
        # print(f'_add_left(self={self}, value={value}, child={child}')
        if child is None:
            # Headed down
            if self.right_is_value():
                # print(f'Adding {value} to right {self.right}')
                self.right += value
                # print(f'    After add left: {SnailNum.str_top(self)}')
            else:
                # print(f'Deferring to right child')
                self.right._add_left(value)
        else:
            # Headed up
            if self.left_is_value():
                # print(f'Adding {value} to left {self.left}')
                self.left += value
                # print(f'    After add left: {SnailNum.str_top(self)}')
            else:
                if self.left != child:
                    # print(f'Deferring to left child')
                    self.left._add_left(value)
                else:
                    if self.parent is not None:
                        # print(f'Deferring to parent')
                        self.parent._add_left(value, self)
                    else:
                        # print(f'No left value found')
                        # print(f'    After add left: {SnailNum.str_top(self)}')
                        pass
        # print(f'TOP: {SnailNum.str_top(self)}')

    def _add_right(self, value, child=None):
        # print(f'_add_right(self={self}, value={value}, child={child}')
        if child is None:
            # Headed down
            if self.left_is_value():
                # print(f'Adding {value} to left {self.left}')
                self.left += value
                # print(f'    After add right: {SnailNum.str_top(self)}')
            else:
                # print(f'Deferring to left child')
                self.left._add_right(value)
        else:
            # Headed up
            if self.right_is_value():
                # print(f'Adding {value} to right {self.right}')
                self.right += value
                # print(f'    After add right: {SnailNum.str_top(self)}')
            else:
                if self.right != child:
                    # print(f'Deferring to right child')
                    self.right._add_right(value)
                else:
                    if self.parent is not None:
                        # print(f'Deferring to parent')
                        self.parent._add_right(value, self)
                    else:
                        # print(f'No right value found')
                        # print(f'    After add right: {SnailNum.str_top(self)}')
                        pass
        # print(f'TOP: {SnailNum.str_top(self)}')

    def _replace(self, child, new):
        # print(f'_replace({self}, {child}, {new})')
        if self.left == child:
            self.left = new
        else:
            self.right = new
        if isinstance(new, SnailNum):
            new.parent = self
        # print(f'    After replace: {SnailNum.str_top(self)}')

    def _split(self):
        # print(f'_split({self})')
        changed = False

        if self.left_is_value():
            if self.left >= SnailNum.SPLIT_THRESHHOLD:
                self.left = SnailNum(self, math.floor(self.left / 2), math.ceil(self.left / 2))
                changed = True
                # print(f'    After split: {SnailNum.str_top(self)}')
        else:
            changed = self.left._split()

        if not changed:
            if self.right_is_value():
                if self.right >= SnailNum.SPLIT_THRESHHOLD:
                    self.right = SnailNum(self, math.floor(self.right / 2), math.ceil(self.right / 2))
                    changed = True
                    # print(f'    After split: {SnailNum.str_top(self)}')
            else:
                changed = self.right._split()
        return changed
