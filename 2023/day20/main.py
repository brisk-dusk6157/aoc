from pprint import pprint
import fileinput
from collections import defaultdict, deque


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

    pprint(types)
    pprint(outputs)
    pprint(inputs)
    pprint(state)

    def handle(source, destination, pulse):
        print(source, destination, pulse)
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
            print('noop', source, destination, pulse)

    result = [0, 0]
    for i in range(1000):
        q = deque()
        q.append(('button', 'broadcaster', False))
        while q:
            source, destination, pulse = q.popleft()
            result[pulse] += 1
            for signal in handle(source, destination, pulse):
                q.append(signal)
        print(state)
    lows, highs = result
    print(lows * highs)




if __name__ == '__main__':
    main()