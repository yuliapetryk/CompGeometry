class Node:
    def __init__(self, point, dim):
        self.point = point
        self.left = None
        self.right = None
        self.dim = dim

    def __repr__(self):
        return "(" + str(self.point) + ", " + str(self.left) + "," + str(self.right)


def sort_point(points, axis=0):
    if axis == 0:
        sorted_points = sorted(points, key=lambda point: point.x)
    elif axis == 1:
        sorted_points = sorted(points, key=lambda point: point.y)
    return sorted_points


def find_middle_point(points):
    middle_point = (len(points) - 1) // 2
    return middle_point


def build_tree(points, depth=0):
    if len(points) == 0:
        return None

    axis = depth % 2
    # Сортуємо або по x або по y
    sorted_points = sort_point(points, axis)
    # Визначаємо медіану
    middle_index = find_middle_point(sorted_points)
    middle_point = sorted_points[middle_index]
    # Ділимо точки на два масиви
    left_points = sorted_points[:middle_index]
    right_points = sorted_points[middle_index + 1:]
    # Створюємо вузол
    node = Node(middle_point, axis)
    # Задаємо йому лівого і правого сина, які визначаємо рекурсивно викликаючи цю функцію ще раз але вже окремо для кожного з масивів
    node.left = build_tree(left_points, depth + 1)
    node.right = build_tree(right_points, depth + 1)

    return node


def check_point(point, x_range, y_range):
    return (x_range[0] < point.x < x_range[1]) and (y_range[0] < point.y < y_range[1])


def search_points(node, x_range, y_range, result):
    # Перевіряємо, чи точка було горизонтальною чи вертикальною медіаною
    if node.dim == 0:
        # Перевіряємо чи медіана лежить у прямокутнику і чи точка лежить
        if x_range[0] < node.point.x < x_range[1] and check_point(node.point, x_range, y_range):
            result.append(node.point)

    elif node.dim == 1:
        # Перевіряємо чи медіана лежить у прямокутнику і чи точка лежить
        if y_range[0] < node.point.y < y_range[1] and check_point(node.point, x_range, y_range):
            result.append(node.point)

    # Переходимо до синів
    if node.left:
        search_points(node.left, x_range, y_range, result)

    if node.right:
        search_points(node.right, x_range, y_range, result)

    return result
