from collections import defaultdict, deque
import typing

import solver


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            rules, updates = f.read().strip().split('\n\n')
            self.rules: typing.Dict[int, typing.List[int]] = {}
            for rule in rules.split():
                a, b = tuple(map(int, rule.split('|')))
                if a not in self.rules:
                    self.rules[a] = [b]
                else:
                    self.rules[a].append(b)
            self.updates: typing.List[typing.List[int]] = [
                list(map(int, line.split(','))) for line in updates.split('\n')
            ]

    def _is_sorted(self, update: typing.List[int]) -> bool:
        for i, num in enumerate(update):
            if num in self.rules:
                for c in self.rules[num]:
                    if c in update[:i]:
                        return False
        return True

    def _sort(self, update: typing.List[int]) -> typing.List[int]:
        graph: typing.Dict[int, typing.List[int]] = defaultdict(list)
        in_degree: typing.Dict[int, int] = {num: 0 for num in update}

        for num in update:
            if num in self.rules:
                for dependent in self.rules[num]:
                    if dependent in in_degree:
                        graph[num].append(dependent)
                        in_degree[dependent] += 1

        queue: deque[int] = deque([node for node in update if in_degree[node] == 0])
        sorted_order: typing.List[int] = []

        while queue:
            node = queue.popleft()
            sorted_order.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        unused_nodes = [num for num in update if num not in sorted_order]
        return sorted_order + unused_nodes

    def _solve_part1(self) -> int:
        return sum([update[len(update) // 2] if self._is_sorted(update) else 0 for update in self.updates])

    def _solve_part2(self) -> int:
        return sum(
            [self._sort(update)[len(update) // 2] if not self._is_sorted(update) else 0 for update in self.updates]
        )
