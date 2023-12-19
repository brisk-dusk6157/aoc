import fileinput


def print_map(m, N, M):
    print_m = []
    for i in range(N):
        print_m.append([])
        for j in range(M):
            print_m[-1].append(m[i,j])
    print('\n'.join([''.join(xs) for xs in print_m]))
    print(N, M)


def f(line):
    return 0


def main():
    result = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        r = f(line)
        result += r
        print(i, line, r, result)

    m = {}
    N, M = 0, 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            m[i,j] = c


if __name__ == '__main__':
    main()

