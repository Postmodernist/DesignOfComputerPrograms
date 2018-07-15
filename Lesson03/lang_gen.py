def genseq(x, y, Ns, startx=0):
    "Set of matches to xy whose total len is in Ns, with x-match's len in Ns_x."
    # Tricky part: x+ is defined as: x+ = x x*
    # To stop the recursion, the first x must generate at least 1 char,
    # and then the recursive x* has that many fewer characters. We use
    # startx=1 to say that x must match at least 1 character
    if not Ns:
        return null
    xmatches = x(set(range(startx, max(Ns)+1)))
    Ns_x = set(len(m) for m in xmatches)
    Ns_y = set(n-m for n in Ns for m in Ns_x if n-m >= 0)
    ymatches = y(Ns_y)
    return set(m1 + m2
                for m1 in xmatches for m2 in ymatches
                if len(m1+m2) in Ns)


def lit(s):
    set_s = set([s])
    len_s = len(s)
    return lambda Ns: set_s if len_s in Ns else null

def alt(x, y):
    return lambda Ns: x(Ns) | y(Ns)

def star(x):
    f = opt(plus(x))
    return lambda Ns: f(Ns)

def plus(x):
    return lambda Ns: genseq(x, star(x), Ns, startx=1) #Tricky

def oneof(chars):
    set_chars = set(chars)
    return lambda Ns: set_chars if 1 in Ns else null

def seq(x, y):
    return lambda Ns: genseq(x, y, Ns)

def opt(x):
    f = alt(epsilon, x)
    return f

dot = oneof('?')    # You could expand the alphabet to more chars.
epsilon = lit('')   # The pattern that matches the empty string.

null = frozenset([])


def test_gen():
    def N(hi): return set(range(hi+1))
    a,b,c = map(lit, 'abc')
    assert star(oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert (seq(star(a), seq(star(b), star(c)))(set([4])) ==
        set(['aaaa', 'aaab', 'aaac', 'aabb', 'aabc', 'aacc', 'abbb', 'abbc', 'abcc',
            'accc', 'bbbb', 'bbbc', 'bbcc', 'bccc', 'cccc']))
    assert (seq(plus(a), seq(plus(b), plus(c)))(set([5])) ==
        set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert (seq(star(alt(a, b)), opt(c))(set([3])) ==
        set(['aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'baa', 'bab', 'bac', 'bba',
            'bbb', 'bbc']))
    assert lit('hello')(set([5])) == set(['hello'])
    assert lit('hello')(set([4])) == set()
    assert lit('hello')(set([6])) == set()
    return 'test_gen passes'


print(test_gen())
