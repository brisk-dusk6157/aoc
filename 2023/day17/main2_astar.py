import copy
import fileinput
import functools
from collections import deque, Counter, defaultdict
from pprint import pprint
import heapq


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
    costs = {}
    N, M = 0, 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            costs[i, j] = int(c)
    # print_map(costs, N, M)

    def h(node):
        i, j, streak, direction = node
        return N-1 - i + M-1 - j

    # (row, col, streak, direction)
    start = (0, 0, 0, (0, 1))

    path = []
    cameFrom = {}

    seen = set()
    q = []
    g_score = defaultdict(lambda: float("inf"))
    g_score[start] = 0

    f_score = defaultdict(lambda: float("inf"))
    f_score[start] = h(start)

    it = 0
    heapq.heappush(q, (f_score[start], start))
    seen.add(start)
    min_heat_loss = None
    while q:
        _, (row, col, streak, direction) = _, current = heapq.heappop(q)

        # it += 1
        # if it % 1000 == 0:
        #     print('#', it, row, col, streak, direction, len(q))

        if row == N - 1 and col == M - 1 and 4 <= streak <= 10:
            min_heat_loss = g_score[current] - h(current)
            path = [(row, col)]
            c = current
            while c[:2] != (0, 0):
                c = cameFrom[c]
                path.append(c[:2])
            break
        else:
            neighbours = []
            if streak < 10:
                di, dj = direction
                neighbours.append((row + di, col + dj, streak + 1, direction))
            # streak == 0 is a special case for start node
            if streak >= 4 or streak == 0:
                if direction in ((-1, 0), (1, 0)):
                    neighbours.append((row, col - 1, 1, (0, -1)))
                    neighbours.append((row, col + 1, 1, (0, 1)))
                if direction in ((0, 1), (0, -1)):
                    neighbours.append((row - 1, col, 1, (-1, 0)))
                    neighbours.append((row + 1, col, 1, (1, 0)))

            for neighbour in neighbours:
                row1, col1, _, _ = neighbour
                if not (0 <= row1 < N and 0 <= col1 < M):
                    continue
                tentative_g_score = g_score[current] + costs[row1, col1]
                if tentative_g_score < g_score[neighbour]:
                    cameFrom[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    priority = f_score[neighbour] = tentative_g_score + h(neighbour)
                    if neighbour not in seen:
                        heapq.heappush(q, (priority, neighbour))
                        seen.add(neighbour)

    for i, j in path:
        costs[i, j] = ','
    # print_map(costs, N, M)
    print(min_heat_loss)


if __name__ == '__main__':
    main()
