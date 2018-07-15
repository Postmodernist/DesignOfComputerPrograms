def bridge_problem2(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()  # set of states we have visited
    # State will be a (people-here, people-there) tuple
    # E.g. ({1, 2, 5, 10, 'light'}, {})
    frontier = [ [(here, frozenset())] ]  # ordered list of paths we have blazed
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        if issolution(path):
            return path
        state1 = final_state(path)
        explored.add(state1)
        t = path_cost(path)
        for (state, action) in bsuccessors2(state1).items():
            if state not in explored:
                path2 = path + [(action, t + bcost(action)), state]
                add_to_frontier(frontier, path2)
    return []

def issolution(path):
    "Test if path is a solution."
    return not path[-1][0] or path[-1][0] == set(['light'])

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def path_cost(path):
    """The total cost of a path (which is stored in a tuple
    with the final action."""
    # path = (state, (action, total_cost), state, ... )
    return path[-2][1] if len(path) > 2 else 0
        
def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are 
    # times; arrow is a string. 
    a, b, arrow = action
    return max(a, b)

def final_state(path):
    return path[-1]

def add_to_frontier(frontier, path):
    "Add path to frontier, replacing costlier path if there is one."
    # (This could be done more efficiently.)
    # Find if there is an old path to the final state of this path.
    old = None
    for i,p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None:
        if path_cost(path) < path_cost(frontier[old]):
            del(frontier[old])  # old path was worse
        else:
            return              # old path was better
    # Add the new path and re-sort
    frontier.append(path)
    frontier.sort(key=path_cost)

def bsuccessors2(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
    '<-' for there to here."""

    def depart(i, j, grp):
        r = grp[:]
        del(r[j])
        if i != j:
            del(r[i])
        del(r[r.index('light')])
        return frozenset(r)

    def arrive(m1, m2, grp):
        r = grp[:]
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
                    sn = (hn, tn)
                else:
                    sn = (tn, hn)
                res[sn] = a

    here, there = state
    res = {}
    if 'light' in here:
        traverse('->')
    else:
        traverse('<-')
    return res
