import chain_method
import read_data
from point import Point

file_edges = 'edges.txt'
file_vertices = 'vertices.txt'

# Read data
initial_vertices = read_data.read_vertices(file_vertices)
edges = read_data.read_edges(file_edges, initial_vertices)

# point = Point(13, 13)
# point = Point(12, 14)
point = Point(10, 13)

# Sort vertices from bottom to top by y
vertices = sorted(initial_vertices, key=lambda p: p.y)

# Locate the point
chain_method.find_point(vertices, edges, point)
