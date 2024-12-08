import argparse
import dataclasses
import datetime
import importlib
import sys
import typing

import solver
import utils


@dataclasses.dataclass
class Config:
    year: int
    day: int
    part: typing.Optional[int] = None
    input_file: typing.Optional[str] = None
    init: bool = False
    fetch_input: bool = False
    session_token: typing.Optional[str] = None

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
        parser.add_argument(
            '--fetch-input',
            help='Fetch input from aoc',
            default=False,
            action='store_true',
        )
        parser.add_argument(
            '--session-token',
            type=typing.Optional[str],
            help='Session token for input fetching',
            default=None,
        )
        args = parser.parse_args()

        return cls(
            year=args.year,
            day=args.day,
            part=args.part,
            input_file=f'inputs/{args.year}/day{args.day}/{args.input}',
            init=args.init,
            fetch_input=args.fetch_input,
            session_token=args.session_token,
        )


if __name__ == '__main__':
    config = Config.from_arguments()

    if config.init:
        utils.init(year=config.year, day=config.day)
    if config.fetch_input:
        utils.fetch_input(year=config.year, day=config.day, token=config.session_token)

    if any([config.init, config.fetch_input]):
        sys.exit(0)

    try:
        s: solver.Solver = importlib.import_module(
            f'{config.year}.day{config.day}.solver',
        ).Solver(config.input_file)
    except ImportError:
        print('Invalid year or day')
        sys.exit(1)

    s.solve(config.part)
