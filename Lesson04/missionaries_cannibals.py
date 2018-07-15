# Missionaries and Cannibals

from operator import add, sub

actions = ('MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-CC', '<-M', '<-C')


def mc_problem(start=(3, 3, 1, 0, 0, 0), goal=None):
    """Solve the missionaries and cannibals problem.
    State is 6 ints: (M1, C1, B1, M2, C2, B2) on the start (1) and other (2) sides.
    Find a path that goes from the initial state t the goal state (which, if not
    specified, is the state with no people or boats on the start side)."""
    if goal is None:
        goal = (0, 0, 0, start[0] + start[3], start[1] + start[4], start[2] + start[5])
    if start == goal:
        return frontier[0]
    frontier = [ [start] ]
    explored = set()
    while frontier:
        path = frontier.pop(0)
        state = path[-1]
        if state == goal:
            return path  # path found
        explored.add(state)
        for state2, action in csuccessors(state).items():
            if state2 not in explored:
                path2 = path + [action, state2]
                frontier.append(path2)
                frontier.sort(key=len)
    return []  # path not found


def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    res = {}
    
    if is_dead_state(state):
        return {}

    for a in actions:
        if '>' in a:
            op1, op2 = sub, add
        else:
            op1, op2 = add, sub
        M1, C1, B1, M2, C2, B2 = state
        M1 = op1(M1, a.count('M'))
        C1 = op1(C1, a.count('C'))
        B1 = op1(B1, 1)
        M2 = op2(M2, a.count('M'))
        C2 = op2(C2, a.count('C'))
        B2 = op2(B2, 1)
        state2 = (M1, C1, B1, M2, C2, B2)
        if is_legit_state(state2):
            res[state2] = a
    return res


def is_legit_state(state):
    """Test if all numbers of people/boats are non-negative."""
    return all(map(lambda x: x >= 0, state))


def is_dead_state(state):
    """Test if state is not legit or cannibals eat missionaries."""
    M1, C1, B1, M2, C2, B2 = state
    return any(map(lambda x: x < 0, state)) or M1 < C1 or M2 < C2

