# -----------------
# User Instructions
# 
# This problem deals with the one-player game foxes_and_hens. This 
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'. 
# 
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions, 
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card. 
#
# Your job is to define two functions. The first is do(action, state), 
# where action is either 'gather' or 'wait' and state is a tuple of 
# (score, yard, cards). This function should return a new state with 
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an 
# action based on the state. This strategy should average at least 
# 1.5 more points than the take5 strategy.

import random, pickle
from functools import wraps

# -----------------------------------------------------------------------------
# Game

def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def strpop(s, i):
    return s[:i]+s[i+1:], s[i]

def do(action, state):
    """Apply action to state, returning a new state."""
    score, yard, cards = state
    cards, card = strpop(cards, random.randrange(len(cards)))
    if action == 'wait':
        yard = yard + 1 if card == 'H' else 0
        return (score, yard, cards)
    if action == 'gather':
        score += yard
        yard = 0
        return (score, yard, cards)
    raise ValueError

def take5(state):
    """A strategy that waits until there are 5 hens in yard, then gathers."""
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=1000):
    res = []
    for _ in range(N):
        res.append(foxes_and_hens(strategy))
    return '%16s: %g\t43: %d\t44: %d\t45: %d' % \
        (strategy.__name__, sum(res) / float(N), res.count(43), res.count(44), res.count(45))

def superior(A, B=take5):
    """Does strategy A have a higher average score than B, by more than 1.5 point?"""
    return average_score(A) - average_score(B) > 1.5

# -----------------------------------------------------------------------------
# Strategies

## Probability threshold

def prob_thold(th=0.7):
    """Probability threshold."""
    def f(state):
        score, yard, cards = state
        # just wait in trivial case
        if 'F' not in cards:
            return 'wait'
        # compute longest H streak that is above probability threshold
        Phen = cards.count('H') / float(len(cards))
        k = 1
        while Phen > th and len(cards) + k <= 52:
            Phen *= (cards.count('H') + k) / (float(len(cards)) + k)
            k += 1
        # compare H sequence len so far to max streak len
        if yard < k:
            return 'wait'
        else:
            return 'gather'
    f.__name__ = 'Ptreshold(%g)' % th
    return f

## Optimal

def optimal(state):
    """Optimal."""
    return max((Q_fh(state, action), action) for action in A_fh(state))[1]

def A_fh(state):
    return ['wait', 'gather'] if state[1] else ['wait']

def Q_fh(state, action):
    score, yard, cards = state
    n = len(cards)
    f = cards.count('F')
    h = n - f
    if action == 'wait':
        state_f = (score, 0, cards[1:])       if 'F' in cards else None
        state_h = (score, yard+1, cards[:-1]) if 'H' in cards else None
    else:
        state_f = (score+yard, 0, cards[1:])  if 'F' in cards else None
        state_h = (score+yard, 0, cards[:-1]) if 'H' in cards else None
    return (f * U_fh(state_f) + h * U_fh(state_h)) / float(n)

@memo
def U_fh(state):
    if state is None:
        return 0
    score, yard, cards = state
    if len(cards) == 0:
        return score + yard
    return max(Q_fh(state, action) for action in A_fh(state))

## Norvig's strategy

def strategy(state):
    score, yard, cards = state
    if 'F' not in cards:
        return 'wait'
    if yard >= 3:
        return 'gather'
    return 'wait'

# -----------------------------------------------------------------------------
# Tools

def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    f.cache = {}
    @wraps(f)
    def wrapper(*args):
        try:
            return f.cache[args]
        except KeyError:
            f.cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return wrapper

def save(item=U_fh.cache):
    """Export U_fh cache."""
    foxes_and_hens(optimal)
    with open('cache.pickle', 'wb') as f:
        pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)

def load(fname='cache.pickle'):
    """Import U_fh cache."""
    with open(fname, 'rb') as f:
        return pickle.load(f)


# -----------------------------------------------------------------------------
# Test

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or 
            gather == (9, 0, 'F'*4 + 'H'*9))
    
    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))
    
    assert superior(strategy())
    return 'tests pass'

# print(test())

# Test thresholds
# for i in (0.67, 0.68, 0.69, 0.7, 0.71):
#     print('%g\t%g' % (i, average_score(strategy(i), 50000)))

U_fh.cache = load()
print(average_score(prob_thold(), 100000))  # ~32.77
print(average_score(optimal, 100000))  # ~32.85
print(average_score(strategy, 100000))  # ~32.38
