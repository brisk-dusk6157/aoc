import copy
import fileinput
import math

T = (-1, 0)
R = (0, 1)
B = (1, 0)
L = (0, -1)


def print_map(m, N, M, out=None):
    print_m = []
    for i in range(N):
        print_m.append([])
        for j in range(M):
            print_m[-1].append(m[i, j])
    print('\n'.join([''.join(xs) for xs in print_m]), file=out)
    print(N, M, file=out)
    print(file=out)


def print_current(step, m, N, M, front, back):
    ii = min(i for i,j in front)
    ai = max(i for i,j in front)
    ij = min(j for i,j in front)
    aj = max(j for i,j in front)
    min_i = - N * ((ai - ii) // N) // 2
    max_i = N * ((ai - ii) // N) // 2 + N
    min_j = - M * ((aj - ij) // M) // 2
    max_j = M * ((aj - ij) // M) // 2 + M

    N1 = max_i - min_i
    M1 = max_j - min_j

    m1 = {}
    for i in range(min_i, max_i+1):
        for j in range(min_j, max_j+1):
            m1[i-min_i, j-min_j] = m[i % N, j % M]

    for i, j in front:
        m1[i-min_i, j-min_j] = 'O'
    for i, j in back:
        m1[i-min_i, j-min_j] = 'o'

    with open(f'animation_test/{step}.txt', 'w') as f:
        print_map(m1, N1, M1, out=f)
        print(sorted(front), file=f)


def main():
    m = {}
    N, M = 0, 0
    sr, sc = None, None
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            m[i, j] = c
            if c == 'S':
                sr, sc = i, j
                m[i, j] = '.'

    def neighbours(tile):
        i0, j0 = tile

        ns = []
        for di, dj in (T, R, B, L):
            i = i0 + di
            j = j0 + dj
            if m[i % N, j % M] == '.':
                ns.append((i, j))
        return ns

    # print_map(m, N, M)

    back1 = set()
    front = {(sr, sc)}
    result = 0
    STEPS = 200
    rem = STEPS % 2
    for step in range(0, STEPS + 1):
        print(f"#{step}", len(front), result)
        # print(front)
        print_current(step, m, N, M, front, back1)
        if step % 2 == rem:
            result += len(front)

        new_front = []
        for i0, j0 in front:
            for di, dj in (T, R, B, L):
                i = i0 + di
                j = j0 + dj
                if m[i % N, j % M] == '.' and (i, j) not in (back1):
                    new_front.append((i, j))
        new_front = set(new_front)

        back1, front = front, new_front

    print(result)


if __name__ == '__main__':
    main()
