import math
import matplotlib.pyplot as plt

from point import Point


def find_point(vertices, edges, point):
    #if is_regularized_graph:
       # print("The chain method cannot be used")
       # return
    if check_vertex(point, vertices) or check_edge(point, edges):
        return

    in_edges = [[] for _ in vertices]
    out_edges = [[] for _ in vertices]

    adjust_edge_weights(vertices, edges, in_edges, out_edges)
    chains = create_chains(vertices, out_edges)
    chain = locate_point(point, chains)
    show_graph(point, vertices, edges, chains, chain)


def adjust_edge_weights(vertices, edges, in_edges, out_edges):
    assign_edges_to_vertices(vertices, edges, in_edges, out_edges)

    balance_bottom_up(vertices, in_edges, out_edges)

    balance_top_down(vertices, in_edges, out_edges)

    for edge in edges:
        print(f"Edge from {edge.start} to {edge.end} has weight: {edge.weight}")


def assign_edges_to_vertices(vertices, edges, in_edges, out_edges):
    for edge in edges:
        start_point = vertices.index(edge.start)
        end_point = vertices.index(edge.end)
        out_edges[start_point].append(edge)
        in_edges[end_point].append(edge)


def balance_bottom_up(vertices, in_edges, out_edges):
    n = len(vertices)
    for i in range(1, n - 1):
        in_weight = calculate_weight(in_edges[i])
        out_weight = calculate_weight(out_edges[i])
        out_edges[i] = sort(out_edges[i])
        if in_weight > out_weight:
            out_edges[i][0].weight = in_weight - out_weight + 1


def balance_top_down(vertices, in_edges, out_edges):
    n = len(vertices)
    for i in range(n - 1, 1, -1):
        in_weight = calculate_weight(in_edges[i])
        out_weight = calculate_weight(out_edges[i])
        in_edges[i] = sort(in_edges[i])
        if out_weight > in_weight:
            in_edges[i][0].weight = out_weight - in_weight + in_edges[i][0].weight


def calculate_weight(edges):
    return sum(edge.weight for edge in edges)


def sort(edges):
    return sorted(edges, key=lambda edge: edge.rotation, reverse=True)


def print_chains(vertices, chains):
    for i, chain in enumerate(chains):
        print(f"Chain {i}: {vertices.index(chain[0].start)}", end="")
        for edge in chain:
            print(f" {vertices.index(edge.end)}", end="")
        print()


def create_chains(vertices, edges_out):
    chains = [[] for _ in range(calculate_weight(edges_out[0]))]
    ordered_edges_out = [sort(v) for v in edges_out]

    for j in range(len(chains)):
        current_vertex_index = 0
        num_vertices = len(vertices)

        while current_vertex_index != num_vertices - 1:
            for edge in ordered_edges_out[current_vertex_index]:
                if edge.weight > 0:
                    chains[j].append(edge)
                    edge.weight -= 1
                    current_vertex_index = vertices.index(edge.end)
                    break
            else:
                break

    print_chains(vertices, chains)

    return chains


def locate_point(point, chains):
    for p, chain in enumerate(chains):
        for edge in chain:
            if edge.start.y <= point.y <= edge.end.y:
                point_vector = Point(point.x - edge.start.x, point.y - edge.start.y)
                edge_vector = Point(edge.end.x - edge.start.x, edge.end.y - edge.start.y)
                if math.atan2(point_vector.y, point_vector.x) >= math.atan2(edge_vector.y, edge_vector.x):
                    print(f"Point ({point.x}, {point.y}) is between chains {p - 1}, {p}")
                    return p - 1


def check_vertex(point: Point, vertices: list) -> bool:
    for vertex in vertices:
        if point.x == vertex.x and point.y == vertex.y:
            print(f"Point ({point.x}, {point.y}) is vertex")
            return True
    return False


def check_edge(point: Point, edges: list):
    for edge in edges:
        edge_end = edge.end
        edge_start = edge.start
        start_to_point = Point(point.x - edge_start.x, point.y - edge_start.y)
        start_to_end = Point(edge_end.x - edge_start.x, edge_end.y - edge_start.y)
        cross_product = start_to_point.x * start_to_end.y - start_to_point.y * start_to_end.x

        if abs(cross_product) < 1e-9 and min(edge_start.x, edge_end.x) <= point.x <= max(edge_start.x, edge_end.x) \
                and min(edge_start.y, edge_end.y) <= point.y <= max(edge_start.y, edge_end.y):
            print(
                f"Point ({point.x}, {point.y}) is on edge ({edge.start.x}, {edge.start.y}), ({edge.end.x}, {edge.end.y})")
            return True
    return False


def show_graph(point, vertices, edges, chains, chain):
    plt.scatter(point.x, point.y, color='green')

    for vertex in vertices:
        plt.scatter(vertex.x, vertex.y, color='black')
        plt.text(vertex.x, vertex.y, f'{vertex}', fontsize=12, ha='right')

    for edge in edges:
        start = edge.start
        end = edge.end
        plt.plot([start.x, end.x], [start.y, end.y], 'b-')

    show_chain(chains, chain)
    show_chain(chains, chain + 1)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


def show_chain(chains, number):
    for i in range(len(chains[number])):
        start = chains[number][i].start
        end = chains[number][i].end

        plt.plot([start.x, end.x],
                 [start.y, end.y],
                 'red')


def is_regularized_graph(vertices: list, edges: list) -> bool:
    degree_count = {}
    for vertex in vertices:
        degree_count[vertex] = 0

    for edge in edges:
        degree_count[edge.start] += 1
        degree_count[edge.end] += 1

    first_degree = degree_count[vertices[0]]
    for degree in degree_count.values():
        if degree != first_degree:
            return True
    return False
