def add_to_set(s, value):
    if value > 0:
        s.add(value)
    return s


def remove_negatives(s):
    return {x for x in s if x >= 0}


def sum_of_set(s):
    return sum(s)
