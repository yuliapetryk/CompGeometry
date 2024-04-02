import math
import matplotlib.pyplot as plt

from point import Point


def find_point(vertices, edges, point):
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


def create_chains(vertices, edges_out):
    chains = [[] for _ in range(calculate_weight(edges_out[0]))]
    ordered_edges_out = [sort(v) for v in edges_out]

    for j in range(len(chains)):
        create_chain(j, ordered_edges_out, chains, vertices)

    print_chains(vertices, chains)

    return chains


def print_chains(vertices, chains):
    for i, chain in enumerate(chains):
        print(f"Chain {i}: {vertices.index(chain[0].start)}", end="")
        for edge in chain:
            print(f" {vertices.index(edge.end)}", end="")
        print()


def create_chain(chain_num, ordered_edges_out, chains, vertices):
    current_vertex_index = 0
    num_vertices = len(vertices)

    while current_vertex_index != num_vertices - 1:
        new_edge = get_next_edge(ordered_edges_out[current_vertex_index])
        chains[chain_num].append(new_edge)
        new_edge.weight -= 1
        current_vertex_index = vertices.index(new_edge.end)


def get_next_edge(array):
    for edge in array:
        if edge.weight > 0:
            return edge
    return None


def locate_point(point, chains):
    for p, chain in enumerate(chains):
        for edge in chain:
            if edge.start.y <= point.y <= edge.end.y:
                point_vector = Point(point.x - edge.start.x, point.y - edge.start.y)
                edge_vector = Point(edge.end.x - edge.start.x, edge.end.y - edge.start.y)
                if math.atan2(point_vector.y, point_vector.x) >= math.atan2(edge_vector.y, edge_vector.x):
                    print(f"Point is between chains {p - 1} , {p}")
                    return p-1


def show_graph(point, vertices, edges, chains, chain):

    plt.scatter(point.x, point.y, color='red')

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

