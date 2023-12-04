# red, green, or blue
# secret number of cubes of each color in the bag
# goal is to figure out information about the number of cubes

from pprint import pprint
import fileinput
import re

game_re = re.compile('Game \d+: ((\d+ [a-z]+,?)+;?)+')


def main():
    games = {}
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        label, draws = line.split(':')
        draws = draws.strip()
        _, gid = label.split()
        gid = int(gid)
        games[gid] = []
        for draw in draws.split(';'):
            draw = draw.strip()
            games[gid].append({})
            for color_draw in draw.split(','):
                color_draw = color_draw.strip()
                count, color = color_draw.split()
                games[gid][-1][color] = int(count)

    gid_sum = 0
    for gid, draws in games.items():
        limits = {'red': 12, 'green': 13, 'blue': 14}
        for draw in draws:
            if limits['red'] < draw.get('red', 0) or limits['green']< draw.get('green', 0) or limits['blue'] < draw.get('blue', 0):
                break
        else:
            gid_sum += gid
    print(gid_sum)

    power_sum = 0
    for gid, draws in games.items():
        red = 0
        green = 0
        blue = 0
        for draw in draws:
            if draw.get('red', 0) > red:
                red = draw['red']
            if draw.get('green', 0) > green:
                green = draw['green']
            if draw.get('blue', 0) > blue:
                blue = draw['blue']
        power_sum += red * green * blue
    print(power_sum)


if __name__ == '__main__':
    main()
