import time
from opt import Node, FQueue, h, g, valid_neighbors, add_close
from maze import maze
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--width", help="window width", default=7, type=int)
parser.add_argument("-he", "--height", help="window height", default=5, type=int)
parser.add_argument("-u", "--unit", help="window unit", default=50, type=int)
parser.add_argument("-hw", "--h_weight", help="weight for h function", default=2, type=float)

args = parser.parse_args()


def loop(q: FQueue) -> Node:
    while True:
        time.sleep(0.1)
        n = q.get()
        add_close(n)

        if maze.is_end_node(n):
            found = n
            break
        neighbors = valid_neighbors(n, q, maze)
        for n_ in neighbors:
            if n_.pre != n:
                new_path_g = g(n, n_)
                if n_.g > new_path_g:
                    n_.pre = n
                    n_.g = new_path_g
            f = h(n_, maze.e_node, weight=args.h_weight) + n_.g
            q.put(f, n_)
            maze.add_f(f, n_)
    return found


def main(event=None):
    q = FQueue()
    q.put(0, maze.s_node)
    n = loop(q)
    maze.backward(n)


maze.build(args.width, args.height, args.unit)
maze.bind('<space>', main)
maze.mainloop()
