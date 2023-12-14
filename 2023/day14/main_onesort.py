import fileinput
from collections import OrderedDict

import numpy as np

t = {'O': 1, '.': 0, '#': 2}

# depends only on shape
# array of shape (R*C,)
ROWIDX_CACHE = None

# depends on 1) platform # positions and 2) platform orientation
# dict of {0..3: array of shape (R*C,)}
PLACETAGS_CACHE = {}


def tilt_east(platform, direction):
    """
    platform:
    #O.
    .#O
    O..

    #O..#OO..  <- flattened

    210021100  <- converted to digits
    011123333  <- placetags (tracks position)
    000111222  <- rowidx
    after lexical sorting (rowidx, placetags, platform)
    201021001  <- sorted flattened platform
    #.O.#O..O  <- sorted flattened platform

    platform tilted east:
    #.0
    .#O
    ..O
    """

    shape = platform.shape
    platform = platform.flatten()

    global ROWIDX_CACHE
    if ROWIDX_CACHE is None:
        ROWIDX_CACHE = np.repeat(np.arange(shape[0]), shape[1])
    if direction not in PLACETAGS_CACHE:
        # in placetags
        # - every uninterrupted stretch of . has the same tag
        # - every # has distinct tag
        # - values are nondecreasing
        blocks = np.where(platform == 2, 1, 0)
        # shift right, so that the stretch right after the block gets a new tag
        blocks1 = np.roll(blocks, shift=1)
        blocks1[0] = 0  # np.roll reintroduces last element at the beginning
        PLACETAGS_CACHE[direction] = np.cumsum(blocks | blocks1)

    # note: sort key priority INcreases
    indices = np.lexsort((platform, PLACETAGS_CACHE[direction], ROWIDX_CACHE))

    return platform[indices].reshape(shape)


def full_cycle(platform):
    for i in range(4):
        platform = np.rot90(platform, 3)
        platform = tilt_east(platform, i)
    return platform


def main():
    platform = np.array([[t[x] for x in line.strip()] for line in fileinput.input()], dtype=np.uint8)
    # [[10], [9], [8], ...]]
    weights = np.arange(platform.shape[1], 0, -1).reshape(-1, platform.shape[1]).T

    def weight(platform):
        return (np.where(platform == 2, 0, endstate) * weights).sum()


    CYCLES = 1_000_000_000
    history = OrderedDict()
    history[platform.tobytes()] = 0
    for cycle_idx in range(1, CYCLES + 1):
        platform = full_cycle(platform)
        encoded = platform.tobytes()
        if seen_idx := history.get(encoded, None):
            period = cycle_idx - seen_idx
            endstate_idx = seen_idx + (CYCLES - seen_idx) % period
            endstate_encoded = list(history.keys())[endstate_idx]
            endstate = np.frombuffer(endstate_encoded, dtype=np.uint8).reshape(platform.shape)
            print(cycle_idx, weight(endstate))
            break
        history[encoded] = cycle_idx


if __name__ == '__main__':
    main()
