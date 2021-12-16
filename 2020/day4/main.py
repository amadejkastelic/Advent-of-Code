import re
import typing


class Passport:
    def __init__(self, passport: str):
        self.data = {}
        passport = passport.replace('\n', ' ').strip()
        for param in passport.split():
            key, value = param.split(':')
            self.data[key] = value

    def is_valid_v1(self) -> bool:
        return (
            'byr' in self.data
            and 'iyr' in self.data
            and 'eyr' in self.data
            and 'hgt' in self.data
            and 'hcl' in self.data
            and 'ecl' in self.data
            and 'pid' in self.data
        )

    def is_valid_v2(self) -> bool:
        return (
            self._byr_valid()
            and self._iyr_valid()
            and self._hgt_valid()
            and self._hcl_valid()
            and self._ecl_valid()
            and self._pid_valid()
        )

    def _between(self, val: typing.Any, range: typing.Tuple[int, int]) -> bool:
        try:
            val = int(val)
        except Exception:
            return False

        return range[0] <= val >= range[1]

    def _byr_valid(self) -> bool:
        return self._between(val=self.data.get('byr'), range=(1920, 2002))

    def _iyr_valid(self) -> bool:
        return self._between(val=self.data.get('iyr'), range=(2010, 2020))

    def _eyr_valid(self) -> bool:
        return self._between(val=self.data.get('eyr'), range=(2020, 2030))

    def _hgt_valid(self) -> bool:
        hgt = self.data.get('hgt')

        if not hgt:
            return False

        if 'cm' in hgt:
            hgt = hgt.replace('cm', '')
            return self._between(val=hgt, range=(150, 193))
        elif 'in' in hgt:
            hgt = hgt.replace('in', '')
            return self._between(val=hgt, range=(59, 76))

        return False

    def _hcl_valid(self) -> bool:
        return re.match(r'^#[a-f0-9]{6}\$', self.data.get('hcl', ''))

    def _ecl_valid(self) -> bool:
        valid = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
        return self.data.get('ecl', '') in valid

    def _pid_valid(self) -> bool:
        return re.match(r'^[0-9]{9}\$', self.data.get('pid', ''))


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read()

    valid_v1, valid_v2 = 0, 0
    for passport_str in content.split('\n\n'):
        passport = Passport(passport=passport_str)
        if passport.is_valid_v1():
            valid_v1 += 1
        if passport.is_valid_v2():
            valid_v2 += 1
    print(f'Part 1: {valid_v1}')
    print(f'Part 2: {valid_v2}')


if __name__ == '__main__':
    main()
