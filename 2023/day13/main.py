import enum
import typing


class ReflectionType(enum.Enum):
    VERTICAL = 0
    HORIZONTAL = 1


class Pattern(object):
    def __init__(self, pattern: typing.List[str]) -> None:
        self.pattern = pattern

        possible_reflections = self._find_reflection_idx()
        for reflection in possible_reflections:
            is_ok = True
            if reflection[0] == ReflectionType.HORIZONTAL:
                for i in range(1, min(reflection[1][0] + 1, len(self.pattern) - reflection[1][1])):
                    if pattern[reflection[1][0] - i] != pattern[reflection[1][1] + i]:
                        is_ok = False
                        break
            elif reflection[0] == ReflectionType.VERTICAL:
                for i in range(1, min(reflection[1][0] + 1, len(self.pattern[0]) - reflection[1][1])):
                    if not all(
                        pattern[j][reflection[1][0] - i] == pattern[j][reflection[1][1] + i]
                        for j in range(len(pattern))
                    ):
                        is_ok = False
                        break
            if is_ok:
                self.indexes = reflection[1]
                self.reflection_type = reflection[0]
                break

    def _find_reflection_idx(self) -> typing.List[typing.Tuple[ReflectionType, typing.Tuple[int, int]]]:
        res = []
        for i in range(len(self.pattern) - 1):
            if self.pattern[i] == self.pattern[i + 1]:
                res.append((ReflectionType.HORIZONTAL, (i, i + 1)))

        for i in range(len(self.pattern[0]) - 1):
            if all(self.pattern[j][i] == self.pattern[j][i + 1] for j in range(len(self.pattern))):
                res.append((ReflectionType.VERTICAL, (i, i + 1)))

        return res


if __name__ == '__main__':
    patterns: typing.List[Pattern] = []
    with open('2023/day13/input.txt', 'r') as input_file:
        raw_patterns = input_file.read().split('\n\n')
        for i, pattern in enumerate(raw_patterns):
            patterns.append(Pattern(pattern=pattern.split()))

    result = 0
    for pattern in patterns:
        if pattern.reflection_type == ReflectionType.VERTICAL:
            result += pattern.indexes[1]
        else:
            result += pattern.indexes[1] * 100
    print(f'Part 1: {result}')
