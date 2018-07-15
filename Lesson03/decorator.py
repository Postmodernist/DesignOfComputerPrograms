from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        f0 = d(fn)
        f1 = update_wrapper(d(fn), fn)
        return update_wrapper(f1, f0, tuple())
    return _d

def disabled(d):
    "Disable decorator."
    return lambda f: f

