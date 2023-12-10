import sys
import typing

sys.setrecursionlimit(10000000)


class Node(object):
    def __init__(
        self,
        symbol: str,
        y: int,
        x: int,
        parent: typing.Optional['Node'] = None,
        children: typing.Optional[typing.List['Node']] = None,
        depth: typing.Optional[int] = None,
    ):
        self.children = children or []
        self.x = x
        self.y = y
        self.symbol = symbol
        self.parent = parent
        self.depth = depth

    def add_node(self, node: 'Node') -> None:
        if not self.parent == node:
            node.depth = self.depth + 1
            self.children.append(node)

    def __str__(self) -> str:
        return f'\'{self.symbol}\' ({self.x}, {self.y})'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: 'Node') -> bool:
        return isinstance(other, Node) and self.x == other.x and self.y == other.y and self.symbol == other.symbol

    def __hash__(self) -> str:
        return hash(str(self))

    def connects_to(self, other: 'Node') -> bool:
        match self.symbol:
            case '|':
                return self.x == other.x and (self.y - 1 == other.y or self.y + 1 == other.y)
            case '-':
                return self.y == other.y and (self.x - 1 == other.x or self.x + 1 == other.x)
            case 'L':
                return (self.x == other.x and self.y - 1 == other.y) or (self.y == other.y and self.x + 1 == other.x)
            case 'J':
                return (self.x == other.x and self.y - 1 == other.y) or (self.y == other.y and self.x - 1 == other.x)
            case '7':
                return (self.x == other.x and self.y + 1 == other.y) or (self.y == other.y and self.x - 1 == other.x)
            case 'F':
                return (self.x == other.x and self.y + 1 == other.y) or (self.y == other.y and self.x + 1 == other.x)
        return False


def find_start(field: typing.List[str]) -> Node:
    for i, line in enumerate(field):
        start = line.find('S')
        if start >= 0:
            return Node(symbol='S', y=i, x=start, depth=0)
    return -1, -1


def at_index(y: int, x: int, field: typing.List[str], parent: typing.Optional[Node] = None) -> Node:
    try:
        return Node(symbol=field[y][x], y=y, x=x, parent=parent)
    except IndexError:
        return '.'


def get_children(node: Node, field: typing.List[str]) -> bool:
    match node.symbol:
        case '|':
            node.add_node(at_index(y=node.y - 1, x=node.x, field=field, parent=node))
            node.add_node(at_index(y=node.y + 1, x=node.x, field=field, parent=node))
            return True
        case '-':
            node.add_node(at_index(y=node.y, x=node.x - 1, field=field, parent=node))
            node.add_node(at_index(y=node.y, x=node.x + 1, field=field, parent=node))
            return True
        case 'L':
            node.add_node(at_index(y=node.y - 1, x=node.x, field=field, parent=node))
            node.add_node(at_index(y=node.y, x=node.x + 1, field=field, parent=node))
            return True
        case 'J':
            node.add_node(at_index(y=node.y - 1, x=node.x, field=field, parent=node))
            node.add_node(at_index(y=node.y, x=node.x - 1, field=field, parent=node))
            return True
        case '7':
            node.add_node(at_index(y=node.y + 1, x=node.x, field=field, parent=node))
            node.add_node(at_index(y=node.y, x=node.x - 1, field=field, parent=node))
            return True
        case 'F':
            node.add_node(at_index(y=node.y + 1, x=node.x, field=field, parent=node))
            node.add_node(at_index(y=node.y, x=node.x + 1, field=field, parent=node))
            return True

    return False


def build_tree(node: Node, field: typing.List[str]):
    if node.children or get_children(node=node, field=field):
        for child in node.children:
            build_tree(node=child, field=field)


def dfs(node: Node, visited: typing.Set[typing.Tuple[int, int]]) -> int:
    visited.add((node.y, node.x))

    if not node.children:
        return node.depth

    return max([dfs(node=child, visited=visited) for child in node.children])


if __name__ == '__main__':
    with open('2023/day10/input.txt', 'r') as input_file:
        field = [line.strip() for line in input_file]

    root = find_start(field=field)
    for i in range(-1, 2, 2):
        lr = at_index(y=root.y, x=root.x + i, field=field)
        ud = at_index(y=root.y + i, x=root.x + i, field=field)
        if lr.symbol != '.' and lr.connects_to(root):
            root.add_node(lr)
        if ud.symbol != '.' and lr.connects_to(root):
            root.add_node(ud)

    build_tree(node=root, field=field)
    visited = set()
    print(f'Part 1: {dfs(node=root, visited=visited) // 2}')

    field = [list(line) for line in field]
    w = at_index(y=root.y, x=root.x - 1, field=field)
    e = at_index(y=root.y, x=root.x + 1, field=field)
    s = at_index(y=root.y - 1, x=root.x, field=field)
    n = at_index(y=root.y + 1, x=root.x, field=field)
    if s.symbol != '.' and n.symbol != '.':
        field[root.y][root.x] = '|'
    elif e.symbol != '.' and w.symbol != '.':
        field[root.y][root.x] = '-'
    elif n.symbol != '.' and e.symbol != '.':
        field[root.y][root.x] = 'L'
    elif n.symbol != '.' and w.symbol != '.':
        field[root.y][root.x] = 'J'
    elif s.symbol != '.' and w.symbol != '.':
        field[root.y][root.x] = '7'
    elif s.symbol != '.' and e.symbol != '.':
        field[root.y][root.x] = 'F'

    count = 0
    skip = ''
    for y in range(len(field)):
        inside = False
        for x in range(len(field[y])):
            if (y, x) in visited:
                if field[y][x] == 'F':
                    skip = '7'
                elif field[y][x] == 'L':
                    skip = 'J'
                elif field[y][x] == '-':
                    continue
                else:
                    if field[y][x] != skip:
                        inside = not inside
                    skip = ''
            elif inside:
                count += 1

    print(f'Part 2: {count}')
