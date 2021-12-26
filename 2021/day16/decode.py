import colorama
from colorama import Back, Cursor, Fore, Style

class Decoder():

    def __init__(self):
        pass

    def decode(self, line):
        bits = ''
        for char in line:
            val = int(char, 16)
            bits += f'{val:04b}'
        print(f'Decoder read line: {bits}')

        offset = 0
        factory = PacketFactory()
        packets = []
        done = False
        while not done:
            print(f'Reading packet from {bits[offset:]}')
            packet, bits_used = factory.create(bits[offset:])
            if packet is None:
                done = True
            offset += bits_used
            packets.append(packet)

        return packets

class PacketFactory():

    VERSION_BITS = 3

    PACKET_TYPE_BITS = 3
    PACKET_TYPE_LIERAL = 4

    OPERATOR_TYPE_BITS = 1
    OPERATOR_TYPE_SIMPLE = 0
    OPERATOR_TYPE_COMPLEX = 1

    def __init__(self):
        pass

    # Return a list of decoded packets
    # The use of type allows other packets that already know
    # The type to pass it in
    def create(self, bits):
        packet = None
        offset = 0

        # Read packet version
        version, bits_used = self._read_version(bits[offset:])
        offset += bits_used
        print(f'Packet version: {version}')

        type, bits_used = self._read_type(bits[offset:])
        offset += bits_used
        if type is not None:
            print(f'Packet Type {type}')
            packet, bits_used = self._handle_type(version, type, bits[offset:])
            offset += bits_used

        return packet, offset

    def _read_version(self, bits):
        return int(bits[:self.VERSION_BITS], 2), self.VERSION_BITS

    # Reads and returns the next packet type and bits used
    def _read_type(self, bits):
        type = None
        offset = 0
        if len(bits) < self.PACKET_TYPE_BITS:
            offset = len(bits)
        else:
            type = int(bits[:self.PACKET_TYPE_BITS], 2)
            offset = self.PACKET_TYPE_BITS
            if type == 0:
                type = None
                offset = len(bits)
        if type is None:
            print(f'Discarding last {offset} bits: {bits}')
        return type, offset

    # NOTE: version is ignored for now
    def _handle_type(self, version, type, bits):
        print(f'Handling type {type}')
        packet = None
        offset = 0
        match type:
            case self.PACKET_TYPE_LIERAL:
                print(f'Detected Literal')
                packet = Literal(self)
                offset += packet.read(bits[offset:])
            case _:
                # For now all other cases are operators
                print(f'Detected Operator')
                operator_type, bits_used = self._read_operator_type(bits[offset:])
                offset += bits_used
                print(f'Found operator type {operator_type}')
                match operator_type:
                    case self.OPERATOR_TYPE_SIMPLE:
                        print(f'Detected SimpleOperator')
                        packet = SimpleOperator(self)
                    # case 1:
                    #     print(f'Detected Type1Operator')
                    #     packet = Type1Operator(self)
                    case _:
                        raise ValueError(f'Unknown operator type {operator_type}')
                offset += packet.read(bits[offset:])
            # case _:
            #     raise ValueError(f'Unknown type: {type}')
        return packet, offset

    def _read_operator_type(self, bits):
        return int(bits[:self.OPERATOR_TYPE_BITS]), self.OPERATOR_TYPE_BITS

class Packet():

    def __init__(self, factory):
        self.factory = factory

    # Read data and return bits used
    def read(self, bits):
        return 0

class Literal(Packet):

    DIGIT_BITS = 4

    def __init__(self, factory):
        super(Literal, self).__init__(factory)
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

        return num_digits * (1 + self.DIGIT_BITS)

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Literal({self.value})'

class Operator(Packet):

    def __init__(self, factory, type):
        super(Operator, self).__init__(factory)
        self.type = type
        self.operands = None

    def __str__(self):
        return f'{self.type}'

    def __repr__(self):
        return f'Operator({self.type})'

class SimpleOperator(Operator):

    LENGTH_BITS = 15

    def __init__(self, factory):
        super(SimpleOperator, self).__init__(factory, 0)

    def read(self, bits):
        print(f'Reading SimpleOperator from {bits}')
        offset = 0
        # Read the length
        length = int(bits[offset:offset + self.LENGTH_BITS], 2)
        print(f'Length {length}')
        offset += self.LENGTH_BITS

        data = bits[offset:offset + length]
        data_offset = 0
        while data_offset < length:
            print(f'Reading Literal operand from {data[data_offset:]}')
            packet, bits_used = self.factory.create(data[data_offset:],
                PacketFactory.PACKET_TYPE_LIERAL)
            self.operands.append(packet)
            data_offset += bits_used
        offset += data_offset

        return offset
    
    def __str__(self):
        return f'{self.type}'

    def __repr__(self):
        return f'Type0Operator({self.type})'

filename = 'test1.txt'
#filename = 'test2.txt'
#filename = 'test3.txt'
#filename = 'input.txt'
use_line = 2

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
packets = decoder.decode(line)
print(f'Packets: {packets}')
