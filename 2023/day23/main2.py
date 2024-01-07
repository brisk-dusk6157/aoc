import fileinput
from collections import deque, defaultdict
from pprint import pprint

L = (0, -1)
T = (-1, 0)
R = (0, 1)
B = (1, 0)
LOOKAROUND = [L, T, R, B]

SLOPE_DIR = {
    '<': L,
    '^': T,
    '>': R,
    'v': B,
}

impossible_climb = {
    (L, '>'),
    (T, 'v'),
    (R, '<'),
    (B, '^'),
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
    m = {}
    N, M = 0, 0
    sr, sc = None, None
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            if i == 0 and c == '.':
                sr, sc = i, j
            m[i, j] = c
    er, ec = None, None
    for j in range(M):
        if m[N - 1, j] == '.':
            er, ec = N - 1, j
            break
    start = sr, sc
    end = er, ec

    def neighbours(cursor, prev):
        i0, j0 = cursor
        if cursor == end:
            return [], False, True
        visible = []
        walkable = []
        for d in LOOKAROUND:
            di, dj = d
            i1, j1 = i0 + di, j0 + dj
            if (i1, j1) != prev and m[i1, j1] != '#':
                visible.append((i1, j1))
                walkable.append((i1, j1))
                # respect_slope_of_origin = (m[i0, j0] not in SLOPE_DIR or SLOPE_DIR[m[i0, j0]] == d)
                # respect_slop_of_dest = (d, m[i1, j1]) not in impossible_climb
                # if respect_slope_of_origin and respect_slop_of_dest:
                #     walkable.append((i1, j1))
        return walkable, len(visible) > 1, False

    def build_graph():
        graph = defaultdict(dict)
        q = deque()
        q.append(
            ((-1, 1), start)
        )
        while q:
            intersection, cursor = q.popleft()
            counter = 1
            directed = False
            prev = intersection
            while True:
                # if m[cursor] in SLOPE_DIR:
                #     directed = True
                walkable, is_intersection, is_end = neighbours(cursor, prev)
                if not walkable and not is_end:
                    # deadend
                    break
                elif is_intersection or is_end:
                    # intersection
                    if cursor not in graph[intersection]:
                        graph[intersection][cursor] = counter
                        if not directed:
                            graph[cursor][intersection] = counter
                        for tile in walkable:
                            q.append((cursor, tile))
                    break
                else:
                    prev = cursor
                    cursor = walkable[0]
                    counter += 1
        return graph

    graph = build_graph()
    pprint(graph)

    def maxpath(source, destination, path=set()):
        if source == destination:
            return 0
        maxlen = float('-inf')
        for node, edgelen in graph[source].items():
            if node not in path:
                m = maxpath(node, destination, path | {source})
                maxlen = max(m+edgelen, maxlen)
        return maxlen

    print(maxpath((sr-1, sc), end)-1)


if __name__ == '__main__':
    main()
