# -----------------
# User Instructions
# 
# Write the two action functions, hold and roll. Each should take a
# state as input, apply the appropriate action, and return a new
# state. 
#
# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored

from collections import namedtuple

State = namedtuple('State', 'p me you pending')

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    return State(state.p^1, state.you, state.me+state.pending, 0)


def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    if d == 1:
        return hold(State(state.p, state.me, state.you, 1))
    else:
        return State(state.p, state.me, state.you, state.pending+d)


## states are tuples of the form:
## (p, me, you, pending) where
##  p:   an int, 0 or 1, indicating which player's turn it is
##  me:  an int, the player-to-move's current score
##  you: an int, the other player's current score
##  pending: and int, the number of points accumulated on current turn, not yet scored

def test():    
    assert hold(State(1, 10, 20, 7))    == State(0, 20, 17, 0)
    assert hold(State(0, 5, 15, 10))    == State(1, 15, 15, 0)
    assert roll(State(1, 10, 20, 7), 1) == State(0, 20, 11, 0)
    assert roll(State(0, 5, 15, 10), 5) == State(0, 5, 15, 15)
    return 'tests pass'

print(test())
