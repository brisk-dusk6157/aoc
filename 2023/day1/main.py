import fileinput
from pprint import pprint
import string
from collections import defaultdict

M = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def construct_prefix_tree(source):
    def ndict():
        return defaultdict(ndict)

    result = ndict()
    for word, value in source.items():
        cont = result
        for letter in word:
            cont = cont[letter]
        cont["VALUE"] = value
    return result


PREFIX_TREE = construct_prefix_tree(M)


def calibration_value(line: str, spell_tree):
    i = 0
    first = None
    last = None

    while i < len(line):
        letter = line[i]
        if letter in string.digits:
            first = int(letter)
            break
        elif letter in spell_tree:
            j = i
            f = spell_tree
            while j < len(line) and line[j] in f:
                f = f[line[j]]
                j += 1
            if 'VALUE' in f:
                first = f['VALUE']
                break
        i += 1

    i = len(line)-1
    last = None
    while i >= 0:
        letter = line[i]
        if letter in string.digits:
            last = int(letter)
            break
        elif letter in spell_tree:
            j = i
            f = spell_tree
            while j < len(line) and line[j] in f:
                f = f[line[j]]
                j += 1
            if 'VALUE' in f:
                last = f['VALUE']
                break
        i -= 1
    print(line, first, last)
    return first * 10 + last


def main():
    sum1 = 0
    sum2 = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        # sum1 += parse(line, {})
        sum2 += calibration_value(line, PREFIX_TREE)
    print(sum1, sum2)


if __name__ == '__main__':
    main()