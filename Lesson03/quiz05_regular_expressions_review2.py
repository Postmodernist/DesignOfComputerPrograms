def match(pattern, text):
    """
    Return True if pattern appears at the start of text
    
    For this quiz, please fill in the return values for:
        1) if pattern == '':
        2) elif pattern == '$':
    """

    if pattern == '':
        return text == ''
    elif pattern == '$':
        return text == ''
    # you can ignore the following elif and else conditions
    # We'll implement them in the next quiz
    elif len(pattern) > 1 and pattern[1] in '*?':
        return True
    else:
        return True
