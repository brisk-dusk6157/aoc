import fileinput


def f(line):
    return 0


def main():
    result = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        r = f(line)
        result += r
        print(i, line, r, result)

    # m = {}
    # for i, line in enumerate(fileinput.input()):
    #     line = line.strip()
    #     for j, c in enumerate(line):
    #         m[i,j] = c


if __name__ == '__main__':
    main()

