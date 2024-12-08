import os
import time
import shutil
import typing
from contextlib import contextmanager

import bs4

import requests


BASE_AOC_URL = 'https://adventofcode.com/{year}/day/{day}'


@contextmanager
def timed(name: str):
    start = time.time()
    yield
    print(f"Time taken for {name}: {round((time.time() - start) * 1000, 2)}ms")


def fetch_input(year: int, day: int, token: typing.Optional[str] = None) -> None:
    path = os.path.join('inputs', str(year), f'day{day}')
    os.makedirs(path, exist_ok=True)

    if not token:
        token = input('Session token: ')

    base_url = BASE_AOC_URL.format(year=year, day=day)
    kwargs = {
        'cookies': {
            'session': token,
        },
    }

    with requests.get(base_url, **kwargs) as resp:
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        example = soup.find('code').get_text()

    with open(os.path.join(path, 'small.txt'), 'w') as f:
        f.write(example)

    with (
        requests.get(
            f'{base_url}/input',
            **kwargs,
        ) as resp,
        open(os.path.join(path, 'input.txt'), 'w') as f,
    ):
        f.write(resp.text)


def init(year: int, day: int) -> None:
    path = os.path.join(str(year), f'day{day}')
    path = f'{year}/day{day}'
    os.makedirs(path, exist_ok=True)
    shutil.copy2(src='examples/template.py', dst=os.path.join(path, 'solver.py'))
