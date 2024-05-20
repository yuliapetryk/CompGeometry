import heapq

from matplotlib import pyplot as plt
from sortedcontainers import SortedList


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Segment:
    def __init__(self, start, end):
        if start > end:
            start, end = end, start
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Segment({self.start}, {self.end})"


class Event:
    def __init__(self, event_type, point, segment1, segment2=None):
        self.event_type = event_type
        self.point = point
        self.segment1 = segment1
        self.segment2 = segment2

    def __lt__(self, other):
        return self.point < other.point

    def __repr__(self):
        return f"Event({self.event_type}, {self.point}, {self.segment1}, {self.segment2})"


def find_intersections(segments):
    event_queue = []
    sweep_line = SortedList(key=lambda seg: (seg.start.y, seg.end.y))
    intersections = set()

    for segment in segments:
        heapq.heappush(event_queue, Event('left', segment.start, segment))
        heapq.heappush(event_queue, Event('right', segment.end, segment))

    while event_queue:
        event = heapq.heappop(event_queue)
        if event.event_type == 'left':
            handle_left_event(event, sweep_line, event_queue)
        elif event.event_type == 'right':
            handle_right_event(event, sweep_line, event_queue)
        elif event.event_type == 'intersection':
            handle_intersection_event(event, sweep_line, event_queue, intersections)

    return list(intersections)


def handle_left_event(event, sweep_line, event_queue):
    segE = event.segment1
    sweep_line.add(segE)

    idx = sweep_line.index(segE)
    segA = sweep_line[idx + 1] if idx + 1 < len(sweep_line) else None
    segB = sweep_line[idx - 1] if idx - 1 >= 0 else None

    check_and_add_intersection(segE, segA, event_queue)
    check_and_add_intersection(segE, segB, event_queue)


def handle_right_event(event, sweep_line, event_queue):
    segE = event.segment1
    idx = sweep_line.index(segE)
    segA = sweep_line[idx + 1] if idx + 1 < len(sweep_line) else None
    segB = sweep_line[idx - 1] if idx - 1 >= 0 else None

    sweep_line.remove(segE)

    if segA and segB:
        check_and_add_intersection(segA, segB, event_queue)


def handle_intersection_event(event, sweep_line, event_queue, intersections):
    intersection_info = (event.point, event.segment1, event.segment2)
    if intersection_info not in intersections:
        intersections.add(intersection_info)

    segE1 = event.segment1
    segE2 = event.segment2

    idx1 = sweep_line.index(segE1)
    idx2 = sweep_line.index(segE2)

    sweep_line.remove(segE1)
    sweep_line.remove(segE2)

    sweep_line.add(segE2)
    sweep_line.add(segE1)

    idx1, idx2 = sorted([idx1, idx2])
    segA = sweep_line[idx2 + 1] if idx2 + 1 < len(sweep_line) else None
    segB = sweep_line[idx1 - 1] if idx1 - 1 >= 0 else None

    check_and_add_intersection(segE1, segA, event_queue)
    check_and_add_intersection(segE2, segB, event_queue)


def check_and_add_intersection(seg1, seg2, event_queue):
    if not seg1 or not seg2:
        return
    intersection_point = find_intersection(seg1, seg2)
    if intersection_point:
        heapq.heappush(event_queue, Event('intersection', intersection_point, seg1, seg2))


def find_intersection(segment1, segment2):

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


def plot_segments_and_intersections(segments, intersections):
    plt.figure(figsize=(10, 10))

    for segment in segments:
        plt.plot([segment.start.x, segment.end.x], [segment.start.y, segment.end.y], 'b')

    for intersection in intersections:
        point, seg1, seg2 = intersection
        plt.plot(point.x, point.y, 'ro')

    plt.grid(True)
    plt.show()


segments = [
    Segment(Point(2, 5), Point(6, 7)),
    Segment(Point(1, 4), Point(8, 1)),
    Segment(Point(0, 2), Point(16, 7)),
    Segment(Point(13, 8), Point(10, 2)),
    Segment(Point(5, 4), Point(15, 4))
]

intersections = find_intersections(segments)

for intersection in intersections:
    point, seg1, seg2 = intersection
    print(f"Intersection at: {point} between {seg1} and {seg2}")

plot_segments_and_intersections(segments,intersections)