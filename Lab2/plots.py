import networkx as nx
from matplotlib import pyplot as plt


def show_points(points: list, x: list, y: list, result: list):
    x_values = [point.x for point in points]
    y_values = [point.y for point in points]

    plt.scatter(x_values, y_values, color='blue')
    for point in result:
        plt.scatter(point.x, point.y, color='red')

    x1, x2 = x
    y1, y2 = y

    plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color='red')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()


def add_nodes_edges(G, node, depth=0, pos=None):
    if node:
        if pos is None:
            pos = {node.point: (0, 0)}
        if node.left:
            G.add_node(node.left.point)
            G.add_edge(node.point, node.left.point)
            pos[node.left.point] = (pos[node.point][0] - 0.5 / (2 ** depth), pos[node.point][1] - 1)  # Вниз та ліворуч
            add_nodes_edges(G, node.left, depth + 1, pos)
        if node.right:
            G.add_node(node.right.point)
            G.add_edge(node.point, node.right.point)
            pos[node.right.point] = (
            pos[node.point][0] + 0.5 / (2 ** depth), pos[node.point][1] - 1)  # Вниз та праворуч
            add_nodes_edges(G, node.right, depth + 1, pos)
    return pos


def draw_tree(tree):
    G = nx.Graph()
    pos = add_nodes_edges(G, tree)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold",
            arrows=True)
    plt.show()
