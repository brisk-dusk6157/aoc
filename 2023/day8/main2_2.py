import fileinput
import itertools
from collections import Counter
from functools import reduce


def main():
    instructions = []
    network = {}
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        if i == 0:
            for c in line:
                if c == 'L':
                    instructions.append(0)
                elif c == 'R':
                    instructions.append(1)
                else:
                    raise ValueError('Impossible')
        elif not line:
            continue
        else:
            source = line[:3]
            left = line[7:10]
            right = line[12:15]
            network[source] = (left, right)

    steps_nodes = []
    for node in [n for n in network.keys() if n[2] == 'A']:
        steps = 0
        instructions = itertools.cycle(instructions)
        while not node[2] == 'Z':
            instr = next(instructions)
            node = network[node][instr]
            steps += 1

        steps_nodes.append(steps)
        print(steps)

    print(reduce(lcm, steps_nodes))


def lcm(x, y):
    from math import gcd # or can import gcd from `math` in Python 3
    return x * y // gcd(x, y)


if __name__ == '__main__':
    main()