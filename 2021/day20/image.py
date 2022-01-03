from io import DEFAULT_BUFFER_SIZE
import colorama
from colorama import Fore, Style
import math
from os import posix_spawn

class Image():

    def read(self, f):
        data = []
        line = f.readline()
        while line:
            line = line.strip()
            row = ''
            for i in range(len(line)):
                row += '1' if line[i] == '#' else '0'
            data.append(row)
            line = f.readline()
        # print(f'\nImage.read(): read {data}')
        self.data(data, False)

    def width(self):
        return len(self.__rows[0]) if self.__rows is not None else 0

    def height(self):
        return len(self.__rows) if self.__rows is not None else 0

    def infinite_value(self):
        return '1' if self.__infinite_ones else '0'

    def infinite_ones(self):
        return self.__infinite_ones

    def data(self, data, infinite_ones):
        # print(f'Image.data():')
        if data is None:
            self.__rows = None
            self.__infinite = False
        else:
            self.__infinite_ones = infinite_ones

            # Get extents of data
            xmin = len(data[0])
            xmax = 0
            ymin = len(data)
            ymax = 0
            for y in range(len(data)):
                for x in range(len(data[y])):
                    if data[y][x] == '1':
                        xmin = min(xmin, x)
                        xmax = max(xmax, x)
                        ymin = min(ymin, y)
                        ymax = max(ymax, y)

            # print(f'Image.data(): extents are x=[{xmin},{xmax}] y=[{ymin},{ymax}]')
            width  = xmax - xmin + 1
            height = ymax - ymin + 1

            self.__rows = []
            for y in range(height):
                row = ''
                for x in range(width):
                    row += data[y][x]
                self.__rows.append(row)
                # print(f'Image.data(): rows={self.__rows}')

    def get_patch(self, x, y, size):
        if size < 0 or (size % 2) != 1: raise ValueError('size must be positive and odd')
        p = ''
        d = int((size - 1) / 2)
        # print(f'\nget_patch({x},{y}): o={o} d={d} x=[{x+o-d},{x+o+d+1}] y=[{y+o-d},{y+o+d+1}]')
        for i in range(y - d, y + d + 1):
            for j in range(x - d, x + d + 1):
                p += self[j,i]
            # print(f'get_patch({x},{y}): row[{i}]={self.__rows[i]} patch={p}')
        return p

    def as_str(self, full=False):
        x_min = 0
        x_max = len(self.__rows[0])
        y_min = 0
        y_max = len(self.__rows)
        if full:
            o = self.patch_size - 1
            x_min -= o
            x_max += o
            y_min -= o
            y_max += o
        # print(f'\nas_str(full={full}): x=[{x_min},{x_max}] y=[{y_min},{y_max}]')

        s = ''
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                # print(f'as_str: getting __rows[{y}][{x}]')
                v = self[x,y]
                if v == '1': s += f'{Fore.YELLOW}#'
                else:
                    s += '.'
                s += f'{Style.RESET_ALL}'
            s+= '\n'
        return s

    # Return the number of '1' values
    def lit_count(self):
        if self.__infinite_ones: return math.inf
        count = 0
        for r in self.__rows:
            for c in r:
                if c == '1': count += 1
        return count

    def __init__(self, data=None, infinite_ones=False):
        self.__rows = None
        self.data(data, infinite_ones)

    def __getitem__(self, pos):
        x, y = pos
        # print(f'\ngetitem({pos}): width={self.width()} height={self.height()} infinite={self.infinite()}')
        if x < 0 or y < 0 or x >= self.width() or y >= self.height(): return self.infinite_value()
        return self.__rows[y][x]

    def __str__(self):
        return self.as_str()

colorama.init()