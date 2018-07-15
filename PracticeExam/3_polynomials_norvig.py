from collections import defaultdict

def poly(coefs):
    """Return a function that is the polynomial with these coefficients.
    For example if coefs=(10, 20, 30) return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""
    return polynomial(canonical(coefs))

@memo
def polynomial(coefs):
    """Return a polynomial function with these attributes.  Memoized, so any
    two polys with the same coefficients will be identical polys."""
    # Build a function by evaluating a lambda in the empty environment.
    # Horner's rule involves fewer multiplications than the normal formula...
    p = eval('lambda x: ' + horner_formula(coefs), {})
    p.__name__ = polynomial_formula(coefs)
    p.coefs = coefs
    return p

def horner_formula(coefs):
    """A relatively efficient form to evaluate a polynomial.
    E.g.:  horner_formula((10, 20, 30, 0, -50)) 
           == '(10 + x * (20 + x * (30 + x * x * -50)))',
    which is 4 multiplies and 3 adds."""
    c = coefs[0]
    if len(coefs) == 1:
        return str(c)
    else:
        factor = 'x * ' + horner_formula(coefs[1:])
        return factor if c == 0 else '(%s + %s)' % (c, factor)

def polynomial_formula(coefs):
    """A simple human-readable form for a polynomial.
    E.g.:  polynomial_formula((10, 20, 30, 0, -50))
           == '-50 * x**4 + 30 * x**2 + 20 * x + 10',
    which is 7 multiplies and 3 adds."""
    terms = [term(c, n) 
             for (n, c) in reversed(list(enumerate(coefs))) if c != 0]
    return ' + '.join(terms)

def term(c, n):
    "Return a string representing 'c * x**n' in simplified form."
    if n == 0:
        return str(c)
    xn = 'x' if (n == 1) else ('x**' + str(n))
    return xn if (c == 1) else '-' + xn if (c == -1) else str(c) + ' * ' + xn

def canonical(coefs):
    "Canonicalize coefs by dropping trailing zeros and converting to a tuple."
    if not coefs: coefs = [0]
    elif isinstance(coefs, (int, float)): coefs = [coefs]
    else: coefs = list(coefs)
    while coefs[-1] == 0 and len(coefs) > 1:
        del coefs[-1]
    return tuple(coefs)

def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    return callable(x) and hasattr(x, 'coefs')

def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    N = max(len(p1.coefs), len(p2.coefs))
    coefs = [0] * N
    for (n, c) in enumerate(p1.coefs): coefs[n] = c
    for (n, c) in enumerate(p2.coefs): coefs[n] += c
    return poly(coefs)

def sub(p1, p2):
    "Return a new polynomial which is p1 - p2."
    N = max(len(p1.coefs), len(p2.coefs))
    coefs = [0] * N
    for (n, c) in enumerate(p1.coefs): coefs[n] = c
    for (n, c) in enumerate(p2.coefs): coefs[n] -= c
    return poly(coefs)

def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    # Given terms a*x**n and b*x**m, accumulate a*b in results[n+m]
    results = defaultdict(int)
    for (n, a) in enumerate(p1.coefs):
        for (m, b) in enumerate(p2.coefs):
            results[n + m] += a * b
    return poly([results[i] for i in range(max(results)+1)])

def power(p, n):
    "Return a poly which is p to the nth power (n a non-negative integer)."
    if n == 0:
        return poly((1,))
    elif n == 1:
        return p
    elif n % 2 == 0:
        return square(power(p, n//2))
    else:
        return mul(p, power(p, n-1))

def square(p): return mul(p, p)

def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    return poly([n*c for (n, c) in enumerate(p.coefs) if n > 0])

def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    return poly([C] + [float(c)/(n+1) for (n, c) in enumerate(p.coefs)])
