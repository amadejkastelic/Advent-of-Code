import typing
import random
from dataclasses import dataclass


@dataclass
class Node:
    name: str
    children: typing.List['Node']
    parent: typing.Optional['Node'] = None
    size: typing.Optional[int] = None
    is_dir: bool = True

    def add_child(self, child: 'Node'):
        child.parent = self
        self.children.append(child)

    def get_size(self) -> int:
        if self.size is not None:
            return self.size

        self.size = sum([child.get_size() for child in self.children])
        return self.size

    def get_child(self, name: str) -> typing.Optional['Node']:
        for child in self.children:
            if child.name == name:
                return child

    def __hash__(self) -> int:
        return hash(self.name + str(self.size) + str(random.randint(1, 1000000)))


def parse_commands(commands: typing.List[str]) -> Node:
    root = Node(name='/', children=[], parent=None)
    current = root
    for command in commands:
        if command.startswith('$ cd'):
            name = command.strip().split(' ')[2]
            if name == '/':
                current = root
                continue
            if name == '..':
                current = current.parent
                continue
            change = current.get_child(name=name)
            if change is not None:
                current = change
                continue
            new = Node(name=name, children=[], parent=current)
            current.add_child(current)
            current = new
        elif command.startswith('$ ls'):
            continue
        else:
            size, name = command.strip().split(' ')
            if size == 'dir':
                current.add_child(Node(name=name, children=[], parent=current))
            else:
                current.add_child(
                    Node(
                        name=name,
                        size=int(size),
                        parent=current,
                        children=None,
                        is_dir=False,
                    )
                )
    return root


def traverse(node: Node):
    for child in node.children:
        if child.children:
            for x in traverse(child):
                yield x
        yield child


with open('2022/day7/input.txt') as file:
    commands = file.readlines()

root = parse_commands(commands=commands)

sizes = dict()
for node in traverse(node=root):
    size = node.get_size()
    if node.is_dir and node.get_size() <= 100000:
        sizes[node] = node.get_size()

print(f'Part 1: {sum(sizes.values())}')

total = 70000000
needed_for_update = 30000000
used = root.get_size()
unused = total - used
needed = needed_for_update - unused

to_delete = min(
    [
        node.size
        for node in traverse(node=root)
        if node.get_size() >= needed and node.is_dir
    ]
)
print(f'Part 2: {to_delete}')
