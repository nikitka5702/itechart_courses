class FibIterator:
    def __init__(self):
        self.a, self.b, self._c = 0, 1, 0

    def __iter__(self):
        while True:
            yield self.a
            self._c += 1
            self.a, self.b = self.b, self.a + self.b
            if self._c >= 100:
                break


def fib_generator():
    a, b, _c = 0, 1, 0
    while _c < 100:
        yield a
        _c += 1
        a, b = b, a + b


def strange_decorator(func):
    def wrapper(*args, **kwargs):
        if len(args + tuple(kwargs.values())) > 10:
            raise ValueError
        if any(isinstance(x, bool) for x in kwargs.values()):
            raise TypeError
        r = func(*args, **kwargs)
        if isinstance(r, int) and not isinstance(r, bool):
            r += 13
        return r
    return wrapper
