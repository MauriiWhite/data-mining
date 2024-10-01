import time


from functools import wraps
from colorama import Fore, Style


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(
            f"{Fore.GREEN}Completed {Style.BRIGHT}'{func.__name__}': {Fore.MAGENTA}{elapsed_time:.2f}s{Style.RESET_ALL}"
        )
        return result

    return wrapper
