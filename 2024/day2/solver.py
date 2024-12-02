import typing
from collections import defaultdict

import solver


class Solver(solver.Solver):
    def _init(self):
        self.reports: typing.List[typing.List[int]] = []
        with open(self.input_file_path) as f:
            for line in f:
                self.reports.append([int(x) for x in line.split()])

    @staticmethod
    def _is_report_increasing(report: typing.List[int]) -> bool:
        return sum([1 if report[i] < report[i + 1] else 0 for i in range(len(report) - 1)]) >= len(report) / 2

    @staticmethod
    def _is_report_safe(report: typing.List[int], allow_bad_level: bool = False) -> bool:
        increasing = Solver._is_report_increasing(report)
        hit = False
        for i in range(len(report) - 1):
            diff = abs(report[i] - report[i + 1])
            if (
                (diff == 0 or diff > 3)
                or (increasing and report[i] > report[i + 1])
                or (not increasing and report[i] < report[i + 1])
            ):
                if allow_bad_level and not hit:
                    if i == 0 and Solver._is_report_safe(report[1:]):
                        return True
                    elif Solver._is_report_safe(report[0:i] + report[i + 1 :]):
                        return True
                    hit = True
                    report[i + 1] = report[i]
                    continue

                return False
        return True

    def _solve_part1(self) -> int:
        return sum([1 if self._is_report_safe(report) else 0 for report in self.reports])

    def _solve_part2(self) -> int:
        return sum([1 if self._is_report_safe(report=report, allow_bad_level=True) else 0 for report in self.reports])
