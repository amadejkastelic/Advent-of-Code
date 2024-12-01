import time
from contextlib import contextmanager


@contextmanager
def timed(name: str):
    start = time.time()
    yield
    print(f"Time taken for {name}: {round((time.time() - start) * 1000, 2)}ms")
