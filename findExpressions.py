import re
import Keywords
from BooleanExpression import BooleanExpression

def findExpressions(sql):

    reText = []
    for c in Keywords.comparators:
        reText.append(re.escape(c))
        reText.append('|')
    reText.pop()

    searchTerm = re.compile(''.join(reText), flags=re.IGNORECASE)

    i = 0
    matches = []
    while i < len(sql):
        m = searchTerm.search(sql, i)
        if m:
            matches.append(m)
            i = m.span()[1]
        else:
            break

    keyRevRe = []
    keyRe = []

    for s in Keywords.syntax:
        keyRevRe.append('(^|\\s)' + re.escape(s[::-1]) + '($|\\s)')
        keyRevRe.append('|')
        keyRe.append('(^|\\s)' + re.escape(s) + '($|\\s)')
        keyRe.append('|')
    for s in Keywords.binary_op:
        keyRevRe.append('(^|\\s)' + re.escape(s[::-1]) + '($|\\s)')
        keyRevRe.append('|')
        keyRe.append('(^|\\s)' + re.escape(s) + '($|\\s)')
        keyRe.append('|')
    keyRe.pop()
    keyRevRe.pop()

    forwardSearch = re.compile(''.join(keyRe), flags=re.IGNORECASE)
    backwardSearch = re.compile(''.join(keyRevRe), flags=re.IGNORECASE)

    revSql = sql[::-1]
    L = len(sql)

    exps = []

    for m in matches:
        end = L
        fTerm = forwardSearch.search(sql, m.span()[1])
        if fTerm:
            end = fTerm.span()[0]
        start = 0
        sTerm = backwardSearch.search(revSql, L - m.span()[0] + 1)
        if sTerm:
            start = L - sTerm.span()[0]
        exps.append(BooleanExpression(sql[start:end], start=start, end=end))

    return exps

