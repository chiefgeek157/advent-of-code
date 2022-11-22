from abc import ABC, abstractmethod
import re
from types import SimpleNamespace

filename = '2015/day07/input.txt'
# filename = '2015/day07/test1.txt'

cmdre = re.compile(r'(?P<arg1>\d+|[a-z]+)? ?(?P<op>AND|OR|NOT|LSHIFT|RSHIFT)? ?(?P<arg2>\d+|[a-z]+)? -> (?P<tgt>[a-z]+)')
mask = 0b1111111111111111
nodes = {}


class Node(ABC):
    def __init__(self, name: str, arg1: str, arg2: str) -> None:
        self.name = name
        self.arg1 = arg1
        self.arg2 = arg2
        self.ans = None

    def eval(self, nodes: dict, mask: int) -> int:
        if self.ans is None:
            self.ans = self._eval(nodes, mask)
        return self.ans

    @abstractmethod
    def _eval(self, nodes: dict, mask: int) -> int:
        pass

    def _arg(self, arg: str, nodes: dict, mask: int):
        if arg.isnumeric():
            return int(arg)
        else:
            return nodes[arg].eval(nodes, mask)


class AssignNode(Node):
    def _eval(self, nodes: dict, mask: int) -> int:
        print(f'{self.name}: [{self.arg1}]')
        ans = self._arg(self.arg1, nodes, mask)
        print(f'{self.name}->{ans}')
        return ans


class NotNode(Node):
    def _eval(self, nodes: dict, maks: int) -> int:
        print(f'{self.name}: ~{self.arg2}')
        ans = (~self._arg(self.arg2, nodes, mask)) & mask
        print(f'{self.name}->{ans}')
        return ans


class AndNode(Node):
    def _eval(self, nodes: dict, mask: int) -> int:
        print(f'{self.name}: {self.arg1} & {self.arg2}')
        ans = (self._arg(self.arg1, nodes, mask) & self._arg(self.arg2, nodes, mask)) & mask
        print(f'{self.name}->{ans}')
        return ans


class OrNode(Node):
    def _eval(self, nodes: dict, mask: int) -> int:
        print(f'{self.name}: {self.arg1} | {self.arg2}')
        ans = (self._arg(self.arg1, nodes, mask) | self._arg(self.arg2, nodes, mask)) & mask
        print(f'{self.name}->{ans}')
        return ans


class LShiftNode(Node):
    def _eval(self, nodes: dict, mask: int) -> int:
        print(f'{self.name}: {self.arg1} << {self.arg2}')
        ans = (self._arg(self.arg1, nodes, mask) << int(self.arg2)) & mask
        print(f'{self.name}->{ans}')
        return ans


class RShiftNode(Node):
    def _eval(self, nodes: dict, mask: int) -> int:
        print(f'{self.name}: {self.arg1} >> {self.arg2}')
        ans = (self._arg(self.arg1, nodes, mask) >> int(self.arg2)) & mask
        print(f'{self.name}->{ans}')
        return ans


def create_node(names: dict) -> Node:
    print(f'names {names}')
    node = None
    match names['op']:
        case 'AND':
            node = AndNode(names['tgt'], names['arg1'], names['arg2'])
        case 'OR':
            node = OrNode(names['tgt'], names['arg1'], names['arg2'])
        case 'NOT':
            node = NotNode(names['tgt'], names['arg1'], names['arg2'])
        case 'LSHIFT':
            node = LShiftNode(names['tgt'], names['arg1'], names['arg2'])
        case 'RSHIFT':
            node = RShiftNode(names['tgt'], names['arg1'], names['arg2'])
        case None:
            node = AssignNode(names['tgt'], names['arg1'], names['arg2'])

    return node

nodes = {}
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        names = cmdre.match(line).groupdict()
        node = create_node(names)
        nodes[node.name] = node
        line = f.readline()

# for name in sorted(nodes.keys()):
#     print(f'Wire {name}: {nodes[name].eval(nodes,mask)}')

ans = nodes['a'].eval(nodes, mask)
print(f'Answer: {ans}')

for node in nodes.values():
    node.ans = None

nodes['b'].ans = ans

ans = nodes['a'].eval(nodes, mask)
print(f'Answer: {ans}')
