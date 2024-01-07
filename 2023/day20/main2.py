import copy
from pprint import pprint
import fileinput
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt


def main():
    types = defaultdict(lambda: None)
    outputs = defaultdict(list)
    inputs = defaultdict(list)
    state = defaultdict(lambda: None)
    for line in fileinput.input():
        line = line.strip()
        name, outputs_str = line.split(' -> ')
        if name[0] in '%&':
            t, name = name[0], name[1:]
            types[name] = t
            if t == '%':
                state[name] = False
            else:
                state[name] = {}
        else:
            types[name] = name

        for output in outputs_str.split(','):
            output = output.strip()
            outputs[name].append(output)
            inputs[output].append(name)
    for name, iis in inputs.items():
        if types[name] == '&':
            state[name] = {i: False for i in iis}

    # print('types')
    # pprint(types)
    # print('\n'.join(types.keys()))
    # print('outputs')
    # pprint(outputs)
    # print('\n'.join(f'{s} {d}' for s, ds in outputs.items() for d in ds))
    # print('inputs')
    # pprint(inputs)
    # print('initial state')
    # pprint(state)
    #
    # G = nx.DiGraph()
    # for n, t in types.items():
    #     G.add_node(n, color='red' if t == '&' else 'green')
    # for n, os in outputs.items():
    #     G.add_edges_from([(n, o) for o in os])
    # print(G.number_of_nodes())
    # print(G.number_of_edges())
    # fig, ax = plt.subplots()
    # nx.draw(G, with_labels=True)
    # plt.show()

    def handle(source, destination, pulse):
        # print(source, destination, pulse)
        if types[destination] == 'broadcaster':
            for dest in outputs[destination]:
                yield destination, dest, pulse
        elif types[destination] == '%':
            if not pulse:
                # if off, send high and switch to on
                # if on, send low and switch to off
                for dest in outputs[destination]:
                    yield destination, dest, not state[destination]
                state[destination] = not state[destination]
        elif types[destination] == '&':
            state[destination][source] = pulse
            allhigh = all(state[destination].values())
            for dest in outputs[destination]:
                yield destination, dest, not allhigh
        else:
            pass
            # print('noop', source, destination, pulse)

    initial_state = copy.deepcopy(state)
    presses_list = []
    print(outputs['broadcaster'])
    for x in outputs['broadcaster']:
        print(x)
        state = initial_state
        presses = 0
        reached = False
        while not reached:
            presses += 1

            q = deque()
            q.append(('broadcaster', x, False))
            while q and not reached:
                source, destination, pulse = q.popleft()
                if source in inputs['ls'] and destination == 'ls' and pulse:
                    reached = True
                    break
                for signal in handle(source, destination, pulse):
                    q.append(signal)
        presses_list.append(presses)
    print(presses_list)

    print(lcm(*presses_list))


def lcm(*xs):
    from math import gcd
    result = 1
    for x in xs:
        result = (x * result) // gcd(x, result)
    return result


if __name__ == '__main__':
    main()