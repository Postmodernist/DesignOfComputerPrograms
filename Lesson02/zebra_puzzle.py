import itertools as it

def imright(h1, h2):
    """House h1 is immediately right of h2 if h1 - h2 == 1."""
    return h1 - h2 == 1

def nextto(h1, h2):
    """Two houses are next to each other if they differ by 1."""
    return abs(h1 - h2) == 1

def zebra_puzzle():
    """Return a tuple (WATER, ZEBRA) indicating their house numbers."""
    houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
    orderings = list(it.permutations(houses))
    return next((WATER, ZEBRA)
        for (red, green, ivory, yellow, blue) in c(orderings)
        if imright(green, ivory)
        for (Englishman, Spaniard, Ukrainian, Japanese, Norwegian) in c(orderings)
        if Englishman == red
        if Norwegian == first
        if nextto(Norwegian, blue)
        for (coffee, tea, milk, oj, WATER) in c(orderings)
        if coffee == green
        if Ukrainian == tea
        if milk == middle
        for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in c(orderings)
        if Kools == yellow
        if LuckyStrike == oj
        if Japanese == Parliaments
        for (dog, snails, fox, horse, ZEBRA) in c(orderings)
        if Spaniard == dog
        if OldGold == snails
        if nextto(Chesterfields, fox)
        if nextto(Kools, horse)
    )


import time

def timedcall(fn, *args):
    """Call a function with args; return the time in seconds and result."""
    t0 = time.clock()
    res = fn(*args)
    t1 = time.clock()
    return t1-t0, res

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times) < n:
            times.append(timedcall(fn, *args)[0])
    return min(times), average(times), max(times)

def average(numbers):
    """Return the average (arithmetic mean) of a sequence of numbers."""
    return sum(numbers) / float(len(numbers))

def c(sequence):
    """Generate items in sequence; keeping counts as we go. c.starts is the
    number of sequences started; c.items is number of items generated."""
    c.starts += 1
    for item in sequence:
        c.items += 1
        yield item

def instrument_fn(fn, *args):
    c.starts, c.items = 0, 0
    result = fn(*args)
    print("{} got {} with {:5d} iters over {:7d} items".format(fn.__name__, result, c.starts, c.items))


instrument_fn(zebra_puzzle)
print(timedcalls(10, zebra_puzzle))
print(timedcalls(3.0, zebra_puzzle))
