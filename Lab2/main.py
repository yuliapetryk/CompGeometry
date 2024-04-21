import data
import range_tree
import plots as pl

points = data.read_points("points.txt")
x, y = data.read_range("region.txt")

tree = range_tree.build_tree(points)
pl.draw_tree(tree)

result = range_tree.search_points(tree, x, y, [])
if len(result) == 0:
    print("Усередині регіону точок немає")
else:
    print("Точки всередині регіону:", result)

pl.show_points(points, x, y, result)
