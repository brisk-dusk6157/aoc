import fileinput
from pprint import pprint

import numpy as np



T = (-1, 0)
R = (0, 1)
B = (1, 0)
L = (0, -1)


def print_map(m, N, M):
    print_m = []
    for i in range(N):
        print_m.append([])
        for j in range(M):
            print_m[-1].append(m[i, j])
    print('\n'.join([''.join(xs) for xs in print_m]))
    print(N, M)


def main():
    m = {}
    N, M = 0, 0
    orig_start_row, orig_start_col = sr, sc = None, None
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            if c == 'S':
                orig_start_row, orig_start_col = sr, sc = i, j
                c = '.'
            m[i, j] = c

    SECTORS = 3
    N1, M1 = (2*SECTORS+1) * N, (2*SECTORS+1) * M
    map = np.empty((N1, M1), dtype=np.uint8)
    for i in range(N1):
        for j in range(M1):
            map[i, j] = 0 if m[i % N, j % M] == '.' else 2
    steps = sr + SECTORS * N
    sr += SECTORS * N
    sc += SECTORS * M

    def neighbours(tile):
        i0, j0 = tile

        ns = []
        for di, dj in (T, R, B, L):
            i = i0 + di
            j = j0 + dj
            if map[i, j] == 0:
                ns.append((i, j))
        return ns

    reached = {(sr, sc)}
    for step in range(steps):
        if step % 100 == 0:
            print(step)
        reached = set().union(*[neighbours(tile) for tile in reached])

    for i, j in reached:
        map[i, j] = 1

    # print(map)
    map[map == 2] = 0
    # print(map.sum())
    sums = [[0 for y in range(2*SECTORS+1)] for x in range(2*SECTORS+1)]
    for x in range(2*SECTORS+1):
        for y in range(2*SECTORS+1):
            sums[x][y] = map[x * N:(x + 1) * N, y * M:(y + 1) * M].sum()
    pprint(sums)

    STEPS = 26501365
    K = (STEPS - orig_start_row) // N
    # b = [[0,    0,    958,  5654, 947,  0,    0],
    #      [0,    958,  6568, 7541, 6569, 947,  0],
    #      [958,  6568, 7541, 7483, 7541, 6569, 947],
    #      [5652, 7541, 7483, 7541, 7483, 7541, 5645],
    #      [961,  6567, 7541, 7483, 7541, 6559, 951],
    #      [0,    961,  6567, 7541, 6559, 951,  0],
    #      [0,    0,    961,  5643, 951,  0,    0]]
    result = (
            (sums[0][3] + sums[3][6] + sums[6][3] + sums[3][0])
            + K * (sums[1][1] + sums[1][5] + sums[5][5] + sums[5][1])
            + (K - 1) * (sums[1][2] + sums[2][5] + sums[5][4] + sums[4][1])
            + (K**2) * sums[3][3]
            + ((K-1)**2) * sums[2][3])
    print(result)


if __name__ == '__main__':
    main()
    # a = [[0,    958,  5654, 947,  0],
    #      [958,  6568, 7541, 6569, 947],
    #      [5652, 7541, 7483, 7541, 5645],
    #      [961,  6567, 7541, 6559, 951],
    #      [0,    961,  5643, 951,  0]]
    #
    #
    # steps = 26501365
    # K = (steps - 65) // 131
    # result = (
    #         (5654 + 5652 + 5643 + 5645)
    #         + K * (958 + 947 + 951 + 961)
    #         + (K - 1) * (6568 + 6569 + 6559 + 6567)
    #         + (K**2) * 7541
    #         + ((K-1)**2) * 7483)
    # print(result)