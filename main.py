import argparse
import importlib
import sys

import solver


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, help="Year of the puzzle")
    parser.add_argument("--day", type=int, help="Day of the puzzle")
    parser.add_argument("--part", type=int, help="Part of the puzzle", default=None, nargs="?")
    parser.add_argument("--input", type=str, help="Input file path", default=None, nargs="?")

    args = parser.parse_args()
    year = args.year
    day = args.day
    part = args.part
    inp = args.input or f"{year}/day{day}/input.txt"

    try:
        s: solver.Solver = importlib.import_module(f"{year}.day{day}.solver").Solver(inp)
        s.solve(part)
    except ImportError:
        print("Invalid year or day")
        sys.exit(1)
