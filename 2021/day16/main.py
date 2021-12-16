import typing
from functools import reduce
from operator import mul


def main():
    file_name = input("Enter input path: ")

    with open(file_name, "r") as f:
        content = f.read().strip()

    binary = ""
    for number in content:
        binary += str(bin(int(number, 16))).lstrip("-0b").zfill(4)

    result = [0]
    _, res = _parse(binary=binary, result=result)
    print(f"Part 1: {result[0]}")
    print(f"Part 2: {res}")


def _parse(binary: str, result: typing.List[int]) -> typing.Tuple[str, int]:
    version = int(binary[:3], 2)
    result[0] += version
    binary = binary[3:]

    _id = int(binary[:3], 2)
    binary = binary[3:]

    if _id == 4:
        number = ""
        for i in range(0, len(binary), 5):
            number += binary[i + 1 : i + 5]
            if binary[i] == "0":
                return binary[i + 5 :], int(number, 2)
    else:
        length_type_id = binary[0]
        binary = binary[1:]
        results = []
        if length_type_id == "1":
            length = int(binary[:11], 2)
            binary = binary[11:]
            for _ in range(length):
                binary, num = _parse(binary=binary, result=result)
                results.append(num)

            print(_id, end=" - ")
            print(results, end=" - ")
            print(_calc_result(results=results, _id=_id))
            return binary, _calc_result(results=results, _id=_id)
        else:
            length = int(binary[:15], 2)
            binary = binary[15:]
            x, y = binary[:length], binary[length:]
            while x:
                x, num = _parse(binary=x, result=result)
                results.append(num)

            print(_id, end=" - ")
            print(results, end=" - ")
            print(_calc_result(results=results, _id=_id))
            return y, _calc_result(results=results, _id=_id)


def _calc_result(results: typing.List[int], _id: int) -> int:
    if _id == 0:
        return sum(results)
    elif _id == 1:
        return reduce(mul, results)
    elif _id == 2:
        return min(results)
    elif _id == 3:
        return max(results)
    elif _id == 5:
        if results[0] > results[1]:
            return 1
    elif _id == 6:
        if results[0] < results[1]:
            return 1
    elif _id == 7:
        if results[0] == results[1]:
            return 1
    return 0


if __name__ == "__main__":
    main()
