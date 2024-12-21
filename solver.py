import typing

import utils


class Solver:
    @utils.timed("init")
    def __init__(self, input_file_path: str, debug: bool = False):
        self.input_file_path = input_file_path
        self.debug = debug
        self._init()

    def _init(self):
        pass

    def solve(self, part: typing.Optional[int]) -> None:
        if not part:
            self._solve_one(1)
            self._solve_one(2)
        else:
            self._solve_one(part)

    def _solve_one(self, part: int) -> None:
        try:
            solve_func = getattr(self, f"_solve_part{part}")
        except AttributeError:
            raise ValueError("Invalid part")

        with utils.timed(f'Part {part}'):
            print(f'Part {part}: {solve_func()}')

    def _solve_part1(self) -> typing.Any:
        raise NotImplementedError()

    def _solve_part2(self) -> typing.Any:
        raise NotImplementedError()
