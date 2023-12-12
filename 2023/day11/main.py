import fileinput


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
    galaxies = []
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            m[i,j] = c
            if c == '#':
                galaxies.append((i,j))
    di = 0
    dj = 0
    map_idx_i = {}
    map_idx_j = {}
    for i in range(N):
        if all([m[i,j]=='.' for j in range(M)]):
            di += 999999
        map_idx_i[i] = i+di
    for j in range(M):
        if all([m[i,j]=='.' for i in range(N)]):
            dj += 999999
        map_idx_j[j] = j+dj
    galaxies = [(map_idx_i[i], map_idx_j[j]) for i, j in galaxies]
    s = 0
    for g1, (i1, j1) in enumerate(galaxies):
        for g2, (i2, j2) in enumerate(galaxies[g1+1:], g1+1):
            d = (i2 - i1) + abs(j2 - j1)
            s += d
    print(s)


if __name__ == '__main__':
    main()
