import fileinput
import itertools
from collections import Counter
from functools import reduce


def main():
    s = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        xs = [int(x) for x in line.split()]
        lasts_rev = [xs[-1]]
        while not all([x == 0 for x in xs]):
            xs = [xs[i]-xs[i-1] for i in range(1, len(xs))]
            lasts_rev.insert(0, xs[-1])

        for i, a in enumerate(lasts_rev):
            if i == 0:
                continue
            lasts_rev[i] += lasts_rev[i-1]

        s += lasts_rev[-1]
    print(s)



if __name__ == '__main__':
    main()
