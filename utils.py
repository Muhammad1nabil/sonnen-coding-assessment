def fibonacci_generator():
    """
    Create a generator for fabonacci series which will be produced lazily, one at a time
    and wont return all at once 
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
