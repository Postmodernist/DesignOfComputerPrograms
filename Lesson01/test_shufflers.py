import random
import itertools


def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    """Shuffle the deck and deal out numhands n-card hands."""
    shuffle1(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]


def shuffle1(deck):
    """My teacher's algorithm."""
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = swapped[j] = True
        swap(deck, i, j)


def shuffle2(deck):
    """A modification of my teacher's algorithm."""
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = True
        swap(deck, i, j)


def shuffle3(deck):
    """An easier modification of my teacher's algorithm."""
    N = len(deck)
    for i in range(N):
        swap(deck, i, random.randrange(N))


def shuffle(deck):
    """Knuth's Algorithm P."""
    N = len(deck)
    for i in range(N-1):
        swap(deck, i, random.randrange(i, N))


def swap(deck, i, j):
    """Swap elements i and j of a collection."""
    deck[i], deck[j] = deck[j], deck[i]

# My version

def test_shuffler(shuffler, deck='abc', n=100*1000):
    chart = {v : 0 for v in itertools.permutations(deck)}
    for _ in range(n):
        tmp = list(deck)
        shuffler(tmp)
        chart[tuple(tmp)] += 1
    for v in chart:
        print("{}  {:.3f}%".format(''.join(v), chart[v]/(n/100)))

# Norvig's version

def test_shuffler(shuffler, deck='abcd', n=10000):
    counts = {''.join(v) : 0 for v in itertools.permutations(deck)}
    for _ in range(n):
        input = list(deck)
        shuffler(input)
        counts[''.join(input)] += 1
    e = n*1./factorial(len(deck))  # expected count
    ok = all((0.9 <= counts[item]/e <= 1.1) for item in counts)
    name = shuffler.__name__
    print("{}({}) {}".format(name, deck, ('ok' if ok else '*** BAD ***')))
    print("   "),
    for item, count in sorted(counts.items()):
        print("{}:{:4.1f}".format(item, count*100./n)),
    print()

def test_shufflers(shufflers=[shuffle, shuffle1], decks=['abc', 'ab']):
    for deck in decks:
        print()
        for f in shufflers:
            test_shuffler(f, deck)

def factorial(n):
    return 1 if (n <= 1) else n*factorial(n-1)
