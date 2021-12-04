import numpy as np


def _main():
    file_name = input("Enter input path: ")

    numbers = np.loadtxt(file_name, max_rows=1, delimiter=",").astype(complex)
    cards = np.loadtxt(file_name, skiprows=2).reshape((100, 5, 5)).astype(complex)

    print(_get_final_score(numbers=numbers, cards=cards))
    print(_get_final_score(numbers=numbers, cards=cards, simple=False))


def _get_final_score(numbers, cards, simple=True):
    score = 0
    for number in numbers:
        for card in cards:
            for i in range(5):
                for j in range(5):
                    if card[i, j] == number:
                        card[i, j] = 0 + 1j
                        if sum(card[i, :]) == (0 + 5j):
                            score = int((np.sum(card) * number).real)
                            if simple:
                                return score
                            card[:, :] = -1.0 + 0j
                        elif sum(card[:, j]) == (0 + 5j):
                            score = int((np.sum(card) * number).real)
                            if simple:
                                return score
                            card[:, :] = -1.0 + 0j
    return score


if __name__ == '__main__':
    _main()
