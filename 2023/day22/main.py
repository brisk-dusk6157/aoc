import fileinput
import functools
from collections import defaultdict
from email.policy import default

import numpy as np


def main():
    blocks = []
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        start, end = line.split('~')
        c1 = (x1, y1, z1) = [int(t) for t in start.split(',')]
        c2 = (x2, y2, z2) = [int(t) for t in end.split(',')]
        min_x = min(x1, x2, min_x)
        min_y = min(y1, y2, min_y)
        max_x = max(x1, x2, max_x)
        max_y = max(y1, y2, max_y)
        blocks.append((c1, c2))

    blocks.sort(key=lambda block: min(block[0][2], block[1][2]))

    # height map
    H = np.zeros((max_x - min_x + 1, max_y - min_y + 1), dtype=np.uint16)
    # block map
    B = np.zeros((max_x - min_x + 1, max_y - min_y + 1), dtype=np.uint16)

    supported_by = defaultdict(set)
    supports = defaultdict(set)
    for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(blocks, start=1):
        idx = slice(x1,x2+1),slice(y1,y2+1)
        Hr = H[idx]
        for s in np.unique(np.where(H == Hr.max(), B, 0)[idx]):
            if s == 0:  # ground
                continue
            supported_by[i].add(s)
            supports[s].add(i)
        H[idx] = Hr.max() + (z2-z1+1)
        B[idx] = i

    can_remove = 0
    for i, _ in enumerate(blocks, start=1):
        if all([len(supported_by[t]) > 1 for t in supports[i]]):
            can_remove += 1
    print('can remove', can_remove)

    def will_fall_chain(removed):
        falls = {b for r in removed for b in supports[r]-removed if supported_by[b].issubset(removed)}
        if falls:
            return will_fall_chain(falls | removed)
        return removed

    will_fall_count = 0
    for i, _ in enumerate(blocks, start=1):
        will_fall_count += len(will_fall_chain({i})) - 1
    print('will fall', will_fall_count)







if __name__ == '__main__':
    main()

