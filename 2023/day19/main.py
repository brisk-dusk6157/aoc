import fileinput


def f(line):
    return 0


def main():
    workflows = {}
    workflows_parsed = False
    totalsum = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        if not line:
            workflows_parsed = True
            continue
        if not workflows_parsed:
            wname, wdef = line[:-1].split('{')
            workflows[wname] = []
            for wd in wdef.split(','):
                if ':' in wd:
                    cond, wnext = wd.split(':')
                    step = ('COND', cond, wnext)
                else:
                    wnext = wd
                    step = ('GOTO', wnext)
                workflows[wname].append(step)
        else:
            # print(line)
            values = {}
            for d in line[1:-1].split(','):
                t, v = d.split('=')
                values[t] = int(v)
            # print(values)

            w = 'in'
            while w not in ('A', 'R'):
                for step in workflows[w]:
                    if step[0] == 'COND':
                        if eval(step[1], {}, values):
                            w = step[2]
                            break
                    else:
                        w = step[1]
            if w == 'A':
                # print(values, list(values.values()), list(values.values()))
                totalsum += sum(list(values.values()))

    print(totalsum)



if __name__ == '__main__':
    main()

