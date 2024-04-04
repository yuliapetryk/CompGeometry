from edge import Edge
from point import Point


def read_vertices(file_name: str) -> list:
    points = []
    with open(file_name, 'r') as file:
        for line in file:
            x_str, y_str = line.strip().split()
            x = int(x_str)
            y = int(y_str)
            points.append(Point(x, y))
    return points


def read_edges(file_name: str, points: list) -> list:
    edges = []
    with open(file_name, 'r') as file:
        for line in file:
            start_index_str, end_index_str = line.strip().split()
            start_index = int(start_index_str)
            end_index = int(end_index_str)
            start_point = points[start_index]
            end_point = points[end_index]
            edges.append(Edge(start_point, end_point, 1))
    return edges
