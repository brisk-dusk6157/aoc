from itertools import chain, combinations
from pprint import pprint
from collections import deque

FINAL = 4

# ((elevator, generators, microchips), (step, history))
input_test = (
    (1, (2, 3), (1, 1)),
    (0, ()))
input_part1 = (
    # thilium, plutonium, strontium, promethium, ruthenium
    (1, (1, 1, 1, 3, 3),
        (1, 2, 2, 3, 3)),
    (0, ())
)
input_part2 = (
    # thilium, plutonium, strontium, promethium, ruthenium, elerium, dilithium
    (1, (1, 1, 1, 3, 3, 1, 1),
        (1, 2, 2, 3, 3, 1, 1)),
    (0, ())
)


def main():
    # q = [input_test]
    q = deque([input_part2])
    seen = set()
    iteration = 0
    while True:
        iteration += 1
        state, meta = q.popleft()
        elevator, G, M = state
        step, history = meta
        if iteration % 100000 == 0:
            print(iteration, len(q), step, len(seen))
        if state in seen:
            continue
        seen.add(state)
        if all([x == FINAL for x in G+M]):
            print(step, state)
            pprint(list(enumerate(history)))
            break
        for i, m in enumerate(M):
            if m == G[i]:
                # i'th microchip is on the same floor as i'th generator
                continue
            elif m in G:
                # invalid state
                break
        else:
            # valid state, find possible children
            this_floor = ([(0, i) for i, f in enumerate(G) if f == elevator]
                          + [(1, i) for i, f in enumerate(M) if f == elevator])
            for picks in chain(combinations(this_floor, 1),
                               combinations(this_floor, 2)):
                # picks is [(0,0), (0,1)]
                placements = [list(G), list(M)]
                if elevator > 1 and any([x < elevator for x in G+M]) and len(picks) == 1:
                    f = elevator - 1
                    for P, i in picks:
                        placements[P][i] = f
                    G1, M1 = placements
                    q.append(((elevator - 1, tuple(G1), tuple(M1)),
                              (step+1, history)))
                              # (step+1, history + (state,))))
                if elevator < FINAL:
                    f = elevator + 1
                    for P, i in picks:
                        placements[P][i] = f
                    G1, M1 = placements
                    q.append(((elevator + 1, tuple(G1), tuple(M1)),
                              (step+1, history)))
                              #(step+1, history + (state,))))


if __name__ == '__main__':
    main()
