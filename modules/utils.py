"""A bunch of utilities"""

def print_vert_header(h_min, h_max, leader='', l_pad='', r_pad=''):
    labels = []
    for h in range(h_min, h_max + 1):
        labels.append(str(h))
    rows = len(max(labels, key=len))
    for i in range(rows):
        line = leader
        for label in labels:
            line += l_pad + label[i] + r_pad
        print(line)
