

def fori(start, end, step):
    """
    the equivalent of an for-i-loop
    :param start:
    :param end:
    :param step:
    """
    while start <= end:
        yield start
        start += step
