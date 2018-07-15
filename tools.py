import time
from functools import wraps


def disabled(d):
    """Disable decorator."""
    return lambda f: f


def trace(f):
    """Decorator that traces function calls and returns."""
    indent = '   '
    trace.level = 0
    @wraps(f)
    def wrapper(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print('%s--> %s' % (trace.level*indent, signature))
        trace.level += 1
        try:
            result = f(*args)
            print('%s<-- %s == %s' % ((trace.level-1)*indent, signature, result))
        finally:
            trace.level -= 1
        return result
    return wrapper


def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    f.cache = {}
    @wraps(f)
    def wrapper(*args):
        try:
            return f.cache[args]
        except KeyError:
            f.cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return wrapper


callcounts = {}

def countcalls(f):
    """Decorator that makes the function count calls to it, in callcounts[f]."""
    @wraps(f)
    def wrapper(*args):
        callcounts[wrapper] += 1
        return f(*args)
    callcounts[wrapper] = 0
    return wrapper


def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    @wraps(f)
    def wrapper(x, *args):
        return x if not args else f(x, wrapper(*args))
    return wrapper


def timedcall(fn, *args):
    """Call a function with args; return the time in seconds and result."""
    t0 = time.clock()
    res = fn(*args)
    t1 = time.clock()
    return t1-t0, res


def self_reference(f):
    """Pass f to itself. f must have 'self' as first argument."""
    @wraps(f)
    def wrapper(*args, **kwds):
        return f(f, *args, **kwds)
    return wrapper
