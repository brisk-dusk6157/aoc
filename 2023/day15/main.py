import fileinput
from collections import OrderedDict
from pprint import pprint


def HASH(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h



def main():
    xs = next(fileinput.input()).strip().split(',')
    print(sum(HASH(x) for x in xs))

    boxes = [
        OrderedDict() for _ in range(256)
    ]

    def remove(label, box):
        boxes[box].pop(label, None)

    def insert(label, box, focus_length):
        boxes[box][label] = focus_length

    steps = [
        (remove, (x[:-1], HASH(x[:-1]))) if '-' in x else (insert, (x[:-2], HASH(x[:-2]), int(x[-1:])))
        for x in xs
    ]

    for step, args in steps:
        step(*args)

    result = 0
    for b, box in enumerate(boxes, 1):
        for l, (label, focal_length) in enumerate(box.items(), 1):
            result += (b * l * focal_length)
    print(result)


if __name__ == '__main__':
    main()