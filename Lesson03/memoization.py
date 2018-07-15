from decorator import decorator

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f


@decorator
def countcalls(f):
    "Decorator that makes the function count calls to it, in callcounts[f]."
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

callcounts = {}


@countcalls
@memo
def fib(n): return 1 if n <= 1 else fib(n-1) + fib(n-2)

print("{:>3}{:>10}{:>10}{:>10}".format("n", "fib(n)", "calls", "ratio"))
calls_prev = 1
for i in range(1, 31):
    fib_i = fib(i)
    calls = callcounts[fib]
    print("{:3}{:10}{:10}{:10.4}".format(i, fib_i, calls, calls/calls_prev))
    calls_prev = calls
