import typing


def _visible_on_y_axis(y: int, x: int, trees: typing.List[typing.List[int]]) -> bool:
    return all([trees[i][x] < trees[y][x] for i in range(y)]) or all(
        [trees[i][x] < trees[y][x] for i in range(y + 1, len(trees))]
    )


def _visible_on_x_axis(y: int, x: int, trees: typing.List[typing.List[int]]) -> bool:
    return all([trees[y][j] < trees[y][x] for j in range(x)]) or all(
        [trees[y][j] < trees[y][x] for j in range(x + 1, len(trees[y]))]
    )


def is_visible(y: int, x: int, trees: typing.List[typing.List[int]]) -> bool:
    return _visible_on_y_axis(y=y, x=x, trees=trees) or _visible_on_x_axis(
        y=y, x=x, trees=trees
    )


def scenic_score(y: int, x: int, trees: typing.List[typing.List[int]]) -> int:
    up = 0
    for i in range(y - 1, -1, -1):
        up += 1
        if trees[i][x] >= trees[y][x]:
            break

    down = 0
    for i in range(y + 1, len(trees)):
        down += 1
        if trees[i][x] >= trees[y][x]:
            break

    left = 0
    for i in range(x - 1, -1, -1):
        left += 1
        if trees[y][i] >= trees[y][x]:
            break

    right = 0
    for i in range(x + 1, len(trees[y])):
        right += 1
        if trees[y][i] >= trees[y][x]:
            break

    return up * down * left * right


with open('2022/day8/input.txt') as file:
    lines = file.readlines()
trees = [list(map(int, list(tree.strip()))) for tree in lines]

visible = 0
for i in range(len(trees)):
    for j in range(len(trees[i])):
        if i == 0 or j == 0 or i == len(trees) - 1 or j == len(trees[i]) - 1:
            visible += 1
        elif is_visible(y=i, x=j, trees=trees):
            visible += 1

print(f'Part 1: {visible}')

result = 0
for i in range(len(trees)):
    for j in range(len(trees[i])):
        score = scenic_score(y=i, x=j, trees=trees)
        if score > result:
            result = score

print(f'Part 2: {result}')
