
import matplotlib.pyplot as plt
from sortedcontainers import SortedList

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y

class ConvexHullNode:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None
        self.parent = None
        self.left_most_right = self

class ConvexHullBST:
    def __init__(self):
        self.root = None

    def insert(self, point):
        new_node = ConvexHullNode(point)
        if self.root is None:
            self.root = new_node
            return

        left_neighbour, right_neighbour = self._find_neighbours(self.root, point)

        if left_neighbour is None and right_neighbour is None:
            self.root = new_node
            return

        if left_neighbour:
            if left_neighbour.right is None:
                left_neighbour.right = new_node
            else:
                left_neighbour.right.parent = new_node
                new_node.left = left_neighbour.right
                left_neighbour.right = new_node
            new_node.parent = left_neighbour
        if right_neighbour:
            if right_neighbour.left is None:
                right_neighbour.left = new_node
            else:
                right_neighbour.left.parent = new_node
                new_node.right = right_neighbour.left
                right_neighbour.left = new_node
            new_node.parent = right_neighbour

        self._update_hull(new_node)

    def delete(self, point):
        node = self._find(self.root, point)
        if not node:
            return

        if node.left and node.right:
            successor = self._find_min(node.right)
            node.point = successor.point
            self._delete_node(successor)
        else:
            self._delete_node(node)

    def _delete_node(self, node):
        if not node.left and not node.right:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = None
                else:
                    node.parent.right = None
            else:
                self.root = None
        elif node.left and not node.right:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = node.left
                else:
                    node.parent.right = node.left
            else:
                self.root = node.left
            node.left.parent = node.parent
        elif not node.left and node.right:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right
            else:
                self.root = node.right
            node.right.parent = node.parent

        if node.parent:
            self._update_hull(node.parent)

    def _find(self, node, point):
        if not node or not node.point:
            return None
        if node.point == point:
            return node
        if point < node.point:
            return self._find(node.left, point)
        return self._find(node.right, point)

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def _find_neighbours(self, node, point, left=None, right=None):
        if not node:
            return left, right

        if point < node.point:
            return self._find_neighbours(node.left, point, left, node)
        return self._find_neighbours(node.right, point, node, right)

    def _update_hull(self, node):
        if not node:
            return

        if node.left:
            node.left_most_right = node.left.left_most_right
        if node.right:
            node.left_most_right = node.right.left_most_right

        self._update_hull(node.parent)

    def get_hull_points(self):
        return self._collect_points(self.root)

    def _collect_points(self, node):
        if not node or not node.point:
            return []
        return self._collect_points(node.left) + [node.point] + self._collect_points(node.right)

class DynamicConvexHull:
    def __init__(self):
        self.points = SortedList()
        self.upper_hull = ConvexHullBST()
        self.lower_hull = ConvexHullBST()

    def add_point(self, point):
        self.points.add(point)
        self.update_hulls()
        self.visualize("Add", point)

    def remove_point(self, point):
        self.points.remove(point)
        self.update_hulls()
        self.visualize("Remove", point)

    def update_hulls(self):
        self.upper_hull = ConvexHullBST()
        self.lower_hull = ConvexHullBST()

        for point in self.points:
            while len(self.upper_hull.get_hull_points()) >= 2 and self.orientation(self.upper_hull.get_hull_points()[-2], self.upper_hull.get_hull_points()[-1], point) != 1:
                self.upper_hull.delete(self.upper_hull.get_hull_points()[-1])
            self.upper_hull.insert(point)

        for point in self.points:
            while len(self.lower_hull.get_hull_points()) >= 2 and self.orientation(self.lower_hull.get_hull_points()[-2], self.lower_hull.get_hull_points()[-1], point) != 2:
                self.lower_hull.delete(self.lower_hull.get_hull_points()[-1])
            self.lower_hull.insert(point)

    def orientation(self, p, q, r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def visualize(self, action, point):
        points = list(self.points)
        x_vals = [p.x for p in points]
        y_vals = [p.y for p in points]

        plt.figure()
        plt.scatter(x_vals, y_vals, color='blue')
        plt.title(f'{action} Point ({point.x}, {point.y})')
        plt.xlabel('X')
        plt.ylabel('Y')

        upper_hull_points = self.upper_hull.get_hull_points()
        lower_hull_points = self.lower_hull.get_hull_points()

        if len(upper_hull_points) > 1:
            upper_hull_x = [p.x for p in upper_hull_points]
            upper_hull_y = [p.y for p in upper_hull_points]
            plt.plot(upper_hull_x, upper_hull_y, color='red')

        if len(lower_hull_points) > 1:
            lower_hull_x = [p.x for p in lower_hull_points]
            lower_hull_y = [p.y for p in lower_hull_points]
            plt.plot(lower_hull_x, lower_hull_y, color='green')

        plt.show()

dynamicConvexHull = DynamicConvexHull()
points = [Point(1, 2),
          Point(3, 4),
          Point(8, 1),
          Point(7, 2),
          Point(11, 4),
          Point(9, 4),
          Point(5, 5),
          Point(2, 2)]

dch = DynamicConvexHull()
for point in points:
    dch.add_point(point)

dch.remove_point(Point(11, 4))
