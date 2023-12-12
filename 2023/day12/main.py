import fileinput


def f(s, p, streak=False, ind=0, concrete=''):
    # print(f"{concrete}|{s}", p)
    if (not s or '#' not in s) and (not p or p == [0]):
        # print("answer", concrete)
        return 1
    if not s and p:
        return 0
    if s and not p:
        return 0

    assert s and p

    c = s[0]
    if p[0] == 0:
        if c == '#':
            return 0
        else:
            p = p[1:]
        streak = False
        if c == '?':
            c = '.'
    if streak:
        if c == '.':
            return 0
        if c == '?':
            c = '#'
    if c == '.':
        return f(s[1:], p, False, ind+1, concrete=concrete + '.')
    elif c == '#':
        return f(s[1:], [p[0]-1] + p[1:], True, ind+1, concrete=concrete + '#')
    elif c == '?':
        return f(s[1:], p, False, ind+1, concrete=concrete + '.') + f(s[1:], [p[0]-1] + p[1:], True, ind+1, concrete=concrete + '#')
    else:
        raise ValueError('impossible')


def main():
    result = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        s, p = line.split()
        p = [int(x) for x in p.split(',')]
        r = f(s, p)
        result += r
        print(s, p, r)
    print(result)


if __name__ == '__main__':
    main()