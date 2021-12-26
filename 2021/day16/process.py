import colorama
from colorama import Back, Cursor, Fore, Style
import sys

class Decoder():

    def __init__(self):
        pass

    def decode(self, line):
        bits = ''
        for char in line:
            val = int(char, 16)
            bits += f'{val:04b}'
        print(f'Decoder read line: {bits}')

        factory = PacketFactory()
        print(f'Reading packet from {bits}')
        packet, bits_used = factory.create(bits)

        return packet

class PacketFactory():

    VERSION_BITS = 3

    PACKET_MIN_LENGTH = 11
    PACKET_TYPE_BITS = 3

    PACKET_TYPE_SUM = 0
    PACKET_TYPE_PRODUCT = 1
    PACKET_TYPE_MIN = 2
    PACKET_TYPE_MAX = 3
    PACKET_TYPE_LITERAL = 4
    PACKET_TYPE_GT = 5
    PACKET_TYPE_LT = 6
    PACKET_TYPE_EQ = 7

    OPERATOR_TYPE_BITS = 1
    OPERATOR_TYPE_SIMPLE = 0
    OPERATOR_TYPE_COMPLEX = 1

    def __init__(self):
        pass

    # Return a list of decoded packets
    # The use of type allows other packets that already know
    # The type to pass it in
    def create(self, bits):
        print(f'PacketFactory.create(bits={bits})')
        if len(bits) < self.PACKET_MIN_LENGTH:
            print(f'Less than {self.PACKET_MIN_LENGTH} of data left: {bits}')
            return None, len(bits)

        # Read packet version
        offset = 0
        version, bits_used = self._read_version(bits[offset:])
        offset += bits_used
        print(f'Packet version: {version}')

        type, bits_used = self._read_type(bits[offset:])
        offset += bits_used
        print(f'Packet Type {type}')
        packet, bits_used = self._handle_type(version, type, bits[offset:])
        offset += bits_used

        return packet, offset

    def _read_version(self, bits):
        return int(bits[:self.VERSION_BITS], 2), self.VERSION_BITS

    # Reads and returns the next packet type and bits used
    def _read_type(self, bits):
        offset = 0
        type = int(bits[:self.PACKET_TYPE_BITS], 2)
        print(f'Read packet type {type}')
        offset = self.PACKET_TYPE_BITS
        return type, offset

    def _handle_type(self, version, type, bits):
        print(f'Handling type {type}')
        packet = None
        offset = 0
        match type:
            case self.PACKET_TYPE_LITERAL:
                print(f'Detected Literal')
                packet = Literal(version, type, self)
                offset += packet.read(bits[offset:])
            case _:
                # All other cases are operators
                print(f'Detected Operator')
                operator_type, bits_used = self._read_operator_type(bits[offset:])
                offset += bits_used
                print(f'Found operator type {operator_type}')
                match operator_type:
                    case self.OPERATOR_TYPE_SIMPLE:
                        print(f'Detected SimpleOperator')
                        packet = SimpleOperator(version, type, self)
                    case 1:
                        print(f'Detected ComplexOperator')
                        packet = ComplexOperator(version, type, self)
                    case _:
                        raise ValueError(f'Unknown operator type {operator_type}')
                offset += packet.read(bits[offset:])
            # case _:
            #     raise ValueError(f'Unknown type: {type}')
        return packet, offset

    def _read_operator_type(self, bits):
        return int(bits[:self.OPERATOR_TYPE_BITS]), self.OPERATOR_TYPE_BITS

class Packet():

    def __init__(self, version, type, factory):
        self.version = version
        self.type = type
        self.factory = factory

    # Read data and return bits used
    def read(self, bits):
        return len(bits)

    def sum_versions(self):
        return None

    def eval(self):
        return None

class Literal(Packet):

    DIGIT_BITS = 4

    def __init__(self, version, type, factory):
        super(Literal, self).__init__(version, type, factory)
        self.value = None
    
    # Read data and return bits used
    def read(self, bits):
        print(f'Reading Literal from {bits}')
        self.value = 0
        offset = 0
        done = False
        num_digits = 0
        while not done:
            num_digits += 1

            # Read "more" bit
            more_bit = int(bits[offset])
            # print(f'Literal at index {offset} read more bit {more_bit}')
            offset += 1
            if more_bit == 0:
                done = True

            # Read digit
            digit = int(bits[offset:offset + self.DIGIT_BITS], 2)
            # print(f'Literal at index {offset} read digit {digit}')
            self.value = self.value * 16 + digit
            # print(f'Literal value now {self.value}')
            offset += self.DIGIT_BITS

        print(f'Read Liternal value {self.value}')
        return num_digits * (1 + self.DIGIT_BITS)

    def sum_versions(self):
       return self.version

    def eval(self):
        return self.value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Literal({self.value})'

class Operator(Packet):

    def __init__(self, version, type, factory):
        super(Operator, self).__init__(version, type, factory)
        self.func = Operator._FUNCTIONS[type]
        self.operands = None

    def sum_versions(self):
        total = self.version
        for packet in self.operands:
            total += packet.sum_versions()
        return total

    def eval(self):
        return self.func(self.operands)

    def __str__(self):
        return f'{self.type}'

    def __repr__(self):
        return f'Operator({self.type})'

    def _func_sum(operands):
        res = 0
        for op in operands:
            res += op.eval()
        return res

    def _func_product(operands):
        res = None
        for op in operands:
            if res is None:
                res = op.eval()
            else:
                res *= op.eval()
        return res

    def _func_min(operands):
        res = sys.maxsize
        for op in operands:
            res = min(res, op.eval())
        return res

    def _func_max(operands):
        res = -sys.maxsize - 1
        for op in operands:
            res = max(res, op.eval())
        return res

    def _func_gt(operands):
        return 1 if operands[0].eval() > operands[1].eval() else 0

    def _func_lt(operands):
        return 1 if operands[0].eval() < operands[1].eval() else 0

    def _func_eq(operands):
        return 1 if operands[0].eval() == operands[1].eval() else 0

    _FUNCTIONS = {
        PacketFactory.PACKET_TYPE_SUM: _func_sum,
        PacketFactory.PACKET_TYPE_PRODUCT: _func_product,
        PacketFactory.PACKET_TYPE_MIN: _func_min,
        PacketFactory.PACKET_TYPE_MAX: _func_max,
        PacketFactory.PACKET_TYPE_GT: _func_gt,
        PacketFactory.PACKET_TYPE_LT: _func_lt,
        PacketFactory.PACKET_TYPE_EQ: _func_eq,
    }

class SimpleOperator(Operator):

    LENGTH_BITS = 15

    def __init__(self, version, type, factory):
        super(SimpleOperator, self).__init__(version, type, factory)

    def read(self, bits):
        print(f'Reading SimpleOperator from {bits}')
        offset = 0
        # Read the length
        length = int(bits[offset:offset + self.LENGTH_BITS], 2)
        print(f'Operands length {length}')
        offset += self.LENGTH_BITS

        data = bits[offset:offset + length]
        data_offset = 0
        self.operands = []
        while data_offset < length:
            print(f'Reading Literal operand from {data[data_offset:]}')
            packet, bits_used = self.factory.create(data[data_offset:])
            self.operands.append(packet)
            data_offset += bits_used
        offset += data_offset

        return offset
    
    def __str__(self):
        return f'{self.type}'

    def __repr__(self):
        return f'SimpleOperator({self.type}, operands: {self.operands})'

class ComplexOperator(Operator):

    PACKET_COUNT_BITS = 11

    def __init__(self, version, type, factory):
        super(ComplexOperator, self).__init__(version, type, factory)

    def read(self, bits):
        print(f'Reading ComplexOperator from {bits}')
        offset = 0
        # Read the numberof subpackets
        packet_count = int(bits[offset:offset + self.PACKET_COUNT_BITS], 2)
        print(f'Operands count {packet_count}')
        offset += self.PACKET_COUNT_BITS

        self.operands = []
        packets_read = 0
        while packets_read < packet_count:
            print(f'Reading operand packet from {bits[offset:]}')
            packet, bits_used = self.factory.create(bits[offset:])
            self.operands.append(packet)
            packets_read += 1
            offset += bits_used

        return offset
    
    def __str__(self):
        return f'{self.type}'

    def __repr__(self):
        return f'ComplexOperator({self.type}, operands: {self.operands})'

#filename = 'test1.txt'
#filename = 'test2.txt'
#filename = 'test3.txt'
filename = 'input.txt'
use_line = 1

colorama.init()

lines_read = 0
with open(filename, 'r') as f:
    line = f.readline()
    lines_read += 1
    while line and lines_read < use_line:
        line = f.readline()
        lines_read += 1
    line = line.strip()
    print(f'Using line {use_line}: {line}')

decoder = Decoder()
packet = decoder.decode(line)
print(f'Packet: {packet}')

print(f'Answer: {packet.eval()}')
