from image import Image
import unittest

class ImageTests(unittest.TestCase):
    def test_read(self):
        with open('2021/day20/test1.txt', 'r') as f:
            f.readline()
            f.readline()
            i = Image()
            i.read(f)
            # print(f'\n{i.as_str()}')
            # print(f'\n{i.as_str(True)}')
            self.assertEqual(i.width(), 5)
            self.assertEqual(i.height(), 5)

    def test_getitem(self):
        with open('2021/day20/test1.txt', 'r') as f:
            f.readline()
            f.readline()
            i = Image()
            i.read(f)
            # print(f'\n{i.as_str()}')
            # print(f'\n{i.as_str(True)}')
            self.assertEqual(i[0,0], '1')
            self.assertEqual(i[4,4], '1')
            self.assertEqual(i[-20,-20], '0')
            self.assertEqual(i[600,600], '0')

    def test_get_patch(self):
        with open('2021/day20/test1.txt', 'r') as f:
            f.readline()
            f.readline()
            i = Image()
            i.read(f)
            # print(f'\n{i.as_str()}')
            # print(f'\n{i.as_str(True)}')
            p = i.get_patch(2, 2, 3)
            # print(f'patch {p}')
            self.assertEqual(p, '000100010')

    def test_get_bigger_patch(self):
        with open('2021/day20/test1.txt', 'r') as f:
            f.readline()
            f.readline()
            i = Image()
            i.read(f)
            # print(f'\n{i.as_str()}')
            # print(f'\n{i.as_str(True)}')
            p = i.get_patch(2, 2, 5)
            # print(f'patch {p}')
            self.assertEqual(p, '1001010000110010010000111')

    def test_count_lit(self):
        with open('2021/day20/test1.txt', 'r') as f:
            f.readline()
            f.readline()
            i = Image()
            i.read(f)
            count = i.lit_count()
            self.assertEqual(count, 10)

if __name__ == '__main__':
    unittest.main()