# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

# My solution

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    res = (0, 0)
    for k in range(len(text) * 2 - 3):
        i, j = int(k / 2), int((k + 3) / 2)
        palin = False
        while i >= 0 and j < len(text) and text[i].lower() == text[j].lower():
            palin = True
            i -= 1
            j += 1
        i += 1
        if palin and j - i > res[1] - res[0]:
            res = (i, j)
    return res

# Norvig's solution

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if text == '':
        return (0, 0)
    candidates = [grow(text, start, end)
                  for start in range(len(text))
                  for end in (start, start+1)]
    return max(candidates, key=lambda x: x[1]-x[0])

def grow(text, start, end):
    "Start with a 0- or 1- length palindrome; try to grow a bigger one."
    while start > 0 and end < len(text) and text[start-1].upper() == text[end].upper():
        start -= 1
        end += 1
    return start, end

def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print(test())
