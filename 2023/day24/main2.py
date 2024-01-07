import fileinput
from pprint import pprint
import numpy as np
from regions import build_region, iterate_region, point_in_region


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
            points.append((x, y, z, dx, dy, dz))
        return points

    points = read_points()
    arr = np.array(points)
    np.save('arr_full.npy', arr)
    X = np.array([p[0] for p in points])
    Y = np.array([p[1] for p in points])
    Z = np.array([p[2] for p in points])
    dX = np.array([p[3] for p in points])
    dY = np.array([p[4] for p in points])
    dZ = np.array([p[5] for p in points])

    regionX = build_region(X, dX)
    regionY = build_region(Y, dY)
    regionZ = build_region(Z, dZ)

    print(regionX)
    print(regionY)
    print(regionZ)
    i = 0
    for px, vx in iterate_region(regionX, vsteps=3, psteps=10):
        if i % 100000 == 0:
            print(i, px, vx)
        i += 1
        T12 = (X[:2]-px) / (vx - dX[:2])
        vy = ((Y[0] - Y[1]) + (dY[0] * T12[0] - dY[1] * T12[1])) / (T12[0] - T12[1])
        py = Y[0] + dY[0] * T12[0] - vy * T12[0]
        vz = ((Z[0] - Z[1]) + (dZ[0] * T12[0] - dZ[1] * T12[1])) / (T12[0] - T12[1])
        pz = Z[0] + dZ[0] * T12[0] - vz * T12[0]
        if np.isinf([vy, py, vz, pz]).any():
            continue
        if not (point_in_region(py, vy, regionY) and point_in_region(pz, vz, regionZ)):
            continue
        TX = (X - px) / (vx - dX)
        TY = (Y - py) / (vy - dY)
        TZ = (Z - pz) / (vz - dZ)
        print(TX, TY, TX - TY)
        if not areq(TX, TY):
            continue
        if not areq(TX, TZ):
            continue

        # found
        print('found', px, py, pz, vx, vy, vz)
        print(px + py + pz)
        break


def areq(x, y):
    return ((x == y) | (np.isnan(x) & ~np.isnan(y)) | (~np.isnan(x) & np.isnan(y))).all()


if __name__ == '__main__':
    main()
