import fileinput
from collections import defaultdict
from pprint import pprint


def edges(c, i, j):
    if c == '-':
        return [(i, j - 1), (i, j + 1)]
    elif c == '|':
        return [(i - 1, j), (i + 1, j)]
    elif c == 'L':
        return [(i - 1, j), (i, j + 1)]
    elif c == 'J':
        return [(i - 1, j), (i, j - 1)]
    elif c == 'F':
        return [(i, j + 1), (i + 1, j)]
    elif c == '7':
        return [(i, j - 1), (i + 1, j)]
    else:
        raise ValueError("impossible")


def main():
    graph = defaultdict(set)
    si, sj = None, None
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        for j, c in enumerate(line):
            if c == '.':
                continue
            elif c == 'S':
                si = i
                sj = j
            else:
                for e in edges(c, i, j):
                    graph[(i,j)].add(e)

    candidates = set('|-7JFL')
    if (si, sj) in graph.get((si-1, sj), set()):
        candidates = candidates & set('|JL')
    if (si, sj) in graph.get((si+1, sj), set()):
        candidates = candidates & set('|7F')
    if (si, sj) in graph.get((si, sj-1), set()):
        candidates = candidates & set('-7J')
    if (si, sj) in graph.get((si, sj+1), set()):
        candidates = candidates & set('-FL')
    s = candidates.pop()
    for e in edges(s, si, sj):
        graph[(si, sj)].add(e)

    i, j = None, None
    steps = 0
    seen = set()
    while True:
        if (i,j) == (None,None):
            i, j = si, sj
        seen.add((i,j))
        cands = (graph[(i,j)]-seen)
        try:
            i, j = cands.pop()
        except KeyError:
            break
        steps += 1
    print((steps+1)//2)


if __name__ == '__main__':
    main()



