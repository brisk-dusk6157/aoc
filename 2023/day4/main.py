import fileinput
import itertools
from collections import defaultdict


def main():
    s = 0
    scores = []
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        l1, l2 = line.split(':')[1].split('|')
        win = {int(x) for x in l1.strip().split()}
        have = {int(x) for x in l2.strip().split()}
        inter = win.intersection(have)
        scores.append(len(inter))
        if inter:
            s += 2**(len(inter)-1)
    print(s)

    copies = [1 for _ in scores]
    for i, score in enumerate(scores):
        # print(i, score, copies[i])
        for j in range(i+1, i+score+1):
            copies[j] += copies[i]

    print(sum(copies))



if __name__ == '__main__':
    main()