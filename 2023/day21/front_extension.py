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
            print_m[-1].append(m[i, j])
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
            m[i, j] = c
            if c == 'S':
                sr, sc = i, j
                m[i, j] = '.'

    # print_map(m, N, M)

    back = set()
    front = {(sr, sc)}
    result = 0
    STEPS = 199
    rem = STEPS % 2
    for step in range(0, STEPS+1):
        # print(f"#{step}", len(front), result)
        if step % 2 == rem:
            result += len(front)

        new_front = []
        for i0, j0 in front:
            for di, dj in (T, R, B, L):
                i = i0 + di
                j = j0 + dj
                if m[i % N, j % M] == '.' and (i,j) not in back:
                    new_front.append((i, j))
        new_front = set(new_front)
        back, front = front, new_front

    print(result)


if __name__ == '__main__':
    main()
