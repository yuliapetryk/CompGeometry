from matplotlib import pyplot as plt
from sortedcontainers import SortedList
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Event = namedtuple('Event', ['point', 'type', 'segment'])


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        if p1.x < p2.x or (p1.x == p2.x and p1.y < p2.y):
            self.start, self.end = p1, p2
        else:
            self.start, self.end = p2, p1

    def __lt__(self, other):
        return (self.start.x, self.start.y, self.end.x, self.end.y) < (
            other.start.x, other.start.y, other.end.x, other.end.y)


def intersect(segment1, segment2):
    def orientation(left, point, right):
        return (point.y - left.y) * (right.x - point.x) - (point.x - left.x) * (right.y - point.y)

    def on_segment(left, point, right):
        return min(left.x, right.x) <= point.x <= max(left.x, right.x) and min(left.y, right.y) <= point.y <= max(left.y, right.y)

    o1 = orientation(segment1.start, segment1.end, segment2.start)
    o2 = orientation(segment1.start, segment1.end, segment2.end)
    o3 = orientation(segment2.start, segment2.end, segment1.start)
    o4 = orientation(segment2.start, segment2.end, segment1.end)

    if o1 != o2 and o3 != o4:
        denominator = (segment1.start.x - segment1.end.x) * (segment2.start.y - segment2.end.y) - (segment1.start.y - segment1.end.y) * (segment2.start.x - segment2.end.x)
        num1 = (segment1.start.x * segment1.end.y - segment1.start.y * segment1.end.x)
        num2 = (segment2.start.x * segment2.end.y - segment2.start.y * segment2.end.x)
        x = (num1 * (segment2.start.x - segment2.end.x) - (segment1.start.x - segment1.end.x) * num2) / denominator
        y = (num1 * (segment2.start.y - segment2.end.y) - (segment1.start.y - segment1.end.y) * num2) / denominator
        intersection_point = Point(x, y)
        if on_segment(segment1.start, intersection_point, segment1.end) and on_segment(segment2.start, intersection_point, segment2.end):
            return intersection_point

    if o1 == 0 and on_segment(segment1.start, segment2.start, segment1.end):
        return segment2.start
    if o2 == 0 and on_segment(segment1.start, segment2.end, segment1.end):
        return segment2.end
    if o3 == 0 and on_segment(segment2.start, segment1.start, segment2.end):
        return segment1.start
    if o4 == 0 and on_segment(segment2.start, segment1.end, segment2.end):
        return segment1.end

    return None


def find_intersections(segments):
    events = []

    for segment in segments:
        events.append(Event(segment.start, 'start', segment))
        events.append(Event(segment.end, 'end', segment))

    events.sort(key=lambda e: (e.point.x, e.point.y))

    active_segments = SortedList()
    intersections = []

    def add_intersection(segment1, segment2):
        point = intersect(segment1, segment2)
        if point:
            intersections.append((point, segment1, segment2))

    for event in events:
        if event.type == 'start':
            idx = active_segments.bisect_left(event.segment)
            active_segments.add(event.segment)
            if idx > 0:
                add_intersection(active_segments[idx - 1], event.segment)
            if idx < len(active_segments) - 1:
                add_intersection(active_segments[idx], active_segments[idx + 1])
        elif event.type == 'end':
            idx = active_segments.index(event.segment)
            if 0 < idx < len(active_segments) - 1:
                add_intersection(active_segments[idx - 1], active_segments[idx + 1])
            active_segments.remove(event.segment)

    return intersections


def plot_segments_and_intersections(segments, intersections):
    plt.figure(figsize=(10, 10))

    for segment in segments:
        plt.plot([segment.p1.x, segment.p2.x], [segment.p1.y, segment.p2.y], 'b')

    for point, segment1, segment2 in intersections:
        plt.plot(point.x, point.y, 'ro')

    plt.grid(True)
    plt.show()


segments = [
    Segment(Point(2, 5), Point(6, 7)),
    Segment(Point(1, 4), Point(8, 1)),
    Segment(Point(0, 2), Point(16, 7)),
    Segment(Point(13, 8), Point(10, 2)),
    Segment(Point(5, 1), Point(12, 5))
]

intersections = find_intersections(segments)

for point, segment1, segment2 in intersections:
    print(f"{segment1.p1, segment1.p2} and {segment2.p1, segment2.p2} intersect at  {point}")

plot_segments_and_intersections(segments, intersections)
