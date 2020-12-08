CLOSE_DICT = {}


class Node:
    def __init__(self, x, y, pre=None):
        self.x = x
        self.y = y
        self.pre = pre
        self.g = 0 if pre is None else g(pre, self)

    def __str__(self):
        return "[%d,%d] %.2f" % (self.x, self.y, self.g)

    @property
    def id(self):
        return "%d_%d" % (self.x, self.y)


class FQueue:
    def __init__(self):
        self.small2large = []
        self.items_dict = {}

    def replace(self, score, item):
        # remove
        del self.items_dict[item.id]
        for i, score_item in enumerate(self.small2large):
            _, _item_id = score_item
            if _item_id == item.id:
                self.small2large.pop(i)
                break

        self.put(score, item)

    def put(self, score, item: Node):
        if item.id in self.items_dict:
            self.replace(score, item)
            return
        if len(self.small2large) == 0:
            self.small2large.append((score, item.id))
            self.items_dict[item.id] = item
            return

        # insert with priority
        self.items_dict[item.id] = item
        inserted = False
        for i, score_item in enumerate(self.small2large):
            _score, _item = score_item
            if score < _score:
                self.small2large.insert(i, (score, item.id))
                inserted = True
                break
        if not inserted:
            self.small2large.append((score, item.id))

    def get(self):
        assert len(self.small2large) > 0, ValueError("cannot get from an empty queue")
        _, item_id = self.small2large.pop(0)
        item = self.items_dict[item_id]
        del self.items_dict[item_id]
        return item


# heuristic function, global guidance
def h(n: Node, e: Node, distance="euclidean", weight=1):
    distance = distance.lower()
    if distance == "euclidean":
        d = ((e.x - n.x)**2 + (e.y - n.y)**2)**0.5
    elif distance == "taxicab":
        d = abs(e.x - n.x) + abs(e.y - n.y)
    elif distance == "dijkstra":
        d = 0
    else:
        raise ValueError("{} is not a supported distance".format(distance))
    return d * weight


# cost of the path
def g(n: Node, n_: Node):
    dx, dy = n_.x - n.x, n_.y - n.y
    if abs(dx) == 1 and abs(dy) == 1:
        # to diagonal
        cost = 1.4
    else:
        # to up, down, left, right = 1
        cost = 1
    return cost + n.g


def valid_neighbors(n: Node, q: FQueue, maze):
    valid_ns = []
    for dx in [1, -1, 0]:
        for dy in [0, 1, -1]:
            x, y = n.x+dx, n.y+dy
            if not maze.has_pos(x, y) or (dx == dy == 0):
                continue
            new_id = "%d_%d" % (x, y)
            if maze.ok_move_to(x, y) and new_id not in CLOSE_DICT:
                if new_id in q.items_dict:
                    n_ = q.items_dict[new_id]
                else:
                    n_ = Node(x, y, pre=n)
                valid_ns.append(n_)
    return valid_ns

def add_close(node):
    CLOSE_DICT[node.id] = node
