import fileinput
import itertools
from collections import Counter


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

    node = 'AAA'
    steps = 0
    instructions = itertools.cycle(instructions)
    while node != 'ZZZ':
        instr = next(instructions)
        node = network[node][instr]
        steps += 1
    print(steps)


if __name__ == '__main__':
    main()