import unittest
from snailnum import SnailNum

class SnailNumTests(unittest.TestCase):

    def test_1(self):
        input = '''
            [[[[4,3],4],4],[7,[[8,4],9]]]
            [1,1]
        '''
        sum = None
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                sum = num if sum is None else sum + num
        self.assertEqual(str(sum), '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')

    def test_2(self):
        input = '''
            [1,1]
            [2,2]
            [3,3]
            [4,4]
        '''
        sum = None
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                sum = num if sum is None else sum + num
        self.assertEqual(str(sum), '[[[[1,1],[2,2]],[3,3]],[4,4]]')

    def test_3(self):
        input = '''
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            [5,5]
        '''
        sum = None
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                sum = num if sum is None else sum + num
        self.assertEqual(str(sum), '[[[[3,0],[5,3]],[4,4]],[5,5]]')

    def test_4(self):
        input = '''
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            [5,5]
            [6,6]
        '''
        sum = None
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                sum = num if sum is None else sum + num
        self.assertEqual(str(sum), '[[[[5,0],[7,4]],[5,5]],[6,6]]')

    def test_5(self):
        input = '''
            [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
            [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
            [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
            [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
            [7,[5,[[3,8],[1,4]]]]
            [[2,[2,2]],[8,[8,1]]]
            [2,9]
            [1,[[[9,3],9],[[9,0],[0,7]]]]
            [[[5,[7,4]],7],1]
            [[[[4,2],2],6],[8,7]]
        '''
        sum = None
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                sum = num if sum is None else sum + num
        self.assertEqual(str(sum), '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')

    def test_6(self):
        input = '[9,1]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 29)

    def test_7(self):
        input = '[1,9]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 21)

    def test_8(self):
        input = '[[9,1],[1,9]]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 129)

    def test_9(self):
        input = '[[1,2],[[3,4],5]]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 143)

    def test_10(self):
        input = '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 1384)

    def test_11(self):
        input = '[[[[1,1],[2,2]],[3,3]],[4,4]]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 445)

    def test_12(self):
        input = '[[[[3,0],[5,3]],[4,4]],[5,5]]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 791)

    def test_13(self):
        input = '[[[[5,0],[7,4]],[5,5]],[6,6]]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 1137)

    def test_14(self):
        input = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
        num = SnailNum.read(input)
        self.assertEqual(num.magnitude(), 3488)

    def test_15(self):
        input = '''
            [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
            [[[5,[2,8]],4],[5,[[9,9],0]]]
            [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
            [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
            [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
            [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
            [[[[5,4],[7,7]],8],[[8,3],8]]
            [[9,3],[[9,9],[6,[4,9]]]]
            [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
            [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
        '''

        sum = None
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                sum = num if sum is None else sum + num
        self.assertEqual(str(sum), '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')
        self.assertEqual(sum.magnitude(), 4140)

    def test_part1(self):
        input = '''
            [[[3,9],[7,2]],[[8,4],[[5,6],0]]]
            [[[1,[4,9]],[[1,8],[1,5]]],[[[2,6],[6,7]],[[4,6],[9,0]]]]
            [[[[9,2],1],[[0,7],[9,6]]],[[5,9],[7,[6,9]]]]
            [8,9]
            [[4,[6,1]],[2,[[6,7],2]]]
            [[6,[[4,1],5]],[4,9]]
            [[[0,6],[8,[8,5]]],[6,9]]
            [[0,[1,0]],[[8,[7,4]],[[1,1],[5,0]]]]
            [[[1,[0,1]],6],[1,9]]
            [[2,[[9,0],[6,1]]],[[8,4],[5,7]]]
            [[[[5,3],[0,9]],[1,[0,7]]],[[9,0],[2,[2,0]]]]
            [[2,[2,[6,8]]],[[9,[5,4]],[4,[3,4]]]]
            [[[[4,0],[7,0]],[[4,8],[5,8]]],[[[7,2],[2,2]],[[3,3],3]]]
            [[5,0],5]
            [[8,[[5,0],2]],[6,[5,1]]]
            [[[9,[8,8]],[8,7]],[[[4,2],4],[[5,1],[4,8]]]]
            [[[[1,1],3],5],9]
            [[[[1,7],[6,5]],5],[[0,6],0]]
            [[9,6],2]
            [[[2,[0,8]],[8,[2,1]]],5]
            [[[9,[3,7]],3],[0,[5,9]]]
            [[[2,[1,7]],6],[[7,[8,2]],[[8,2],8]]]
            [[[[1,2],1],5],2]
            [4,[8,[3,9]]]
            [[[[8,9],[6,0]],[[1,6],7]],8]
            [[2,[8,1]],3]
            [[2,2],[[8,[0,2]],[[5,0],5]]]
            [9,[2,[[6,1],[8,9]]]]
            [[4,[[6,6],4]],[[[9,3],[3,1]],5]]
            [[[7,8],1],0]
            [[[8,8],[[1,0],7]],[4,6]]
            [9,8]
            [[[[4,2],9],[[9,9],7]],[7,[9,[5,8]]]]
            [[4,[4,[3,3]]],8]
            [0,2]
            [[4,[5,5]],[9,[[6,9],4]]]
            [[[7,3],[[1,2],6]],[[[2,4],[6,7]],[[5,0],9]]]
            [[[[2,0],5],[4,5]],[[[6,5],[6,0]],[1,[3,4]]]]
            [[3,[6,8]],[[[3,0],0],[[2,8],7]]]
            [[[4,[6,2]],[9,[4,1]]],[8,[3,4]]]
            [[[6,[6,8]],[7,[2,0]]],[4,[[8,7],[1,6]]]]
            [2,[0,[4,0]]]
            [[[[0,5],1],8],[[9,[0,3]],3]]
            [[[3,[5,2]],[3,[3,2]]],[[[7,3],1],7]]
            [1,[[[1,8],[1,7]],0]]
            [[8,6],[[0,4],4]]
            [[[8,2],[4,6]],3]
            [5,[[[7,5],[4,5]],[0,2]]]
            [[3,[3,6]],6]
            [[[[6,8],[5,7]],[[7,3],5]],[[8,[4,8]],8]]
            [[[[5,8],[3,1]],[[3,7],[7,0]]],[[9,7],0]]
            [[2,[[5,3],8]],0]
            [0,[2,8]]
            [[8,9],[[[2,2],[4,7]],[[4,0],1]]]
            [[[[3,0],8],[[7,3],[6,1]]],[[3,8],[4,2]]]
            [[[[6,7],[4,3]],[[3,9],5]],8]
            [[[7,7],[[3,4],7]],[[[0,4],1],9]]
            [[[7,5],5],[[2,[9,9]],[0,[3,5]]]]
            [[[[3,3],[6,1]],[5,8]],[[4,7],[8,1]]]
            [[[0,[7,3]],[6,[7,2]]],[[0,8],7]]
            [[[2,7],[9,7]],[8,[3,8]]]
            [[[0,2],6],[[9,[6,5]],[[3,9],1]]]
            [[7,[[3,4],[2,8]]],[[[4,1],4],7]]
            [[3,[[3,4],6]],[[3,9],[[4,5],[3,0]]]]
            [[[5,[5,1]],[2,4]],[1,[[1,6],6]]]
            [[[5,6],[[1,3],[5,0]]],[[[4,1],8],[5,5]]]
            [[[[2,0],7],[[8,9],1]],[[[4,0],[1,6]],1]]
            [[[2,0],[[4,2],[9,9]]],[4,9]]
            [[[[1,9],6],2],[[5,4],[2,4]]]
            [[[[4,1],[4,5]],[[2,3],2]],[3,[[8,8],1]]]
            [[[[8,1],0],[2,2]],[[2,[7,1]],1]]
            [[[7,4],[[1,3],5]],[[6,8],[[0,0],2]]]
            [[[1,2],8],[[[1,7],[4,0]],[[8,2],8]]]
            [[[0,8],[3,6]],[[[5,3],7],[9,7]]]
            [[4,6],[[[7,9],[7,5]],[[4,6],[8,4]]]]
            [[[[7,3],0],[[6,2],[7,2]]],[9,[[8,0],3]]]
            [[[3,0],1],[[2,3],1]]
            [[[5,[8,6]],[[1,2],2]],[[[1,4],6],[5,[7,1]]]]
            [[[[1,5],8],[0,0]],4]
            [[[7,[6,8]],3],[[5,1],[[2,8],[4,6]]]]
            [3,[[[5,8],[4,5]],[[7,7],8]]]
            [[6,[7,[8,2]]],[[9,0],0]]
            [[[8,[7,6]],1],[[2,4],6]]
            [[[[0,4],2],[0,7]],[6,6]]
            [1,[[1,9],[9,3]]]
            [[[[5,2],[5,3]],[[9,0],4]],2]
            [[[[5,5],3],[7,[1,2]]],[6,[7,2]]]
            [[[[2,1],3],8],[[2,[8,2]],[7,4]]]
            [[8,[9,[1,8]]],[[[4,4],[0,6]],[6,3]]]
            [[[1,6],[1,[2,5]]],0]
            [[[[0,1],[7,2]],[[7,2],3]],[2,[[7,8],[0,7]]]]
            [[[[1,8],8],[[5,7],[3,4]]],[[[2,5],[7,4]],[[8,4],9]]]
            [[[2,2],[5,[1,0]]],[[[6,6],[3,0]],[[8,5],5]]]
            [[[[8,2],[4,8]],[9,4]],[[8,[7,9]],0]]
            [[3,[5,[2,4]]],[[[8,1],0],[[0,4],[4,5]]]]
            [[5,[9,[3,8]]],[4,[1,[5,2]]]]
            [[[3,[0,6]],[7,[8,7]]],[[6,8],[[8,7],0]]]
            [[[[0,2],5],[4,6]],3]
            [[6,7],[[1,[4,6]],9]]
            [7,[3,[[8,8],5]]]
       '''

        sum = None
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                sum = num if sum is None else sum + num
        print(f'\n\nAnswer: {sum.magnitude()}\n\n')

    def test_16(self):
        input = '''
            [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
            [[[5,[2,8]],4],[5,[[9,9],0]]]
            [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
            [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
            [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
            [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
            [[[[5,4],[7,7]],8],[[8,3],8]]
            [[9,3],[[9,9],[6,[4,9]]]]
            [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
            [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
        '''

        nums = []
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                nums.append(num)
        num1, num2, sum, mag = SnailNum.largest_mag(nums)
        self.assertEqual(str(num1), '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]')
        self.assertEqual(str(num2), '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]')
        self.assertEqual(str(sum), '[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]')
        self.assertEqual(mag, 3993)

    def test_part2(self):
        input = '''
            [[[3,9],[7,2]],[[8,4],[[5,6],0]]]
            [[[1,[4,9]],[[1,8],[1,5]]],[[[2,6],[6,7]],[[4,6],[9,0]]]]
            [[[[9,2],1],[[0,7],[9,6]]],[[5,9],[7,[6,9]]]]
            [8,9]
            [[4,[6,1]],[2,[[6,7],2]]]
            [[6,[[4,1],5]],[4,9]]
            [[[0,6],[8,[8,5]]],[6,9]]
            [[0,[1,0]],[[8,[7,4]],[[1,1],[5,0]]]]
            [[[1,[0,1]],6],[1,9]]
            [[2,[[9,0],[6,1]]],[[8,4],[5,7]]]
            [[[[5,3],[0,9]],[1,[0,7]]],[[9,0],[2,[2,0]]]]
            [[2,[2,[6,8]]],[[9,[5,4]],[4,[3,4]]]]
            [[[[4,0],[7,0]],[[4,8],[5,8]]],[[[7,2],[2,2]],[[3,3],3]]]
            [[5,0],5]
            [[8,[[5,0],2]],[6,[5,1]]]
            [[[9,[8,8]],[8,7]],[[[4,2],4],[[5,1],[4,8]]]]
            [[[[1,1],3],5],9]
            [[[[1,7],[6,5]],5],[[0,6],0]]
            [[9,6],2]
            [[[2,[0,8]],[8,[2,1]]],5]
            [[[9,[3,7]],3],[0,[5,9]]]
            [[[2,[1,7]],6],[[7,[8,2]],[[8,2],8]]]
            [[[[1,2],1],5],2]
            [4,[8,[3,9]]]
            [[[[8,9],[6,0]],[[1,6],7]],8]
            [[2,[8,1]],3]
            [[2,2],[[8,[0,2]],[[5,0],5]]]
            [9,[2,[[6,1],[8,9]]]]
            [[4,[[6,6],4]],[[[9,3],[3,1]],5]]
            [[[7,8],1],0]
            [[[8,8],[[1,0],7]],[4,6]]
            [9,8]
            [[[[4,2],9],[[9,9],7]],[7,[9,[5,8]]]]
            [[4,[4,[3,3]]],8]
            [0,2]
            [[4,[5,5]],[9,[[6,9],4]]]
            [[[7,3],[[1,2],6]],[[[2,4],[6,7]],[[5,0],9]]]
            [[[[2,0],5],[4,5]],[[[6,5],[6,0]],[1,[3,4]]]]
            [[3,[6,8]],[[[3,0],0],[[2,8],7]]]
            [[[4,[6,2]],[9,[4,1]]],[8,[3,4]]]
            [[[6,[6,8]],[7,[2,0]]],[4,[[8,7],[1,6]]]]
            [2,[0,[4,0]]]
            [[[[0,5],1],8],[[9,[0,3]],3]]
            [[[3,[5,2]],[3,[3,2]]],[[[7,3],1],7]]
            [1,[[[1,8],[1,7]],0]]
            [[8,6],[[0,4],4]]
            [[[8,2],[4,6]],3]
            [5,[[[7,5],[4,5]],[0,2]]]
            [[3,[3,6]],6]
            [[[[6,8],[5,7]],[[7,3],5]],[[8,[4,8]],8]]
            [[[[5,8],[3,1]],[[3,7],[7,0]]],[[9,7],0]]
            [[2,[[5,3],8]],0]
            [0,[2,8]]
            [[8,9],[[[2,2],[4,7]],[[4,0],1]]]
            [[[[3,0],8],[[7,3],[6,1]]],[[3,8],[4,2]]]
            [[[[6,7],[4,3]],[[3,9],5]],8]
            [[[7,7],[[3,4],7]],[[[0,4],1],9]]
            [[[7,5],5],[[2,[9,9]],[0,[3,5]]]]
            [[[[3,3],[6,1]],[5,8]],[[4,7],[8,1]]]
            [[[0,[7,3]],[6,[7,2]]],[[0,8],7]]
            [[[2,7],[9,7]],[8,[3,8]]]
            [[[0,2],6],[[9,[6,5]],[[3,9],1]]]
            [[7,[[3,4],[2,8]]],[[[4,1],4],7]]
            [[3,[[3,4],6]],[[3,9],[[4,5],[3,0]]]]
            [[[5,[5,1]],[2,4]],[1,[[1,6],6]]]
            [[[5,6],[[1,3],[5,0]]],[[[4,1],8],[5,5]]]
            [[[[2,0],7],[[8,9],1]],[[[4,0],[1,6]],1]]
            [[[2,0],[[4,2],[9,9]]],[4,9]]
            [[[[1,9],6],2],[[5,4],[2,4]]]
            [[[[4,1],[4,5]],[[2,3],2]],[3,[[8,8],1]]]
            [[[[8,1],0],[2,2]],[[2,[7,1]],1]]
            [[[7,4],[[1,3],5]],[[6,8],[[0,0],2]]]
            [[[1,2],8],[[[1,7],[4,0]],[[8,2],8]]]
            [[[0,8],[3,6]],[[[5,3],7],[9,7]]]
            [[4,6],[[[7,9],[7,5]],[[4,6],[8,4]]]]
            [[[[7,3],0],[[6,2],[7,2]]],[9,[[8,0],3]]]
            [[[3,0],1],[[2,3],1]]
            [[[5,[8,6]],[[1,2],2]],[[[1,4],6],[5,[7,1]]]]
            [[[[1,5],8],[0,0]],4]
            [[[7,[6,8]],3],[[5,1],[[2,8],[4,6]]]]
            [3,[[[5,8],[4,5]],[[7,7],8]]]
            [[6,[7,[8,2]]],[[9,0],0]]
            [[[8,[7,6]],1],[[2,4],6]]
            [[[[0,4],2],[0,7]],[6,6]]
            [1,[[1,9],[9,3]]]
            [[[[5,2],[5,3]],[[9,0],4]],2]
            [[[[5,5],3],[7,[1,2]]],[6,[7,2]]]
            [[[[2,1],3],8],[[2,[8,2]],[7,4]]]
            [[8,[9,[1,8]]],[[[4,4],[0,6]],[6,3]]]
            [[[1,6],[1,[2,5]]],0]
            [[[[0,1],[7,2]],[[7,2],3]],[2,[[7,8],[0,7]]]]
            [[[[1,8],8],[[5,7],[3,4]]],[[[2,5],[7,4]],[[8,4],9]]]
            [[[2,2],[5,[1,0]]],[[[6,6],[3,0]],[[8,5],5]]]
            [[[[8,2],[4,8]],[9,4]],[[8,[7,9]],0]]
            [[3,[5,[2,4]]],[[[8,1],0],[[0,4],[4,5]]]]
            [[5,[9,[3,8]]],[4,[1,[5,2]]]]
            [[[3,[0,6]],[7,[8,7]]],[[6,8],[[8,7],0]]]
            [[[[0,2],5],[4,6]],3]
            [[6,7],[[1,[4,6]],9]]
            [7,[3,[[8,8],5]]]
       '''

        nums = []
        for s in input.split('\n'):
            s = s.strip()
            if len(s) > 0 and not s.startswith('#'):
                num = SnailNum.read(s)
                nums.append(num)
        num1, num2, sum, mag = SnailNum.largest_mag(nums)
        print(f'\n\nAnswer: {mag}\n\n')

if __name__ == '__main__':
    unittest.main()