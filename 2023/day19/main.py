import copy
import typing
from functools import reduce


VAR_TO_POS = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3,
}


class Rating(object):
    def __init__(self, ratings: typing.Dict[str, int]) -> None:
        for name, rating in ratings.items():
            self.__setattr__(name, int(rating))

    @property
    def rating(self) -> int:
        return sum([value for value in self.__dict__.values()])


class Rule(object):
    def __init__(self, id: str, rules: str) -> None:
        self.id = id
        self.rules: typing.List[typing.Tuple[typing.Optional[str], str]] = []
        for rule in rules.strip('{}').split(','):
            if ':' in rule:
                expr, res = rule.split(':')
            else:
                expr, res = None, rule
            self.rules.append((expr, res))

    def evaluate(self, rating: Rating) -> typing.Optional[str]:
        for expr, res in self.rules:
            if not expr:
                return res
            if eval(f'rating.{expr}'):
                return res

        return None


def evaluate_range(rules: typing.Dict[str, Rule], rule: str, ranges: typing.Tuple[typing.Tuple[int, int]]) -> int:
    if rule == 'A':
        return reduce(lambda x, y: x * y, [(j - i) + 1 for i, j in ranges])
    elif rule == 'R':
        return 0

    result = 0
    new_ranges = copy.deepcopy(ranges)
    for expr, res in rules[rule].rules:
        if not expr:
            result += evaluate_range(rules=rules, rule=res, ranges=new_ranges)
        else:
            op = expr[1]
            var, val = expr.split(op)
            val = int(val)
            curr_range = new_ranges[VAR_TO_POS[var]]

            if val >= curr_range[0] and val <= curr_range[1]:
                if op == '>':
                    result += evaluate_range(
                        rules=rules,
                        rule=res,
                        ranges=[new_ranges[i] if i != VAR_TO_POS[var] else (val + 1, curr_range[1]) for i in range(4)],
                    )
                    new_ranges = [new_ranges[i] if i != VAR_TO_POS[var] else (curr_range[0], val) for i in range(4)]
                elif op == '<':
                    result += evaluate_range(
                        rules=rules,
                        rule=res,
                        ranges=[new_ranges[i] if i != VAR_TO_POS[var] else (curr_range[0], val - 1) for i in range(4)],
                    )
                    new_ranges = [new_ranges[i] if i != VAR_TO_POS[var] else (val, curr_range[1]) for i in range(4)]

    return result


if __name__ == '__main__':
    with open('2023/day19/input.txt', 'r') as input_file:
        workflow, ratings = input_file.read().split('\n\n')

    rules: typing.Dict[str, Rule] = {}
    for line in workflow.split('\n'):
        _id, rule = line.split('{')
        rules[_id] = Rule(id=_id, rules=rule)

    part_ratings: typing.List[Rating] = []
    for line in ratings.split('\n'):
        part_ratings.append(Rating(ratings=eval(line.replace('{', '{"').replace('=', '":').replace(',', ',"'))))

    result = 0
    for rating in part_ratings:
        res = rules['in'].evaluate(rating=rating)
        while res not in ('A', 'R'):
            res = rules[res].evaluate(rating=rating)
        if res == 'A':
            result += rating.rating
    print(f'Part 1: {result}')

    ranges = ((1, 4000), (1, 4000), (1, 4000), (1, 4000))

    result = evaluate_range(rules=rules, rule='in', ranges=ranges)
    print(f'Part 2: {result}')
