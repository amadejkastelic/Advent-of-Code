import enum
import typing


class ReflectionType(enum.Enum):
    VERTICAL = 0
    HORIZONTAL = 1


class Pattern(object):
    def __init__(self, pattern: typing.List[str]) -> None:
        self.pattern = pattern

        possible_reflections = self._find_reflection_idx()
        for reflection_type, indexes, smudge in possible_reflections:
            is_ok = True
            if reflection_type == ReflectionType.HORIZONTAL:
                for i in range(1, min(indexes[0] + 1, len(self.pattern) - indexes[1])):
                    matches, smudge = self._matches_horizontally(
                        y1=indexes[0] - i, y2=indexes[1] + i, smudge=smudge
                    )
                    if not matches:
                        is_ok = False
                        break
            elif reflection_type == ReflectionType.VERTICAL:
                for i in range(1, min(indexes[0] + 1, len(self.pattern[0]) - indexes[1])):
                    matches, smudge = self._matches_vertically(x1=indexes[0] - i, x2=indexes[1] + i, smudge=smudge)
                    if not matches:
                        is_ok = False
                        break
            if is_ok:
                self.indexes = indexes
                self.reflection_type = reflection_type
                break

        if not hasattr(self, 'reflection_type'):
            for line in pattern:
                print(line)
            raise Exception('No reflection found')

    def _find_reflection_idx(self) -> typing.List[typing.Tuple[ReflectionType, typing.Tuple[int, int], bool]]:
        res = []
        for i in range(len(self.pattern) - 1):
            matches, smudge = self._matches_horizontally(y1=i, y2=i + 1, smudge=True)
            if matches:
                res.append((ReflectionType.HORIZONTAL, (i, i + 1), smudge))

        for i in range(len(self.pattern[0]) - 1):
            matches, smudge = self._matches_vertically(x1=i, x2=i + 1, smudge=True)
            if matches:
                res.append((ReflectionType.VERTICAL, (i, i + 1), smudge))

        return res

    def _matches_horizontally(self, y1: int, y2: int, smudge: bool = True) -> typing.Tuple[bool, bool]:
        fully_matches = self.pattern[y1] == self.pattern[y2]
        if fully_matches:
            return True, smudge

        if not smudge:
            return False, False

        if 1 == [
            self.pattern[y1][j] == self.pattern[y2][j] for j in range(len(self.pattern[0]))
        ].count(False):
            return True, False

        return False, True

    def _matches_vertically(self, x1: int, x2: int, smudge: bool = True) -> typing.Tuple[bool, bool]:
        fully_matches = all(self.pattern[j][x1] == self.pattern[j][x2] for j in range(len(self.pattern)))
        if fully_matches:
            return True, smudge

        if not smudge:
            return False, False

        if 1 == [
            self.pattern[j][x1] == self.pattern[j][x2] for j in range(len(self.pattern))
        ].count(False):
            return True, False

        return False, True


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
