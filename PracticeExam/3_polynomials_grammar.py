
"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of 
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**' 
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""

## Solution (2)

import re
from functools import wraps

# -----------------------------------------------------------------------------
# Original poly for test purposes

def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""

    terms = [term(c, p) for p, c in enumerate(coefs)]

    def _f(x):
        return sum(t(x) for t in terms)

    _f.coefs = coefs
    _f.ispoly = True
    _f.__name__ = poly_formula(coefs)
    return _f

def term(c, p): return lambda x: c * x**p

def poly_formula(coefs):
    res = ''.join((' - ' if c < 0 else ' + ')
        + (((str(c)[1:] if c < 0 else str(c)) + (' * ' if p else '')) if p == 0 or abs(c) > 1 else '')
        + (('x**' + str(p)) if p > 1 else 'x' if p == 1 else '')
        for p, c in reversed(list(enumerate(coefs))) if c)
    return res if coefs[-1] < 0 else res[3:]

p1 = poly((10, 20, 30))

def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""
    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
    return canonical_name(name1) == canonical_name(name2)

# -----------------------------------------------------------------------------
# Grammar solution

def grammar(description, whitespace=r'\s*'):
    "Convert a description to a grammar."
    G = {' ': whitespace}
    description = description.replace('\t', ' ')  # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit=-1):
    "Like str.split applied to text, but strips whitespace from each piece."
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

# Expression example: 30 * x**2 + 20 * x + 10
G = grammar(r"""
Term    => Factor \* Factor [+-] Term | Factor [+-] Term | Factor \* Factor | Factor
Factor  => Num | Var
Num     => [0-9]+
Var     => x \*\* [0-9]+ | x
""")

fail = (None, None)
tokenizer = G[' '] + '(%s)'

def parse(text, atom='Term'):
    "Example call: parse('30 * x**2 + 20 * x + 10'). Return a (tree, remainder) pair."
    global G, fail, tokenizer
    if atom in G:  # Non-Terminal: tuple of alternatives
        for alternative in G[atom]:
            tree = []
            rem = text
            for atom_alt in alternative:
                subtree, rem = parse(rem, atom_alt)
                if rem is None: break
                tree.append(subtree)
            else:
                return [atom]+tree, rem
        return fail
    else:  # Terminal: match characters against start of text
        m = re.match(tokenizer % atom, text)
        return (m.group(1), text[m.end():]) if m else fail

def convert(tree):
    "Convert parse tree to coefs tuple."
    if not tree: return tuple()
    coef_pow_pairs = convert_term(tree)
    powr_counter = coef_pow_pairs[0][1]
    # add 0's for missing terms and reverse coefs list
    res = []
    for coef, powr in coef_pow_pairs:
        if powr_counter > powr:
            res += [0] * (powr_counter - powr)
            powr_counter = powr
        res.append(coef)
        powr_counter -= 1
    return tuple(reversed(res))

def convert_term(tree, sign=1):
    "Recursively convert terms from parse tree to a sequence of (coef, powr) pairs."
    if not tree: return []
    assert tree[0] == 'Term'
    factors = {x[1][0] : x[1][1:] for x in tree if x[0] == 'Factor'}
    nextterm = tree[-1] if tree[-1][0] == 'Term' else None
    coef = sign * (int(factors['Num'][0]) if 'Num' in factors else 1)
    powr = (int(factors['Var'][2]) if len(factors['Var']) == 3 else 1) if 'Var' in factors else 0
    sign = -1 if '-' in tree else 1
    return [(coef, powr)] + convert_term(nextterm, sign)

def poly(exp):
    tree, rem = parse(exp)
    if rem: raise ValueError('parsing failed: ' + exp)
    coefs = convert(tree)
    terms = [term(c, p) for p, c in enumerate(coefs)]
    def _f(x): return sum(t(x) for t in terms)
    _f.coefs = coefs
    _f.ispoly = True
    _f.__name__ = canonize(exp)
    return _f

def canonize(exp):
    exp = exp.replace(' ', '')
    exp = exp.replace('+', ' + ')
    exp = exp.replace('-', ' - ')
    exp = exp.replace('*', ' * ')
    exp = exp.replace(' *  * ', '**')
    return exp

# -----------------------------------------------------------------------------
# Tests

def test_poly2():
    newp1 = poly('30 * x**2 + 20 * x + 10')
    assert p1(100) == newp1(100)
    assert same_name(p1.__name__,newp1.__name__)
    print('test_poly2 passes')

