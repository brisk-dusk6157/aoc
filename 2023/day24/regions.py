minf = float('-inf')
inf = float('inf')


def build_region(P, V):
    union = [((minf, inf), (minf, inf))]
    for p, v in sorted(zip(P, V)):
        nunion = []
        for p1, (vbot, vtop) in union[:-1]:
            if vtop < v:
                continue
            nunion.append((p1, (max(vbot, v), vtop)))
        (pleft, pright), (vbot, vtop) = union[-1]
        if p == pleft:
            nunion.append(((pleft, pright), (vbot, min(vtop, v))))
        else:  # p > pleft
            if vtop >= v:
                nunion.append((
                    (pleft, p), (v, vtop)
                ))
            nunion.append((
                (p, pright), (vbot, min(v, vtop))
            ))
        union = nunion
    return union


def iterate_region(union, vsteps=100, psteps=1000000):
    for (pleft, pright), (vbot, vtop) in union[2:-1]:
        for v in range(vbot, vtop + 1):
            for p in range(pleft, pright + 1):
                yield p, v

    (_, pright), (vbot, _) = union[0]
    for v in range(vbot, vbot + vsteps):
        for p in range(pright, pright - psteps, -1):
            yield p, v

    print('here')
    (pleft, _), (_, vtop) = union[-1]
    for v in range(vtop, vtop - vsteps, -1):
        for p in range(pleft, pleft + psteps):
            yield p, v


def point_in_region(p, v, union):
    for (pleft, pright), (vbot, vtop) in union:
        if pleft <= p <= pright and vbot <= v <= vtop:
            return True
    return False


if __name__ == '__main__':
    union = build_region([1, 2, -1, 7], [1, -2, -1, 3])
    print(union)
    for p, v in iterate_region(union, vsteps=3, psteps=5):
        print(p, v)
