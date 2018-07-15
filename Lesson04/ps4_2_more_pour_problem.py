# -----------------
# User Instructions
# 
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes 
# as input capacities, goal, and (optionally) start. This function should 
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the 
# volume of a glass. 
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i), 
# ('empty', i), ('pour', i, j) where i and j are indices indicating the 
# glass number. 

import itertools as it


def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    start = (0,) * len(capacities) if start is None else start
    psuccessors = psuccessors_new(capacities)
    is_goal = lambda x: goal in x
    return shortest_path_search(start, psuccessors, is_goal)


def psuccessors_new(capacities):
    """Make a function that takes a state and returns a dict of all possible
    state:action pairs that change initial state. If more that one action
    lead to the same state then the first occurence is kept."""

    def fill(state, i):
        return replace(state, i, capacities[i])

    def empty(state, i):
        return replace(state, i, 0)

    def pour(state, i, j):
        res = list(state)
        tmp = res[i] + res[j]
        if tmp > capacities[j]:
            res[i], res[j] = tmp - capacities[j], capacities[j]
        else:
            res[i], res[j] = 0, tmp
        return tuple(res)

    actions = [(fill, 1), (empty, 1), (pour, 2)]  # (action, argc)
    groups = {a : list(it.permutations(range(len(capacities)), i))
                for a, i in actions}  # {action : args_combinations}

    def f(state):
        res = {}
        for action, _ in actions:
            for args in groups[action]:
               s = action(state, *args)
               if s != state and s not in res:
                   res[s] = (action.__name__,) + args
        return res
    return f


def replace(tup, i, v):
    return tup[:i] + (v,) + tup[i+1:]


def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []
    
def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print(test_more_pour())
