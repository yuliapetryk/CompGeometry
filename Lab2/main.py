import data

initial_points = data.read_points("points.txt")
points = sorted(initial_points, key=lambda p: p.x)

region = data.read_line("region.txt")

data.show_points(points, region)