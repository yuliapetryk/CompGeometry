from point import Point


def read_points(file_name: str) -> list:
    points = []
    with open(file_name, 'r') as file:
        for line in file:
            x_str, y_str = line.strip().split()
            x = int(x_str)
            y = int(y_str)
            points.append(Point(x, y))
    return points


