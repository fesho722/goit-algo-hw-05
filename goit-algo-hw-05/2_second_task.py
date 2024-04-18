import re
from typing import Callable


def generator_numbers(text: str):
    pattern = r'[-+]?\d*\.\d+|\d+'
    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable):
    gen = func(text)
    total_sum = sum(gen)
    return total_sum
