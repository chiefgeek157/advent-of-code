from enhancer import Enhancer
from image import Image
import unittest

class EngancerTests(unittest.TestCase):

    def test_read(self):
        with open('2021/day20/test1.txt', 'r') as f:
            e = Enhancer()
            e.read(f)
            # print(f'\n{e}')
            val = \
                '0010100111110101010111011000001110110100111011110011111001000010'\
                '0100110011100111111011100011110010011111001100101111100011010100'\
                '1011001010000001011101111110111011110001011011001001001111100000'\
                '1010000111001011000000100000100100100110010001101111110111101111'\
                '0101000100000001001010100011110110100000010010001101011001000110'\
                '1011001110100000010100000001010101111011101100010000011110100100'\
                '1011010000110010111100001100011001000100000010100000001000000011'\
                '0011110010001010100011001010011100111110000000010011110000001001'
            self.assertEqual(str(e), val)

    def test_enhance_value_at(self):
        with open('2021/day20/test1.txt', 'r') as f:
            e = Enhancer()
            e.read(f)
            f.readline()
            i = Image()
            i.read(f)
            v = e.enhance_value_at(i, 2, 2, 3)
            self.assertEqual(v, '1')

    def test_enhance(self):
        with open('2021/day20/test1.txt', 'r') as f:
            e = Enhancer()
            e.read(f)
            f.readline()
            i1 = Image()
            i1.read(f)
            # print(f'\n{i1}')

            i2 = e.enhance(i1)
            self.assertEqual(i2.width(), 7)
            self.assertEqual(i2.height(), 7)
            self.assertEqual(i2.lit_count(), 24)
            self.assertEqual(i2[1, 0], '1')
            self.assertEqual(i2[5, 0], '1')
            self.assertEqual(i2[3, 6], '1')
            self.assertEqual(i2[5, 6], '1')
            # print(f'\n{i2}')

            i3 = e.enhance(i1, 2)
            self.assertEqual(i3.width(), 9)
            self.assertEqual(i3.height(), 9)
            self.assertEqual(i3.lit_count(), 35)
            self.assertEqual(i3[1, 1], '1')
            self.assertEqual(i3[0, 7], '0')
            self.assertEqual(i3[4, 8], '1')
            self.assertEqual(i3[6, 8], '1')
            # print(f'\n{i3}')

            # i3 = e.enhance(i1, 100)
            # # print(f'\n{i3}')

if __name__ == '__main__':
    unittest.main()