import typing


def main():
    file_name = input("Enter input path: ")

    with open(file_name, 'r') as f:
        content = f.readlines()

    print(_count_appearances_1(display_codes=content))
    print(_count_appearances_2(display_codes=content))


def _count_appearances_1(display_codes: typing.List[str]) -> int:
    count = 0
    for line in display_codes:
        _, codes = line.split('|')
        for code in codes.split():
            if len(code) in [2, 3, 4, 7]:
                count += 1
    return count


def _count_appearances_2(display_codes: typing.List[str]) -> int:
    count = 0
    for line in display_codes:
        inputs, outputs = line.split('|')
        lengths = {len(signal): set(signal) for signal in inputs.split()}

        result = ''
        outputs = map(set, outputs.split())
        for output in outputs:
            match [len(output.intersection(lengths[mask])) for mask in [7, 2, 4]]:
                case 7, _, _: 
                    result += '8'
                case 4, _, _:
                    result += '4'
                case 3, _, _:
                    result += '7'
                case 2, _, _:
                    result += '1'
                case 5, 1, 2:
                    result += '2'
                case 5, 1, 3:
                    result += '5'
                case 5, 2, 3:
                    result += '3'
                case 6, 1, 3:
                    result += '6'
                case 6, 2, 3:
                    result += '0'
                case 6, 2, 4:
                    result += '9'
        count += int(result)
    return count


if __name__ == '__main__':
    main()
