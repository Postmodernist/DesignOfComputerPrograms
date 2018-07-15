import math

million = 1000000

def Q(state, action, U):
    """The expected value of taking action in state, according to utility U."""
    if action == 'hold':
        return U(state + 1*million)
    if action == 'gamble':
        return U(state + 3*million) * 0.5 + U(state) * 0.5

def actions(state):
    return ['hold', 'gamble']

def identity(x):
    return x

U = identity

def best_action(state, actions, Q, U):
    """Return optimal action for a state, given U."""
    def EU(action):
        return Q(state, action, U)
    return max(actions(state), key=EU)

print(best_action(100, actions, Q, identity))  # linear money value

print(best_action(100, actions, Q, math.log))  # logarithmic money value

print(best_action(10*million, actions, Q, math.log))  # log value, 10M start
