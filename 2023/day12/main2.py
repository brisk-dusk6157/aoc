import fileinput
import functools


@functools.cache
def f(s, p, streak=0):
    if '#' not in s and not p:
        return 1
    if not (s and p):
        return 0
    c = s[0]
    if streak == p[0]:
        if c == '#':
            return 0
        return f(s[1:], p[1:], 0)
    elif streak > 0:
        if c == '.':
            return 0
        return f(s[1:], p, streak+1)
    elif c == '.':
        return f(s[1:], p, 0)
    elif c == '#':
        return f(s[1:], p, 1)
    elif c == '?':
        return f(s[1:], p, 1) + f(s[1:], p, 0)
    else:
        raise ValueError("Impossible")


def main():
    result = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        s, p = line.split()
        p = tuple([int(x) for x in p.split(',')])
        r = f('?'.join([s]*5) + '.', p * 5)
        result += r
        print(f"#{i}, input='''{line}''', result={r}, total={result}")
    print(result)


if __name__ == '__main__':
    main()

