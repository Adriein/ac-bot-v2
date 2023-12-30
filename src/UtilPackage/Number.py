import random


class Number:
    @staticmethod
    def random(min_int: int, max_int: int) -> int:
        return random.randint(min_int, max_int)
