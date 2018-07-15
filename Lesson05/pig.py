"""
Pig (dice game)

Each turn, a player repeatedly rolls a die until either a 1 is rolled or the
player decides to "hold":
- If the player rolls a 1, they score nothing and it becomes the next player's
  turn.
- If the player rolls any other number, it is added to their turn total and the
  player's turn continues.
- If a player chooses to "hold", their turn total is added to their score, and
  it becomes the next player's turn.
The first player to score 100 or more points wins.

For example, the first player, Ann, begins a turn with a roll of 5. Ann could
hold and score 5 points, but chooses to roll again. Ann rolls a 2, and could
hold with a turn total of 7 points, but chooses to roll again. Ann rolls a 1,
and must end her turn without scoring. The next player, Bob, rolls the sequence
4-5-3-5-5, after which he chooses to hold, and adds his turn total of 22 points
to his score.
"""

import random

def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f


# -----------------------------------------------------------------------------
# Pig Game

goal = 40

def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (p, me, you, pending) = state
    if d == 1:
        return (p^1, you, me+1, 0)      # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (p, me, you, pending) = state
    return (p^1, you, me+pending, 0)

def Q_pig(state, action, U):  
    "The expected value of choosing action in state."
    if action == 'hold':
        return 1 - U(hold(state))
    if action == 'roll':
        return (1 - U(roll(state, 1))
                + sum(U(roll(state, d)) for d in (2,3,4,5,6))) / 6.0
    raise ValueError

def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def expected_utility(action): return Q(state, action, U)
    return max(actions(state), key=expected_utility)

def pig_actions(state):
    "The legal actions from a state."
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']

@memo
def Pwin(state):
    """The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state."""
    # Assumes opponent also plays with optimal strategy.
    (p, me, you, pending) = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig(state, action, Pwin)
                   for action in pig_actions(state))

def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)

def play_pig(A, B, dierolls=dierolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    player = [A, B]
    state  = (0, 0, 0 ,0)
    while state[2] < goal:
        action = player[state[0]](state)
        if action == 'hold':
            state = hold(state)
        else:
            state = roll(state, next(dierolls))
    return player[state[0]^1]


# -----------------------------------------------------------------------------
# Strategies

def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(pig_actions(state))

def hold_at(x):
    """Return a strategy that holds if and only if 
    pending >= x or player reaches goal."""
    def strategy(state):
        (p, me, you, pending) = state
        return 'hold' if (pending >= x or me + pending >= goal) else 'roll'
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy

def max_wins(state):
    "The optimal pig strategy chooses an action with the highest win probability."
    return best_action(state, pig_actions, Q_pig, Pwin)


# -----------------------------------------------------------------------------
# Tournament

def play_tournament(strategies):
    """Play single elimination tournament."""
    pairs = pairup(strategies)
    # qualification
    while len(pairs) > 1:
        winners = []
        for pair in pairs:
            if all(pair):
                winners.append(play_pig(*pair))
            else:
                winners.append(pair[0] if pair[0] else pair[1])
        pairs = pairup(winners)
    # final
    pair = pairs[0]
    if all(pair):
        return play_pig(*pair).__name__
    else:
        return pair[0] if pair[0] else pair[1]

def isodd(x):
    return bool(x%2)

def pairup(items):
    """Group items into random pairs."""
    tmp = items[:]
    if isodd(len(tmp)):
        tmp += [None]
    random.shuffle(tmp)
    return list(zip(tmp[:len(tmp)//2], tmp[len(tmp)//2:]))


# strategies = [clueless, hold_at(goal/4), hold_at(1+goal/3), hold_at(goal/2),
#               hold_at(goal), max_wins]
strategies = [hold_at(20), max_wins]


stats = {}
for _ in range(10000):
    winner = play_tournament(strategies)
    if winner in stats:
        stats[winner] += 1
    else:
        stats[winner] = 1
for item in sorted(stats.items(), key=lambda x: x[1], reverse=True):
    print("{}\t{}".format(*item))
