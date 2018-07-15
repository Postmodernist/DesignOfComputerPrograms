from using_tools import *

def story():
    r = defaultdict(lambda: [0, 0])
    for s in states:
        w, d = max_wins(s), max_diffs(s)
        if w != d:
            pending = s[3]
            i = 0 if (w == 'roll') else 1
            r[pending][i] += 1
    print('pending: max_wins rolls  max_diffs rolls')
    for (delta, (wrolls, drolls)) in sorted(r.items()):
        print('%4d: %3d %3d' % (delta, wrolls, drolls))

if __name__ == '__main__':
    story()
