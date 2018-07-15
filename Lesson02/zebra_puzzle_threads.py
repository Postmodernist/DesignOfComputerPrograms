import itertools as it
from threading import Thread

def imright(h1, h2):
    """House h1 is immediately right of h2 if h1 - h2 == 1."""
    return h1 - h2 == 1

def nextto(h1, h2):
    """Two houses are next to each other if they differ by 1."""
    return abs(h1 - h2) == 1


def zebra_puzzle(n):
    """Return a tuple (WATER, ZEBRA) indicating their house numbers."""
    houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
    orderings = list(it.permutations(houses))
    batch_len = len(orderings) // 10
    res = next((WATER, ZEBRA)
        for (red, green, ivory, yellow, blue) in orderings[n*batch_len : (n+1)*batch_len]
        for (Englishman, Spaniard, Ukrainian, Japanese, Norwegian) in orderings
        for (dog, snails, fox, horse, ZEBRA) in orderings
        for (coffee, tea, milk, oj, WATER) in orderings
        for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in orderings
        if Englishman == red
        if Spaniard == dog
        if coffee == green
        if Ukrainian == tea
        if imright(green, ivory)
        if OldGold == snails
        if Kools == yellow
        if milk == middle
        if Norwegian == first
        if nextto(Chesterfields, fox)
        if nextto(Kools, horse)
        if LuckyStrike == oj
        if Japanese == Parliaments
        if nextto(Norwegian, blue))
    print(res)


def main():
    """Divide search space to 10 batches and run a thread for each."""
    threads = []
    for i in range(10):
        t = Thread(target=zebra_puzzle, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
