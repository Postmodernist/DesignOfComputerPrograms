"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools as it

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    orderings = list(it.permutations(range(5)))
    Monday, Tuesday, Wednesday, Thursday, Friday = range(5)
    indexes = next((Hamming, Knuth, Minsky, Simon, Wilkes)
        for laptop, droid, tablet, iphone, unknown_device in orderings
        if laptop == Wednesday
           and tablet != Friday
           and (iphone == Tuesday or tablet == Tuesday)
        for programmer, writer, manager, designer, unknown_profession in orderings
        if designer != Thursday
           and designer != droid
           and manager != tablet
           and writer == laptop
        for Hamming, Knuth, Minsky, Simon, Wilkes in orderings
        if Hamming == programmer
           and Knuth == manager + 1
           and Knuth == Simon + 1
           and Minsky != writer
           and Wilkes == Monday
           and Wilkes != programmer
           and Wilkes == droid)
    return [x[1] for x in sorted(zip(indexes, ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']))]

print(logic_puzzle())
