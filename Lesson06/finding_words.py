import itertools as it
import time

def readwordlist(filename='words.txt'):
    """Read the words from a file and return a set of the words 
    and a set of the prefixes."""
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    print('%d words loaded from %s' % (len(wordset), filename))
    return wordset, prefixset

def find_words_my(letters):
    """Find all words that can be made from the letters in hand."""
    lperms = it.chain(*[it.permutations(letters, i) for i in range(1, len(letters)+1)])
    res = set()
    for w in lperms:
        w = ''.join(w)
        if w in WORDS:
            res.add(w)
    return res

def find_words1(hand):
    """Find all words that can be made from the letters in hand."""
    res = set()
    for a in hand:
        if a in WORDS: res.add(a)
        for b in removed(hand, a):
            w = a+b
            if w in WORDS: res.add(w)
            for c in removed(hand, w):
                w = a+b+c
                if w in WORDS: res.add(w)
                for d in removed(hand, w):
                    w = a+b+c+d
                    if w in WORDS: res.add(w)
                    for e in removed(hand, w):
                        w = a+b+c+d+e
                        if w in WORDS: res.add(w)
                        for f in removed(hand, w):
                            w = a+b+c+d+e+f
                            if w in WORDS: res.add(w)
                            for g in removed(hand, w):
                                w = a+b+c+d+e+f+g
                                if w in WORDS: res.add(w)
    return res

def find_words2(hand):
    """Find all words that can be made from the letters in hand."""
    res = set()
    for a in hand:
        if a in WORDS: res.add(a)
        if a not in PREFIXES: continue
        for b in removed(hand, a):
            w = a+b
            if w in WORDS: res.add(w)
            if w not in PREFIXES: continue
            for c in removed(hand, w):
                w = a+b+c
                if w in WORDS: res.add(w)
                if w not in PREFIXES: continue
                for d in removed(hand, w):
                    w = a+b+c+d
                    if w in WORDS: res.add(w)
                    if w not in PREFIXES: continue
                    for e in removed(hand, w):
                        w = a+b+c+d+e
                        if w in WORDS: res.add(w)
                        if w not in PREFIXES: continue
                        for f in removed(hand, w):
                            w = a+b+c+d+e+f
                            if w in WORDS: res.add(w)
                            if w not in PREFIXES: continue
                            for g in removed(hand, w):
                                w = a+b+c+d+e+f+g
                                if w in WORDS: res.add(w)
                                if w not in PREFIXES: continue
    return res

def find_words3(letters):
    return extend_prefix('', letters, set())

def find_words4(letters, pre='', results=None):
    if results is None: results = set()
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            find_words4(letters.replace(L, '', 1), pre+L, results)
    return results


# -----------------------------------------------------------------------------
# Helpers

def timedcall(fn, *args):
    """Call a function with args; return the time in seconds and result."""
    t0 = time.clock()
    res = fn(*args)
    t1 = time.clock()
    return t1-t0, res

def removed(letters, remove):
    """Return a str of letters, but with each letter in remove removed once."""
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def prefixes(word):
    """A list of the initial sequences of a word, not including the complete word."""
    return [word[:i] for i in range(len(word))]

def extend_prefix(pre, letters, results):
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results)
    return results


# -----------------------------------------------------------------------------
# Tests

WORDS, PREFIXES = readwordlist('words4k.txt')

# Regression test
hands = {
    'ABECEDR':  set(['BRA', 'AE', 'ARC', 'EAR', 'DAB', 'BEAR', 'BAR', 'RED', 'CAB', 'ARB', 'RACE', 'BE', 'CARE', 'REB', 'ERA', 'ARE', 'CAD', 'DEE', 'CEE', 'DE', 'AD', 'DEB', 'REC', 'READ', 'ER', 'BA', 'AB', 'ACE', 'BAD', 'BEE', 'RAD', 'ERE', 'REE', 'CAR', 'ED', 'DEAR', 'AR', 'RE', 'BED']),
    'AEINRST':  set(['ANESTRI', 'AIR', 'RAN', 'EAT', 'SER', 'TEA', 'AIT', 'ERA', 'RETINAS', 'TAE', 'ANT', 'ARS', 'NAE', 'AI', 'SEA', 'AIN', 'ER', 'NASTIER', 'IRE', 'NA', 'SEI', 'IS', 'TAS', 'NEAR', 'RE', 'AS', 'RISE', 'RET', 'SIT', 'ANTSIER', 'ETA', 'TI', 'SIN', 'RIN', 'NE', 'RIA', 'TIN', 'INS', 'SEAT', 'RAT', 'EN', 'NIT', 'SET', 'AT', 'ITS', 'AR', 'STIR', 'ES', 'SI', 'AE', 'RATE', 'RATINES', 'RAIN', 'EAST', 'SAE', 'TEN', 'TAN', 'TAR', 'RES', 'ARE', 'RAISE', 'STAIN', 'TA', 'ENS', 'TRAIN', 'STEARIN', 'ERS', 'SEN', 'REI', 'TIE', 'STAIR', 'ART', 'IN', 'ARTS', 'REST', 'RAS', 'EAR', 'ATE', 'STAINER', 'TEAR', 'SRI', 'TIS', 'AIS', 'NET', 'ANI', 'RETSINA', 'ANE', 'EARN', 'ET', 'SENT', 'RETAINS', 'IT', 'AN', 'ERN', 'SAT', 'SIR']),
    'DRAMITC':  set(['CAM', 'ARC', 'TAM', 'MI', 'AIR', 'ARM', 'CAT', 'AIM', 'AIT', 'TI', 'MAT', 'TAR', 'DIT', 'RIM', 'RAM', 'TA', 'TIC', 'CAD', 'RIA', 'MAC', 'AID', 'ID', 'AI', 'AD', 'DAM', 'MIR', 'AM', 'RAT', 'RID', 'MID', 'MA', 'MAR', 'MAD', 'AMI', 'RAD', 'AT', 'IT', 'TAD', 'CAR', 'DIM', 'ART', 'ACT', 'AR']),
    # 'ADEINRST': set(['ET', 'IDEAS', 'RETAINS', 'AID', 'TEAR', 'DEN', 'ANTIRED', 'RES', 'RAD', 'RID', 'READ', 'AI', 'NASTIER', 'DIT', 'STAIR', 'RETSINA', 'DIN', 'ATE', 'ARE', 'SEI', 'ADS', 'RED', 'RAISED', 'NAE', 'STAINER', 'STIR', 'IS', 'ANT', 'AD', 'STRAINED', 'RAISE', 'NET', 'IDS', 'TAR', 'DINE', 'AIS', 'SER', 'TED', 'TRAINED', 'ENDS', 'TRIED', 'DIE', 'AIT', 'TAE', 'SIT', 'ERS', 'ID', 'STAND', 'AT', 'ANE', 'TRAIN', 'ARTS', 'NE', 'STEARIN', 'RIA', 'AIR', 'EARN', 'ARS', 'TIS', 'DETRAINS', 'EAT', 'SAD', 'NA', 'RAS', 'ANESTRI', 'SIR', 'RATE', 'ERA', 'RAIN', 'TRADE', 'RIN', 'TAS', 'SENT', 'RETINAS', 'IDEA', 'RISE', 'SAID', 'REST', 'TEN', 'RIDE', 'ES', 'SAE', 'RET', 'TAD', 'EAR', 'ANTSIER', 'ANI', 'AND', 'TIN', 'INSTEAD', 'NEAR', 'RAN', 'SIDE', 'RANDIEST', 'REI', 'SEA', 'ENS', 'ER', 'END', 'AN', 'TAN', 'AIN', 'EAST', 'SI', 'TIE', 'TA', 'IN', 'ETA', 'IRE', 'DATE', 'DIS', 'AR', 'TEA', 'ITS', 'SAT', 'ERN', 'SEN', 'STAIN', 'RAT', 'AE', 'AS', 'SEND', 'DEAR', 'TI', 'ART', 'NIT', 'DETRAIN', 'ASIDE', 'SET', 'SIN', 'EN', 'INS', 'SRI', 'SEAT', 'ED', 'IT', 'DE', 'RE', 'RATINES']),
    'ETAOIN':   set(['AE', 'ONE', 'ATE', 'TOE', 'EAT', 'TEA', 'NOT', 'NOTE', 'ETA', 'AIT', 'TI', 'TEN', 'NO', 'TAN', 'EON', 'INTO', 'TAE', 'TA', 'ANT', 'NE', 'ION', 'NAE', 'TIN', 'TO', 'AI', 'NET', 'ANI', 'OAT', 'ANE', 'AIN', 'EN', 'NIT', 'ET', 'TON', 'ON', 'NA', 'AT', 'IT', 'TIE', 'AN', 'TAO', 'IN', 'OE']),
    'SHRDLU':   set(['US', 'SH', 'UH', 'URD']),
    'SHROUDT':  set(['US', 'SH', 'OUT', 'RHO', 'HOT', 'OUR', 'UDO', 'THUS', 'SO', 'DOT', 'TOR', 'OS', 'OHS', 'DO', 'OD', 'RUT', 'HO', 'HOURS', 'OUD', 'HOUR', 'THO', 'SHORT', 'TO', 'ODS', 'SHOUT', 'HOD', 'ROT', 'DOS', 'SOUTH', 'SOD', 'ORT', 'DUO', 'URD', 'OR', 'UT', 'UH', 'DOR', 'DUST', 'TOD', 'UTS', 'SOT', 'ROD', 'OH', 'SHOT', 'SORT', 'HUT', 'SOU', 'ORS']),
    'TOXENSI':  set(['OSE', 'ES', 'EXIST', 'SI', 'ONE', 'NEXT', 'SEX', 'TOE', 'NOT', 'NOTE', 'XI', 'SO', 'SIT', 'TEN', 'TI', 'OS', 'EX', 'NO', 'ONS', 'EON', 'SIN', 'INTO', 'SIX', 'NOS', 'NE', 'ION', 'TIN', 'INS', 'TO', 'ENS', 'TIS', 'NIX', 'NET', 'NOSE', 'EN', 'NIT', 'ONES', 'SOX', 'SON', 'ET', 'XIS', 'TON', 'SOT', 'ON', 'SET', 'SEN', 'SENT', 'SEI', 'IS', 'IT', 'TIE', 'OES', 'ITS', 'OX', 'IN', 'STONE', 'OE'])
}

def test_words(func=find_words4):
    assert removed('LETTERS', 'L') == 'ETTERS'
    assert removed('LETTERS', 'T') == 'LETERS'
    assert removed('LETTERS', 'SET') == 'LTER'
    assert removed('LETTERS', 'SETTER') == 'L'
    assert prefixes('WORD') == ['', 'W', 'WO', 'WOR']
    results = map(func, hands)
    for ((hand, expected), got) in zip(hands.items(), results):
        assert got == expected, "For %r: got %s, expected %s (diff %s)" % (hand, got, expected, expected^got)
    return 'tests pass'

print('%s\ntime elapsed: %gs' % timedcall(test_words)[::-1])
