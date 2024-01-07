import copy
import fileinput


T = (-1, 0)
R = (0, 1)
B = (1, 0)
L = (0, -1)


def print_map(m, N, M):
    print_m = []
    for i in range(N):
        print_m.append([])
        for j in range(M):
            print_m[-1].append(m[i,j])
    print('\n'.join([''.join(xs) for xs in print_m]))
    print(N, M)


def main():
    m = {}
    N, M = 0, 0
    sr, sc = None, None
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            m[i,j] = c
            if c == 'S':
                sr, sc = i, j
                m[i,j] = '.'

    def neighbours(tile):
        i0, j0 = tile

        ns = []
        for di, dj in (T, R, B, L):
            i = i0 + di
            j = j0 + dj
            if 0 <= i < N and 0 <= j < M and m[i,j] == '.':
                ns.append((i,j))
        return set(ns)

    # print_map(m, N, M)
    reached = {(sr, sc)}
    for step in range(21):
        reached = set().union(*[neighbours(tile) for tile in reached])

    m2 = copy.copy(m)
    for i, j in reached:
        m2[i,j] = 'O'
    print_map(m2, N, M)
    print(sr, sc)
    print(len(reached))




if __name__ == '__main__':
    main()

