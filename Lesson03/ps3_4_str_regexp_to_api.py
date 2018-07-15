## Unit 3 Homeword: parse/convert str regular expression to API

import re
from tools import *

# -----------------------------------------------------------------------------
# Public methods

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:
            return m

def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    f = parse_re(pattern)
    remainders = f(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]

# -----------------------------------------------------------------------------
# RE API

def lit(s): return lambda t: set([t[len(s):]]) if t.startswith(s) else null
def seq(x, y): return lambda t: set().union(*map(y, x(t)))
def alt(x, y): return lambda t: x(t) | y(t)
def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null
dot = lambda t: set([t[1:]]) if t else null
eol = lambda t: set(['']) if t == '' else null
def star(x): return lambda t: (set([t]) | set(t2 for t1 in x(t) if t1 != t
                               for t2 in star(x)(t1)))

null = frozenset([])

# -----------------------------------------------------------------------------
# Grammar

def grammar(description, whitespace=r'\s*'):
    """Convert a description to a grammar.  Each line is a rule for a
    non-terminal symbol; it looks like this:
        Symbol =>  A1 A2 ... | B1 B2 ... | C1 C2 ...
    where the right-hand side is one or more alternatives, separated by
    the '|' sign.  Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.
    
    Notation for *, +, or ? not allowed in a rule alternative (but ok
    within a token). Use '\' to continue long lines.  You must include spaces
    or tabs around '=>' and '|'. That's within the grammar description itself.
    The grammar that gets defined allows whitespace between tokens by default;
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between tokens)."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit=-1):
    "Like str.split applied to text, but strips whitespace from each piece."
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '({})'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem  
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer.format(atom), text)
            return Fail if (not m) else (m.group(1), text[m.end():])

    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)

REGRAMMAR = grammar("""
RE          =>  seq
seq         =>  element seq | element
element     =>  star | alt | oneof | dot | eol | lit
element_s   =>  alt | oneof | dot | lit
alt         =>  \( element \| element \)
oneof       =>  \[ lit \]
dot         =>  \.
eol         =>  \^
star        =>  element_s \*
lit         =>  ([^\\\(\)\|\[\]\.\^\*]|\\\\[\(\)\|\[\]\.\^\*])+(?!\*) | ([^\\\(\)\|\[\]\.\^\*]|\\\\[\(\)\|\[\]\.\^\*])
""", whitespace='')

# -----------------------------------------------------------------------------
# Compiler

api_funcs = 'lit seq dot eol star alt oneof'.split()
control_chars = '( ) [ ] | . ^ *'.split()

@memo
def parse_re(pattern):
    "Take string pattern and return match function."
    return convert(parse('RE', pattern, REGRAMMAR))

def convert(tree):
    "Take parse tree and return match function."
    assert not tree[1]
    f = convert_r(cleantree_r(tree[0]))
    return f if f else lambda x: x

def convert_r(tree):
    "Create match function from tree."
    if not tree:
        return lambda t : ''
    op = tree[0] if type(tree) == list else tree
    if op == 'lit':
        return lit(tree[1])
    if op == 'seq':
        x = convert_r(tree[1])
        if len(tree) == 2:
            return lambda t: x(t)
        else:
            y = convert_r(tree[2])
            return seq(x, y)
    if op == 'alt':
        return alt(convert_r(tree[1]), convert_r(tree[2]))
    if op == 'oneof':
        return oneof(tree[1][1])
    if op == 'dot':
        return dot
    if op == 'eol':
        return eol
    if op == 'star':
        return star(convert_r(tree[1]))        

def cleantree_r(tree):
    "Clean parse tree, leaving only api functions and literals."
    if not tree:                    # empty tree
        return None
    elif type(tree) != list:        # leaf node
        return tree if tree not in control_chars else None
    else:                           # branch
        res = []
        reroot = True
        if tree[0] in api_funcs:
            res.append(tree[0])
            reroot = False
        for t in tree[1:]:
            ct = cleantree_r(t)
            if ct:
                if type(ct) == list and (reroot or len(ct) == 1):
                    res.extend(ct)
                else:
                    res.append(ct)
        return res


# -----------------------------------------------------------------------------
# Tests

def printtree_r(tree, tab=0):
    "Print tree."
    if not tree or len(tree) == 0:
        return
    print('  '*tab, end='')
    if type(tree) != list:
        print(tree)
    else:
        print(tree[0])
        for t in tree[1:]:
            printtree_r(t, tab+1)

def test():
    assert search('def', 'abcdefg') == 'def'
    assert search('def^', 'abcdefg') == None
    assert search('a', 'not the start') == 'a'
    assert match('a', 'not the start') == None
    assert match('a*b*c*', 'aaabbbccccccccccdef') == 'aaabbbcccccccccc'
    assert match('a*b*c*', 'junk') == ''
    assert all(match('a*b*c*^', s) == s for s in 'abc aaabbccc aaaabcccc'.split())
    assert all(match('a*b*c*^', s) == None for s in 'cab aaabbcccd aaaa-b-cccc'.split())
    r = 'ab.*aca.*a^'
    assert all(search(r, s) is not None
                for s in 'abracadabra abacaa about-acacia-flora'.split())
    assert all(match('c.*b', s) is not None
                for s in 'cab cob carob cb carbuncle'.split())
    assert not any(match('c.b', s)
                for s in 'crab cb across scab'.split())
    return 'test_search passes'

print(test())
