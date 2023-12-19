import fileinput
from collections import deque


def product(xs):
    r = 1
    for x in xs:
        r *= x
    return r


def intersect(i1, i2):
    if not (i1 and i2):
        return ()
    x1, y1 = i1
    x2, y2 = i2
    if y1 < x2:
        return ()
    return max(x1, x2), min(y1, y2)


def main():
    workflows = {}
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        if not line:
            break
        wname, wdef = line[:-1].split('{')
        workflows[wname] = []
        for wd in wdef.split(','):
            if ':' in wd:
                cond, wnext = wd.split(':')
                if '<' in cond:
                    c, v = cond.split('<')
                    include = (1, int(v)-1)
                    exclude = (int(v), 4000)
                else:
                    c, v = cond.split('>')
                    exclude = (1, int(v))
                    include = (int(v)+1, 4000)
                step = ('COND', c, include, exclude, wnext)
            else:
                wnext = wd
                step = ('GOTO', wnext)
            workflows[wname].append(step)

    q = deque([('in', {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}, [])])
    result = 0
    while q:
        wname, counts, path = q.pop()
        if wname == 'A':
            result += product(interval[1] - interval[0] + 1 if interval else 0 for interval in counts.values())
        elif wname != 'R':
            for step in workflows[wname]:
                if step[0] == 'GOTO':
                    q.append((step[1], counts, path + [wname]))
                else:
                    category, include, exclude, wnext = step[1:]
                    q.append((wnext, {**counts, category: intersect(include, counts[category])}, path + [wname]))
                    counts = {**counts, category: intersect(exclude, counts[category])}
    print(result)


if __name__ == '__main__':
    main()
