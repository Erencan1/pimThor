import random


def randomSet(left, right, length):
    if length > abs(right - left):
        return set(_ for _ in range(left, right + 1))

    the_set = set()
    length = min(length, abs(right - left) + 1)
    while len(the_set) < length:
        the_set.add(random.randint(left, right))
    return the_set
