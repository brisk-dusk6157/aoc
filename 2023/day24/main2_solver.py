import fileinput
from sympy import symbols, nonlinsolve


def main():

    def read_points():
        points = []
        for i, line in enumerate(fileinput.input()):
            line = line.strip()
            pos, vel = line.split('@')
            x, y, z = [int(v.strip()) for v in pos.split(',')]
            dx, dy, dz = [int(v.strip()) for v in vel.split(',')]
            points.append((x, y, z, dx, dy, dz))
        return points

    points = read_points()
    eqs = []
    px, py, pz, vx, vy, vz = symbols('p_x, p_y, p_z, v_x, v_y, v_z')
    ts = []
    for i, (x, y, z, dx, dy, dz) in enumerate(points[:10]):
        ti = symbols(f't_{i}')
        ts.append(ti)
        eqs.append(x + dx * ti - (px + vx * ti))
        eqs.append(y + dy * ti - (py + vy * ti))
        eqs.append(z + dz * ti - (pz + vz * ti))
    print(nonlinsolve(eqs, [px, py, pz, vx, vy, vz, *ts]))



if __name__ == '__main__':
    main()
