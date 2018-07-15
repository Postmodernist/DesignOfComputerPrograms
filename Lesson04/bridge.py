def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()  # set of states we have visited
    # State will be a (people-here, people-there, time-elapsed)
    frontier = [ [(here, frozenset(), 0)] ]  # ordered list of paths we have blazed
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        if issolution(path):
            return path
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                here, there, t = state
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time)
    return []

def elapsed_time(path):
    return path[-1][2]

def issolution(path):
    return not path[-1][0] or path[-1][0] == set(['light'])

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

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
