from point import Point
import matplotlib.pyplot as plt

def read_points(file_name: str) -> list:
    points = []
    with open(file_name, 'r') as file:
        for line in file:
            x_str, y_str = line.strip().split()
            x = int(x_str)
            y = int(y_str)
            points.append(Point(x, y))
    return points

def read_line(file_name: str) -> list:
    with open(file_name, 'r') as file:
        line = file.readline()
        lines = line.split()
        lines = [int(num) for num in lines]
    return lines


def show_points(points: list, region: list):
    x_values = [point.x for point in points]
    y_values = [point.y for point in points]

    plt.scatter(x_values, y_values, color='blue')

    x1, y1, x2, y2 = region

    plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color='red')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()
