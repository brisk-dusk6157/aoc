import fileinput
import string
import typing as t


class Interval:

    def is_empty(self):
        raise NotImplementedError

    def scale(self, k) -> 'Interval':
        raise NotImplementedError

    def shift(self, d) -> 'Interval':
        raise NotImplementedError

    def difference(self, other: 'Interval') -> 'Interval':
        raise NotImplementedError

    def difference_segment(self, other: 'Segment') -> 'Interval':
        raise NotImplementedError

    def difference_union(self, other: 'Union') -> 'Interval':
        raise NotImplementedError

    def union(self, other: 'Interval') -> 'Interval':
        raise NotImplementedError

    def union_segment(self, other: 'Segment') -> 'Interval':
        raise NotImplementedError

    def union_union(self, other: 'Union') -> 'Interval':
        raise NotImplementedError

    def intersect(self, source: 'Interval') -> 'Interval':
        raise NotImplementedError

    def intersect_union(self, other: 'Union') -> 'Interval':
        raise NotImplementedError

    def intersect_segment(self, other: 'Segment') -> 'Interval':
        raise NotImplementedError


class Empty(Interval):

    def is_empty(self):
        return True

    def scale(self, k) -> 'Interval':
        return self

    def shift(self, d) -> 'Interval':
        return self

    def intersect(self, other: 'Interval') -> 'Interval':
        return self

    def difference(self, other: 'Interval') -> 'Interval':
        return self

    def union(self, other: 'Interval') -> 'Interval':
        return other


class Segment(Interval):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def intersect(self, other: 'Interval') -> 'Interval':
        return other.intersect_segment(self)

    def intersect_segment(self, other: 'Segment') -> 'Interval':
        if self.start > other.start:
            return other.intersect(self)
        if other.start < self.end:
            return Segment(self.start, min(self.end, other.end))
        else:
            return Empty()

    def intersect_union(self, other: 'Union') -> 'Interval':
        return other.intersect_segment(self)

    def is_empty(self):
        return False

    def scale(self, k) -> 'Interval':
        return Segment(k * self.start, k * self.end)

    def shift(self, d) -> 'Interval':
        return Segment(self.start + d, self.end + d)

    def difference(self, other: 'Interval') -> 'Interval':
        return other.difference_segment(self)

    def difference_segment(self, other: 'Segment') -> 'Interval':
        intersection = self.intersect(other)
        if intersection.is_empty():
            return self

        result = Empty()
        if self.start < intersection.start:
            result = result.union(Segment(self.start, other.start))
        if intersection.end < self.end:
            result = result.union(Segment(intersection.end, self.end))
        return result

    def difference_union(self, other: 'Union') -> 'Interval':
        result = Empty()
        for segment in other.segments:
            result = result.union(self.difference(segment))
        return result

    def union(self, other: 'Interval') -> 'Interval':
        return other.union_segment(self)

    def union_segment(self, other: 'Segment') -> 'Interval':
        if self.intersect(other).is_empty():
            return Union.from_intervals(self, other)
        return Segment(min(self.start, other.start),
                       min(self.end, other.end))

    @classmethod
    def from_start_n(cls, start, n):
        return cls(start, start + n - 1)


class Union(Interval):

    def __init__(self, segments):
        self.segments = segments

    def intersect(self, other: 'Interval') -> 'Interval':
        return other.intersect_union(self)

    def intersect_segment(self, other: 'Segment') -> 'Interval':
        result = Empty()
        for segment in self.segments:
            result = result.union(segment.intersect(other))
        return result

    def intersect_union(self, other: 'Union') -> 'Interval':
        i = 0
        j = 0
        result = Empty()
        while i < len(self.segments) and j < len(other.segments):
            s1 = self.segments[i]
            s2 = other.segments[j]
            intersection = s1.intersect(s2)
            if not intersection.is_empty():
                result = result.union(intersection)
            if s1.end < s2.end:
                i += 1
            else:
                j += 1
        return result

    def union(self, other: 'Interval') -> 'Interval':
        return other.union_union(self)

    def union_segment(self, other: 'Segment') -> 'Interval':
        return Union.from_intervals(self.segments + [other])

    def union_union(self, other: 'Union') -> 'Interval':
        return Union.from_intervals(self.segments + other.segments)

    @classmethod
    def from_intervals(cls, *intervals) -> 'Interval':
        segments = []
        for i in intervals:
            if i.is_empty():
                continue
            elif isinstance(i, Union):
                segments.extend(i.segments)
            elif isinstance(i, Segment):
                segments.append(i)

        segments = merge(list(sorted(segments, key=lambda x: (x.start, x.end))))
        if not segments:
            return Empty()
        elif len(segments) == 1:
            return segments[0]
        else:
            return Union(segments)


def merge(segments: t.List[Segment]):
    if len(segments) < 2:
        return segments
    else:
        first, second = segments[:2]
        if first.end >= second.start:
            return merge([(first.start, second.end)] + segments[2:])
        else:
            return [first] + merge(segments[1:])


class Map:

    def __init__(self, parts: t.List[t.Tuple[int, int, int]]):
        self.parts = parts

    def translate(self, interval: Interval) -> Interval:
        translated = Empty()
        remaining = interval
        for source_start, dest_start, n in self.parts:
            source = Segment.from_start_n(source_start, n)
            intersection = remaining.intersect(source)
            if intersection.is_empty():
                continue
            else:
                translated = translated.union(intersection.shift(dest_start-source_start))
                remaining = remaining.difference(intersection)
        return translated.union(remaining)


def solution(seeds: Union, maps: t.List[Map]):
    current = seeds
    for map in maps:
        current = map.translate(current)
    return current.leftmost()


def parse(f):
    seeds = []
    maps = []
    map_parts = []
    for i, line in enumerate(f):
        line = line.strip()
        if i == 0:
            xs = [int(x) for x in line.split(':')[1].split()]
            for start, n in zip(xs[::2], xs[1::2]):
                seeds.append(Segment.from_start_n(start, n))
        elif not line:
            maps.append(Map(map_parts))
            map_parts = []
        elif line[0] in string.ascii_lowercase:
            continue
        else:
            map_parts.append(tuple([int(x) for x in line.split()]))
    return Union(seeds), maps


def main():
    seeds, maps = parse(fileinput.input())
    print(solution(seeds, maps))


if __name__ == '__main__':
    main()
