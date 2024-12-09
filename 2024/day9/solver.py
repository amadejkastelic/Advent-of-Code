import typing
from collections import defaultdict

import solver


class DiskMap:
    def __init__(self, disk_map: typing.List[int]) -> None:
        self.layout = []
        self.free_space = 0
        self.free_spaces = defaultdict(lambda: [])
        self.blocks = defaultdict(lambda: [])
        idx = 0
        block_id = 0
        for i, num in enumerate(disk_map):
            if i % 2 == 0:
                self.blocks[block_id] = [idx] * num
                self.layout += [idx] * num
                idx += 1
                block_id += 1
            elif num != 0:
                self.layout += [-1] * num
                self.free_spaces[block_id] = [-1] * num
                self.free_space += num
                block_id += 1
        self.trimmed = list(self.layout)

    def is_trimmed(self) -> bool:
        return all(block == -1 for block in self.trimmed[-1 : -self.free_space - 1 : -1])

    def trim(self) -> None:
        i = 0
        j = len(self.trimmed) - 1
        while not self.is_trimmed():
            if j <= i:
                i = 0
                j = len(self.trimmed) - 1
                continue

            if self.trimmed[i] != -1:
                i += 1
                continue
            if self.trimmed[j] == -1:
                j -= 1
                continue

            self.trimmed[i], self.trimmed[j] = self.trimmed[j], self.trimmed[i]

    def trim_2(self) -> None:
        for j in sorted(self.free_spaces.keys()):
            for i in sorted(self.blocks.keys(), reverse=True):
                if len(self.blocks[i]) <= len(self.free_spaces[j]):
                    diff = len(self.free_spaces[j]) - len(self.blocks[i])
                    self.blocks[j] += list(self.blocks[i])
                    self.free_spaces[j] = [-1] * (diff)
                    self.free_spaces[i] = [-1] * len(self.blocks[i])
                    del self.blocks[i]

        # Combine free spaces with blocks
        for i, free_block in self.free_spaces.items():
            if not free_block:
                continue
            if i not in self.blocks:
                self.blocks[i] = free_block
            else:
                self.blocks[float(f'{i}.{i}')] = free_block

    @property
    def checksum(self) -> int:
        if not self.is_trimmed():
            self.trim()

        return sum([i * num for i, num in enumerate(self.trimmed[: -self.free_space])])

    @property
    def checksum_2(self) -> int:
        self.trim_2()

        res = 0
        idx = 0
        for bkey in sorted(self.blocks.keys()):
            for num in self.blocks[bkey]:
                if num != -1:
                    res += idx * num
                idx += 1

        return res


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.disk_map = DiskMap(list(map(int, list(f.read().strip()))))

    def _solve_part1(self) -> int:
        return 0
        return self.disk_map.checksum

    def _solve_part2(self) -> int:
        return self.disk_map.checksum_2
