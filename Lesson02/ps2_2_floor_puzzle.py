#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools

def floor_puzzle():
    res = next((Hopper, Kay, Liskov, Perlis, Ritchie)
        for Hopper, Kay, Liskov, Perlis, Ritchie in itertools.permutations([1, 2, 3, 4, 5])
        if Hopper != 5
        if Kay != 1
        if Liskov != 1 and Liskov != 5
        if Perlis > Kay
        if Ritchie-Liskov != 1 and Liskov-Ritchie != 1
        if Liskov-Kay != 1 and Kay-Liskov != 1)
    return list(res)

print(floor_puzzle())
