import typing


INT_TO_DIRECTION = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U',
}


def shoelace(positions: typing.List[typing.Tuple[int, int]]) -> int:
    return int(
        abs(
            sum(
                [
                    (positions[i + 1][0] - positions[i][0]) * (positions[i + 1][1] + positions[i][1])
                    for i in range(len(positions) - 1)
                ]
            )
            / 2
        )
    )


if __name__ == '__main__':
    with open('2023/day18/input.txt', 'r') as input_file:
        plan: typing.List[str] = input_file.read().split('\n')

    pos = (0, 0)
    positions = [pos]
    lens = []
    for line in plan:
        direction, meters, _ = line.split()
        lens.append(int(meters))
        match direction:
            case 'R':
                pos = (pos[0] + int(meters), pos[1])
            case 'L':
                pos = (pos[0] - int(meters), pos[1])
            case 'D':
                pos = (pos[0], pos[1] + int(meters))
            case 'U':
                pos = (pos[0], pos[1] - int(meters))
        positions.append(pos)

    print(f'Part 1: {int(shoelace(positions=positions) + (sum(lens) / 2) + 1)}')

    pos = (0, 0)
    positions = [pos]
    lens = []
    for line in plan:
        _, _, val = line.split()
        val = val.strip('()')
        direction = INT_TO_DIRECTION[int(val[-1])]
        meters = int(val[1:-1], 16)
        lens.append(int(meters))
        match direction:
            case 'R':
                pos = (pos[0] + int(meters), pos[1])
            case 'L':
                pos = (pos[0] - int(meters), pos[1])
            case 'D':
                pos = (pos[0], pos[1] + int(meters))
            case 'U':
                pos = (pos[0], pos[1] - int(meters))
        positions.append(pos)

    print(f'Part 2: {int(shoelace(positions=positions) + (sum(lens) / 2) + 1)}')
