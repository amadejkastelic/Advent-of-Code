def remove_empty(var):
    if not var:
        return False

    return True


with open('2022/day1/input.txt') as file:
    calories = file.read()

calories = calories.split('\n\n')
calories = [sum(map(int, filter(remove_empty, c.split('\n')))) for c in calories]

print('Part 1: ' + str(max(calories)))

print(
    'Part 2: '
    + str(
        calories.pop(calories.index(max(calories)))
        + calories.pop(calories.index(max(calories)))
        + calories.pop(calories.index(max(calories)))
    )
)
