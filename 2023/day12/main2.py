import fileinput
import functools


def backtrack(string, pattern):

    @functools.cache
    def b(si, pi, streak):
        if pi == len(pattern) and '#' not in string[si:]:
            return 1
        if pi == len(pattern) or si == len(string):
            return 0

        c = string[si]
        if streak == pattern[pi]:
            if c == '#':
                return 0
            return b(si+1, pi+1, 0)
        elif streak > 0:
            if c == '.':
                return 0
            return b(si+1, pi, streak+1)
        else:
            if c == '.':
                return b(si+1, pi, 0)
            elif c == '#':
                return b(si+1, pi, 1)
            elif c == '?':
                return b(si+1, pi, 0) + b(si+1, pi, 1)
            else:
                raise ValueError("Impo")

    return b(0, 0, 0)


def main():
    result = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        s, p = line.split()
        p = tuple([int(x) for x in p.split(',')])
        # r = backtrack(s + '.', p)
        r = backtrack('?'.join([s]*5) + '.', p * 5)
        result += r
        print(f"#{i}, input='''{line}''', result={r}, total={result}")
    print(result)


if __name__ == '__main__':
    main()
