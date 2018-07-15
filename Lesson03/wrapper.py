from functools import update_wrapper

# Variant 1

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    return update_wrapper(_d, d)

# Variant 2

def decorator(d):
    return lambda fn: update_wrapper(d(fn), fn)

decorator = decorator(decorator)

# My version of Variant 1

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    return _d

# My version of Variant 1 adopted for Python 3

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        f0 = d(fn)
        f1 = update_wrapper(d(fn), fn)
        return update_wrapper(f1, f0, tuple())
    return _d


@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

## DECORATOR

@n_ary
def seq(x, y):
    "This is seq docstring"
    return ('seq', x, y)
