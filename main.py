import argparse
import dataclasses
import datetime
import importlib
import os
import shutil
import sys
import typing

import solver


@dataclasses.dataclass
class Config:
    year: int
    day: int
    part: typing.Optional[int] = None
    input_file: typing.Optional[str] = None
    init: bool = False

    @classmethod
    def from_arguments(cls) -> 'Config':
        today = datetime.date.today()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--year',
            type=int,
            help='Year of the puzzle',
            default=today.year,
        )
        parser.add_argument(
            '--day',
            type=int,
            help='Day of the puzzle',
            default=today.day,
        )
        parser.add_argument(
            '--part',
            type=typing.Optional[int],
            help='Part of the puzzle',
            default=None,
        )
        parser.add_argument(
            '--input',
            type=str,
            help='Input file name',
            default='input.txt',
        )
        parser.add_argument(
            '--init',
            help='Prepare stuff',
            default=False,
            action='store_true',
        )
        args = parser.parse_args()

        return cls(
            year=args.year,
            day=args.day,
            part=args.part,
            input_file=f'inputs/{args.year}/day{args.day}/{args.input}',
            init=args.init,
        )


def init(year: int, day: int) -> None:
    path = os.path.join(str(year), f'day{day}')
    path = f'{year}/day{day}'
    os.makedirs(path, exist_ok=True)
    shutil.copy2(src='examples/template.py', dst=os.path.join(path, 'solver.py'))


if __name__ == '__main__':
    config = Config.from_arguments()

    if config.init:
        init(year=config.year, day=config.day)
        sys.exit(0)

    try:
        s: solver.Solver = importlib.import_module(
            f'{config.year}.day{config.day}.solver',
        ).Solver(config.input_file)
    except ImportError:
        print('Invalid year or day')
        sys.exit(1)

    s.solve(config.part)
