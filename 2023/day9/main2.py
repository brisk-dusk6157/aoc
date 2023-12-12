import fileinput
import itertools
from collections import Counter
from functools import reduce


def main():
    s = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        xs = [int(x) for x in line.split()]
        firsts_rev = [xs[0]]
        while not all([x == 0 for x in xs]):
            xs = [xs[i]-xs[i-1] for i in range(1, len(xs))]
            firsts_rev.insert(0, xs[0])

        print(firsts_rev)
        for i, a in enumerate(firsts_rev):
            if i == 0:
                continue
            firsts_rev[i] -= firsts_rev[i-1]

        print(firsts_rev)
        print(firsts_rev[-1])

        s += firsts_rev[-1]
    print(s)



if __name__ == '__main__':
    main()
