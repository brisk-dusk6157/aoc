import fileinput
from pprint import pprint


def is_past(x0, y0, dx, dy, x, y):
    return (x - x0) / dx < 0 or (y - y0) / dy < 0


def main():

    def read_points():
        points = []
        for i, line in enumerate(fileinput.input()):
            line = line.strip()
            pos, vel = line.split('@')
            x, y, z = [int(v.strip()) for v in pos.split(',')]
            dx, dy, dz = [int(v.strip()) for v in vel.split(',')]
            points.append(((x, y, z), (dx, dy, dz)))
        return points

    points = read_points()

    pprint(sorted(points, key=lambda x: x[0][1]))

    counter = 0
    for i, ((x1, y1, _), (dx1, dy1, _)) in enumerate(points):
        for j, ((x2, y2, _), (dx2, dy2, _)) in enumerate(points):
            if i >= j:
                continue
            m1 = dy1 / dx1
            c1 = y1 - m1 * x1
            m2 = dy2 / dx2
            c2 = y2 - m2 * x2

            if m1 == m2:
                if c1 != c2:
                    # parallel
                    continue
                elif abs(dx1) + abs(dy1) != abs(dx1 + dy1):
                    # same line, opposite direction
                    continue
                else:
                    # same line, same direction
                    counter += 1

            x_inter = (c2 - c1) / (m1 - m2)
            y_inter = m1 * x_inter + c1
            if is_past(x1, y1, dx1, dy1, x_inter, y_inter) or is_past(x2, y2, dx2, dy2, x_inter, y_inter):
                continue
            elif 200000000000000 <= x_inter <= 400000000000000 and 200000000000000 <= y_inter <= 400000000000000:
                # elif 7 <= x_inter <= 21 and 7 <= y_inter <= 21:
                counter += 1
    print(counter)


if __name__ == '__main__':
    main()
