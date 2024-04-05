class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.w_in = 0
        self.w_out = 0

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"