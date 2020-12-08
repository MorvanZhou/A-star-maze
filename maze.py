import tkinter as tk
from opt import Node


class Maze(tk.Tk):
    s_node_num = 1
    e_node_num = 2
    wall_node_num = -1

    def __init__(self):
        super().__init__()
        self.title("A*")
        self.canvas = None
        self.map = None
        self.unit = None
        self.w, self.h = 0, 0
        self.n_click = 0
        self.s_node = None
        self.e_node = None
        self.bind("<Button-1>", self.modify_map)
        self.text_dict = {}

    def build(self, w, h, unit=20):
        self.w, self.h, self.unit = w, h, unit
        self.geometry('%dx%d' % (w * unit, h * unit))
        self.canvas = tk.Canvas(self, height=h * unit, width=w * unit, relief='sunken', bg='white')
        for i in range(w):
            for j in range(h):
                x1, y1 = i * unit, j * unit
                x2, y2 = x1 + unit, y1 + unit
                coord = (x1, y1, x2, y2)
                self.canvas.create_rectangle(coord)
        self.canvas.pack()
        self.map = [[0 for _ in range(h)] for _ in range(w)]

    def modify_map(self, event=None):
        x, y = event.x // self.unit, event.y // self.unit
        if self.n_click == 0:
            self.map[x][y] = self.s_node_num
            c = "yellow"
            self.s_node = Node(x, y)
        elif self.n_click == 1:
            self.map[x][y] = self.e_node_num
            c = "red"
            self.e_node = Node(x, y)
        else:
            self.map[x][y] = self.wall_node_num
            c = "black"
        self.n_click += 1
        coord = (x * self.unit, y * self.unit, (x + 1) * self.unit, (y + 1) * self.unit)
        self.canvas.create_rectangle(coord, fill=c)
        self.canvas.update()

    def has_pos(self, x, y):
        if (x < 0 or y < 0) or (x > self.w - 1 or y > self.h - 1):
            return False
        return True

    def ok_move_to(self, x, y):
        if self.map[x][y] in [self.s_node_num, self.wall_node_num]:
            return False
        return True

    def backward(self, n: Node):
        while True:
            n = n.pre
            if n.x == self.s_node.x and n.y == self.s_node.y:
                break
            coord = (n.x * self.unit, n.y * self.unit, (n.x + 1) * self.unit, (n.y + 1) * self.unit)
            self.canvas.create_rectangle(coord, fill="blue")
            self.canvas.update()

    def is_end_node(self, node):
        if node.x == self.e_node.x and node.y == self.e_node.y:
            return True
        return False

    def add_f(self, f, node):
        t = self.canvas.create_text(
            self.unit * node.x + self.unit / 2, self.unit * node.y + self.unit / 2, fill="black",
            font="Times %d" % (8 / 30 * self.unit),
            text="%.1f" % f)
        if node.id in self.text_dict:
            self.canvas.delete(self.text_dict[node.id])
        self.text_dict[node.id] = t
        self.canvas.update()

maze = Maze()