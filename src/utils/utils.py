import time
from functools import wraps


def timeit(func):
    """
    Decorator to measure and print the execution time of a function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result

    return wrapper
