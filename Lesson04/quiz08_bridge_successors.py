# -----------------
# User Instructions
# 
# Write a function, bsuccessors(state), that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# A state is a (here, there, t) tuple, where here and there are 
# frozensets of people (indicated by their times), and potentially
# the 'light,' t is a number indicating the elapsed time.
#
# An action is a tuple (person1, person2, arrow), where arrow is 
# '->' for here to there or '<-' for there to here. When only one 
# person crosses, person2 will be the same as person one, so the
# action (2, 2, '->') means that the person with a travel time of
# 2 crossed from here to there alone.


#### My solution

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
    '<-' for there to here."""

    def depart(i, j, grp):
        r = grp.copy()
        del(r[j])
        if i != j:
            del(r[i])
        del(r[r.index('light')])
        return frozenset(r)

    def arrive(m1, m2, grp):
        r = grp.copy()
        r.append(m1)
        if m1 != m2:
            r.append(m2)
        r.append('light')
        return frozenset(r)

    def traverse(dir):
        grp1, grp2 = (list(here), list(there)) if dir == '->' else (list(there), list(here))
        li = grp1.index('light')
        for i in range(len(grp1)):
            if i == li:
                continue
            for j in range(i, len(grp1)):
                if j == li:
                    continue
                a = (grp1[i], grp1[j], dir)
                hn = depart(i, j, grp1)
                tn = arrive(grp1[i], grp1[j], grp2)
                if dir == '->':
                    sn = (hn, tn, t + max(grp1[i], grp1[j]))
                else:
                    sn = (tn, hn, t + max(grp1[i], grp1[j]))
                res[sn] = a

    here, there, t = state
    res = {}
    if 'light' in here:
        traverse('->')
    else:
        traverse('<-')
    return res

#### Norvig's solution

# def bsuccessors(state):
#     """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
#     where here and there are frozensets of people (indicated by their times) and/or
#     the 'light', and t is a number indicating the elapsed time. Action is represented
#     as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
#     '<-' for there to here."""

#     def dif(a, b): return a - b
#     def uni(a, b): return a | b

#     def move(dir):
#         nonlocal here, there
#         op1, op2, grp = (dif, uni, here) if dir == '->' else (uni, dif, there)
#         return dict(((op1(here,  frozenset([a, b, 'light'])),
#                       op2(there, frozenset([a, b, 'light'])),
#                       t + max(a, b)),
#                      (a, b, dir))
#                     for a in grp if a is not 'light'
#                     for b in grp if b is not 'light')

#     here, there, t = state
#     return move('->') if 'light' in here else move('<-')


def test():

    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == \
        {(frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) == \
        {(frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    
    return 'tests pass'

print(test())
