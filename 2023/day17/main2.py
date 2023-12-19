import copy
import fileinput
import functools
from collections import deque, Counter, defaultdict
from pprint import pprint


def print_map(m, N, M):
    print_m = []
    for i in range(N):
        print_m.append([])
        for j in range(M):
            print_m[-1].append(m[i, j])
    print('\n'.join([''.join([str(x) for x in xs]) for xs in print_m]))
    print(N, M)


def f(line):
    return 0


def main():
    m = {}
    N, M = 0, 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            m[i, j] = int(c)
    print_map(m, N, M)

    # (row, col, loss, streak, direction)
    q = deque([(0, 0, 0, 0, (0, 1), [])])
    finished = {}

    minlosses = {}
    min_heat_loss = float("inf")
    it = 0
    while q:
        it += 1
        row, col, loss, streak, direction, path = q.popleft()
        if it % 100 == 0:
            print('#', it, row, col, loss, streak, direction, len(path), len(q))
        if row == N - 1 and col == M - 1 and streak == 4:
            min_heat_loss = min(loss + m[row, col], min_heat_loss)
            finished[min_heat_loss] = path
        elif not (0 <= row < N and 0 <= col < M):
            continue
        else:
            if len(path) > 2 * (N + M):
                continue
            new_loss = loss + m[row, col]
            key = (row, col, streak, direction)
            if key in minlosses and new_loss >= minlosses[key]:
                # been here and have a better min loss
                continue
            minlosses[key] = new_loss

            # maintain direction
            if streak < 10:
                di, dj = direction
                q.append((row + di, col + dj, new_loss, streak + 1, direction,
                          path[:] + [(row + di, col + dj),],
                          ))

            if streak >= 4:
                # change direction
                if direction in ((-1, 0), (1, 0)):
                    q.append((row, col - 1, new_loss, 1, (0, -1),
                              path[:] + [(row, col - 1)],
                              ))
                    q.append((row, col + 1, new_loss, 1, (0, 1),
                              path[:] + [(row, col + 1),],
                              ))
                if direction in ((0, 1), (0, -1)):
                    q.append((row - 1, col, new_loss, 1, (-1, 0),
                              path[:] + [(row - 1, col),],
                              ))
                    q.append((row + 1, col, new_loss, 1, (1, 0),
                              path[:] + [(row + 1, col),],
                              ))
    # pprint(minlosses)
    # pprint(finished[min_heat_loss])
    m2 = copy.deepcopy(m)
    for i, j in finished[min_heat_loss]:
        m2[i,j] = ','
    print_map(m, N, M)
    print_map(m2, N, M)
    print(finished[min_heat_loss], len(finished[min_heat_loss]))

    print(min_heat_loss - m[0, 0])


if __name__ == '__main__':
    main()
