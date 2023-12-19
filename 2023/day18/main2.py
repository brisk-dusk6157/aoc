import fileinput

N2D = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U',
}
DIR = {
    'U': (-1, 0),
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
}


def print_map(m, N, M):
    print_m = []
    for i in range(N):
        print_m.append([])
        for j in range(M):
            print_m[-1].append(m[i, j])
    print('\n'.join([''.join(xs) for xs in print_m]))
    print(N, M)


def main():
    instructions = []
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        _, _, color = line.split()
        direction = N2D[int(color[7])]
        steps = int(color[2:7], base=16)

        instructions.append((DIR[direction], int(steps), color))

    i, j = 0, 0
    turns = []
    B = 0
    for (di, dj), s, c in instructions:
        turns.append((i, j))
        B += s
        i += s * di
        j += s * dj

    A = 0
    for (i1, j1), (i2, j2) in zip(turns, turns[1:] + turns[:1]):
        A += (j1 + j2) * (i1 - i2)
    A = abs(A) / 2
    I = A - B / 2 + 1
    print(abs(I + B))
    # print(A, B, I, I + B)


if __name__ == '__main__':
    main()
