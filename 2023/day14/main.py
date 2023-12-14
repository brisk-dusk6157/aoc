import fileinput


def tostring(m, R, C):
    a = []
    for i in range(R):
        a.append([])
        for j in range(C):
            a[i].append(m[i, j])
    return '\n'.join([''.join(row) for row in a])


def calculate_load(m, R, C):
    result = 0
    for c in range(C):
        for r in range(R):
            if m[r, c] == 'O':
                result += C - r
    return result


def tilt_north(m, R, C):
    m2 = {}
    for c in range(C):
        start = 0
        count = 0
        for r in range(R + 1):
            if r == R or m[r, c] == '#':
                for r2 in range(start, start + count):
                    m2[r2, c] = 'O'
                for r2 in range(start + count, r):
                    m2[r2, c] = '.'
                m2[r, c] = '#'
                start = r + 1
                count = 0
            elif m[r, c] == 'O':
                count += 1
    return m2


def tilt_west(m, R, C):
    m2 = {}
    for r in range(R):
        start = 0
        count = 0
        for c in range(C + 1):
            if c == C or m[r, c] == '#':
                for c2 in range(start, start + count):
                    m2[r, c2] = 'O'
                for c2 in range(start + count, c):
                    m2[r, c2] = '.'
                m2[r, c] = '#'
                start = c + 1
                count = 0
            elif m[r, c] == 'O':
                count += 1
    return m2


def tilt_south(m, R, C):
    m2 = {}
    for c in range(C):
        start = R-1
        count = 0
        for r in range(R-1, -2, -1):
            if r == -1 or m[r, c] == '#':
                for r2 in range(start, start - count, -1):
                    m2[r2, c] = 'O'
                for r2 in range(start - count, r, -1):
                    m2[r2, c] = '.'
                m2[r, c] = '#'
                start = r - 1
                count = 0
            elif m[r, c] == 'O':
                count += 1
    return m2


def tilt_east(m, R, C):
    m2 = {}
    for r in range(R):
        start = C-1
        count = 0
        for c in range(C-1, -2, -1):
            if c == -1 or m[r, c] == '#':
                for c2 in range(start, start - count, -1):
                    m2[r, c2] = 'O'
                for c2 in range(start - count, c, -1):
                    m2[r, c2] = '.'
                m2[r, c] = '#'
                start = c - 1
                count = 0
            elif m[r, c] == 'O':
                count += 1
    return m2


def cycle(m, R, C):
    m = tilt_north(m, R, C)
    m = tilt_west(m, R, C)
    m = tilt_south(m, R, C)
    m = tilt_east(m, R, C)
    return m


def main():
    R, C = 0, 0
    m = {}
    for r, line in enumerate(fileinput.input()):
        line = line.strip()
        R += 1
        C = len(line)
        for c, tile in enumerate(line):
            m[r, c] = tile

    print(calculate_load(m, R, C))
    h = {tostring(m, R, C): 0}
    r = {0: m}

    for i in range(1, 1000000000+1):
        m = cycle(m, R, C)
        s = tostring(m, R, C)
        if s in h:
            period = i - h[s]
            endstate_idx = h[s] + (1000000000-h[s]) % period
            print(i, calculate_load(r[endstate_idx], R, C))
            break
        h[s] = i
        r[i] = m

        # print(tostring(m, R, C))


if __name__ == '__main__':
    main()
