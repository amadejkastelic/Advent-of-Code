import typing


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.readlines()

    incomplete_lines = []
    result = 0
    for line in content:
        syntax_result, needs_closing = _validate_syntax(line=line.strip())
        if syntax_result == 0:
            needs_closing.reverse()
            incomplete_lines.append((syntax_result, needs_closing))
        else:
            result += syntax_result
    print(f'Part 1: {result}')

    scores = []
    for line, need_closing in incomplete_lines:
        score = 0
        for char in need_closing:
            score *= 5
            score += _get_points_2(_get_matching(char))
        scores.append(score)
    print(f'Part 2: {sorted(scores)[int((len(scores) ) / 2)]}')


def _validate_syntax(line: str) -> typing.Tuple[int, typing.Optional[typing.List[str]]]:
    need_closing = []
    for char in line:
        if _is_opening(char):
            need_closing.append(char)
        elif _is_closing(char):
            if len(need_closing) == 0 or need_closing[-1] != _get_matching(char):
                return _get_points(char), []
            elif need_closing[-1] == _get_matching(char):
                need_closing.pop()
    return 0, need_closing


def _is_opening(char: str) -> bool:
    return char in ['(', '[', '{', '<']


def _is_closing(char: str) -> bool:
    return char in [')', ']', '}', '>']


def _get_matching(char: str) -> str:
    match char:
        case ')':
            return '('
        case ']':
            return '['
        case '}':
            return '{'
        case '>':
            return '<'
        case '(':
            return ')'
        case '[':
            return ']'
        case '{':
            return '}'
        case '<':
            return '>'


def _get_points(char: str) -> int:
    match char:
        case ')':
            return 3
        case ']':
            return 57
        case '}':
            return 1197
        case '>':
            return 25137


def _get_points_2(char: str) -> int:
    match char:
        case ')':
            return 1
        case ']':
            return 2
        case '}':
            return 3
        case '>':
            return 4


if __name__ == '__main__':
    main()
