import argparse
import dataclasses
import datetime
import importlib
import sys
import typing

import solver


@dataclasses.dataclass
class Config:
    year: int
    day: int
    part: typing.Optional[int] = None
    input_file: typing.Optional[str] = None

    @classmethod
    def from_arguments(cls) -> 'Config':
        today = datetime.date.today()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--year",
            type=int,
            help="Year of the puzzle",
            default=today.year,
        )
        parser.add_argument(
            "--day",
            type=int,
            help="Day of the puzzle",
            default=today.day,
        )
        parser.add_argument(
            "--part",
            type=typing.Optional[int],
            help="Part of the puzzle",
            default=None,
        )
        parser.add_argument(
            "--input",
            type=str,
            help="Input file name",
            default='input.txt',
        )
        args = parser.parse_args()

        return cls(
            year=args.year,
            day=args.day,
            part=args.part,
            input_file=f"{args.year}/day{args.day}/{args.input}",
        )


if __name__ == "__main__":
    config = Config.from_arguments()

    try:
        s: solver.Solver = importlib.import_module(
            f"{config.year}.day{config.day}.solver",
        ).Solver(config.input_file)
    except ImportError:
        print("Invalid year or day")
        sys.exit(1)

    s.solve(config.part)
