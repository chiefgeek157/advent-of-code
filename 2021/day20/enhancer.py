import colorama
from colorama.ansi import clear_screen
from colorama import Fore, Style, Cursor
from image import Image
import os

class Enhancer():

    DEFAULT_PATCH_SIZE = 3

    # Turn a line of '.' and '#' into an array of 0 and 1
    def read(self, f):
        line = f.readline()
        self.__code = [1 if c == '#' else 0 for c in line.strip()]

        # Sanity check
        if self.code(0) == 1 and self.code(511) == 1: raise ValueError('Code pos 0 and 511 are both 1')

        # Set swap infinite
        self.__swap_infinite = True if self.code(0) == 1 and self.code(511) == 0 else False

    def enhance(self, image, passes=1, size=None):
        if size is None: size = Enhancer.DEFAULT_PATCH_SIZE
        elif size < 0 or (size % 2) != 1: raise ValueError('size must be positive and odd')

        # self.print_info(image, None, 0, 0, size)

        print(f'Enhancer.enhance(passes={passes}, size={size})')
        d = int((size - 1)/2)
        for i in range(passes):
            data = []
            for y in range(-d, image.height() + d):
                row = []
                for x in range(-d, image.width() + d):
                    # self.print_info(image, data, x, y, size, None, f'coords [{x:-3},{y:-3}]')
                    row += self.enhance_value_at(image, x, y, size)
                    # print(f'row={self.row_str(row)}')
                    # input('Enter...')
                data.append(row)
                # print(f'\ndata={self.data_str(data)}')
                # input('Enter...')
            image = Image(data, not image.infinite_ones())
            print(f'After pass {i} image\n{image}')
        return image

    # Return the enhanced value at the given point
    def enhance_value_at(self, image, x, y, size):
        if size is None: size = Enhancer.DEFAULT_PATCH_SIZE
        elif size < 0 or (size % 2) != 1: raise ValueError('size must be positive and odd')

        # print(f'\nenhance_value_at({x},{y})')
        p = image.get_patch(x, y, size)
        # print(f'p={p}')
        i = int(p, 2)
        # print(f'i={i}')
        v = self.code(i)
        # print(f'enhance_value_at({x},{y}) p={p} i={i} v={v}')
        return str(v)

    def code(self, i):
        return self.__code[i]

    def swap_infinite(self):
        return self.__swap_infinite

    def __init__(self):
        self.__code = None
        self.__swap_infinite = False

    def __str__(self):
        s = ''
        for d in self.__code:
            s += str(d)
        return s

    def data_str(self, data):
        s = ''
        for y in range(len(data)):
            if y > 0: s += '\n'
            s += self.row_str(data[y])
        return s

    def row_str(self, row):
        s = ''
        for x in range(len(row)):
            v = row[x]
            if v == '1': s += f'{Fore.YELLOW}{Style.NORMAL}#'
            else: s += f'{Fore.WHITE}{Style.DIM}.'
        s += f'{Style.RESET_ALL}'
        return s

    def print_info(self, image, data, x, y, size, message=None, info=None):
        image_lines = 11
        pad = int((image_lines - 1) / 2)
        margin = int(size / 2)

        clear = '\033[2J'
        rst = Style.RESET_ALL

        title_pos = Cursor.POS(0, 1)
        title_sty = Fore.WHITE + Style.BRIGHT

        msg_pos = Cursor.POS(0, 3)
        msg_sty = Fore.CYAN + Style.NORMAL

        info_pos = Cursor.POS(0,5)
        info_sty = Fore.CYAN + Style.NORMAL
        img_pos = Cursor.POS(0, 7)
        img_num = Fore.WHITE + Style.BRIGHT
        img_one = Fore.YELLOW + Style.BRIGHT
        img_zer = Fore.WHITE + Style.DIM
        img_cur = Fore.GREEN + Style.BRIGHT
        img_pat = Fore.RED + Style.BRIGHT
        img_pad = Fore.LIGHTWHITE_EX + Style.DIM

        data_pos = Cursor.POS(0, 20)

        size = os.get_terminal_size()
        message = size
        print(f'{clear}')

        # Title
        print(f'{title_pos}{title_sty}IMAGE ENHANCER{rst}', end='')

        # Message
        if message is not None: print(f'{msg_pos}{msg_sty}{message}{rst}', end='')

        # Image
        if image is not None:
            print(f'{img_pos}', end='')
            for r in range(y - pad, y + pad + 1):
                l = f'{img_num}{r:-3}{rst} '
                for c in range(0 - margin, image.width() + margin):
                    v = image[c,r]
                    if c == x and r == y: l += f'{img_cur}'
                    elif c in range(x-margin,x+margin+1) and r in range(y-margin,y+margin+1): l += f'{img_pat}'
                    elif r < 0 or r >= image.width() or y < 0 or y >= image.height(): l += f'{img_pad}'
                    elif v == '1': l += f'{img_one}'
                    else: l += f'{img_zer}'

                    if v == '1': l += f'#{rst}'
                    else: l += f'.{rst}'
                print(f'{l}')
            print(f'{rst}', end='')

        # Info
        if info is not None: print(f'{info_pos}{info_sty}{info}{rst}', end='')

        # Data
        if data is not None:
            print(f'{data_pos}', end='')
            for r in range(max(0,y - pad), min(y + pad + 1, len(data))):
                l = f'{img_num}{r:3}{rst} '
                for c in range(len(data[r])):
                    v = data[r][c]
                    if c == x and r == y: l += f'{img_cur}'
                    elif v == '1': l += f'{img_one}'
                    else: l += f'{img_zer}'

                    if v == '1': l += f'#{rst}'
                    else: l += f'.{rst}'
                print(f'{l}')
            print(f'{rst}')

colorama.init()