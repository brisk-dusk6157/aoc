import fileinput
import itertools

ROW = 100
COL = 1
flipped = {'#': '.', '.': '#'}


def first_symmetry(m, N, M, fix_coords=(None, None)):
    def fixed(x, y):
        return m[x,y] if (x,y) != fix_coords else flipped[m[x,y]]

    rows = [''.join([fixed(x, y) for y in range(M)]) for x in range(N)]
    cols = [''.join([fixed(x, y) for x in range(N)]) for y in range(M)]

    def find_symmetries(xs, typ, fix_coord):
        for mid in range(1, len(xs)):
            start = max(0, 2 * mid - len(xs))
            end = min(len(xs), 2 * mid)
            if fix_coord is not None and not (start <= fix_coord < end):
                continue
            l, r = xs[start:mid], xs[mid:end]
            if l == list(reversed(r)):
                yield typ, mid

    for typ, i in itertools.chain(find_symmetries(rows, ROW, fix_coords[0]),
                                  find_symmetries(cols, COL, fix_coords[1])):
        return typ, i
    return None


def main():
    m = {}
    N, M = 0, 0
    p1_result = 0
    p2_result = 0
    for idx, line in enumerate(fileinput.input()):
        line = line.strip()
        if not line:
            sym = first_symmetry(m, N, M)
            p1_result += sym[0] * sym[1]

            for (fix_i, fix_j) in itertools.product(range(N), range(M)):
                sym = first_symmetry(m, N, M, (fix_i, fix_j))
                if sym:
                    p2_result += sym[0] * sym[1]
                    break

            m = {}
            N, M = 0, 0
            continue
        N += 1
        M = len(line)
        for fix_, c in enumerate(line):
            m[N - 1, fix_] = c
    print('p1', p1_result)
    print('p2', p2_result)


if __name__ == '__main__':
    main()
