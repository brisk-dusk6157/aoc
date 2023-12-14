import fileinput
from collections import OrderedDict

import numpy as np

t = {'O': 1, '.': 0, '#': 2}


def main():
    # platform is modified in place
    platform = np.array([[t[x] for x in line.strip()] for line in fileinput.input()], dtype=np.uint8)

    # [[10], [9], [8], ...]]
    weights = np.arange(platform.shape[1], 0, -1).reshape(-1, platform.shape[1]).T

    # find all vertical and horizontal segments where balls can roll (block/block, block/edge or edge/edge)
    # store views of platform array, so that platform is modified in-place during tilting
    blocks = platform == 2
    horizontal_segments = []
    vertical_segments = []
    for ri in range(platform.shape[0]):
        indices = np.nonzero(blocks[ri, :])[0]
        for segment in np.split(platform[ri, :], indices):
            if len(segment) and segment[0] == 2:
                segment = segment[1:]
            if len(segment):
                horizontal_segments.append(segment)
    for ci in range(platform.shape[1]):
        indices = np.nonzero(blocks[:, ci])[0]
        for segment in np.split(platform[:, ci], indices):
            if len(segment) and segment[0] == 2:
                segment = segment[1:]
            if len(segment):
                vertical_segments.append(segment)

    def full_cycle():
        # north
        for segment in vertical_segments:
            segment[::-1].sort()
        # west
        for segment in horizontal_segments:
            segment[::-1].sort()
        # south
        for segment in vertical_segments:
            segment.sort()
        # east
        for segment in horizontal_segments:
            segment.sort()

    # to simplify weight calculation (information about blocks is already in _segments lists)
    platform[platform == 2] = 0

    CYCLES = 1000000000
    history = OrderedDict()
    history[platform.tobytes()] = 0
    for cycle_idx in range(1, CYCLES + 1):
        full_cycle()
        encoded = platform.tobytes()
        if seen_idx := history.get(encoded, None):
            period = cycle_idx - seen_idx
            endstate_idx = seen_idx + (CYCLES - seen_idx) % period
            endstate_encoded = list(history.keys())[endstate_idx]
            endstate = np.frombuffer(endstate_encoded, dtype=np.uint8).reshape(platform.shape)
            print(cycle_idx, (endstate * weights).sum())
            break
        history[encoded] = cycle_idx


if __name__ == '__main__':
    main()
