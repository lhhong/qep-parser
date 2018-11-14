from findExpressions import *
from BooleanExpression import BooleanExpression


def stripParenthesis(foo):
    foo = foo.replace("(", '')
    foo = foo.replace(")", '')
    foo = foo.replace('::text', '')
    return foo


def findMatchingBE(query, booleans, cond):
    for b in booleans:
        be = BooleanExpression(cond, variables=b.variables, rev_variables=b.rev_variables)
        if isEquivalentBooleanExpression(be, b):
            return b.start, b.end, query[b.start:b.end]
    return -1, -1, ""


def reverseComparatorIfNeeded(comparator):
    if comparator == '<':
        return '>'
    elif comparator == '<=':
        return '>='
    return comparator


def isEquivalentBooleanExpression(a,b):
    if not hasattr(a.right, 'exp'):
        if hasattr(a.right, 'val') and hasattr(b.right, 'val'):
            return a.left.exp==b.left.exp and a.right.val==b.right.val
    elif a.left.exp==b.left.exp and a.right.exp==b.right.exp:
        return a.comparator==b.comparator
    elif a.left.exp==b.right.exp and a.right.exp==b.left.exp:
        return a.comparator==reverseComparatorIfNeeded(b.comparator)
    
    return False


def getMatchingClause(query, search_key):
    start = query.find(search_key)
    if start == -1:
        return start
    shortened_query = query[start+len(search_key)+1:]
    parts = shortened_query.split(' ') 
    return search_key + ' ' + parts[0]


def correlateQuery(all_nodes, query):
    
    # Change query to a list of Boolean expressions
    query = query.lower()
    booleans = findExpressions(query)
    
    for node in all_nodes:
        #print(node.title)
        s = -1
        e = -1
        if 'Join' in node.title:
            # Find hash condition as boolean expression
            cond = stripParenthesis(node.description_dict['Hash Cond'])
            s, e, match = findMatchingBE(query, booleans, cond)
            #print('Join:', cond, 'Matched: ', match)
            
        elif 'Scan' in node.title:
            # Find relation name
            clause = " ".join([node.description_dict['Relation Name'], node.description_dict['Alias']])
            s, e, match = findClauseStartEnd(query, clause.lower())
            #print('Scan:', clause, 'Matched: ', match)
            if 'Filter' in node.description_dict:
                # Find filter condition as boolean expression
                cond = stripParenthesis(node.description_dict['Filter'])
                s, e, match = findMatchingBE(query, booleans, cond)
                #print('Filter:', cond, 'Matched: ', match)
                
        elif 'Aggregate' in node.title:
            # Find GROUP BY
            clause = getMatchingClause(query, 'group by')
            s, e, match = findClauseStartEnd(query, clause)
            #print('Aggregate:', 'Matched: ', match)
        
        elif 'Sort' in node.title:
            clause = getMatchingClause(query, 'order by')
            s, e, match = findClauseStartEnd(query, clause)
            #print('Sort:', 'Matched: ', match)
        
        elif 'Limit' in node.title:
            clause = getMatchingClause(query, 'limit')
            s, e, match = findClauseStartEnd(query, clause)
            #print('Limit:', 'Matched: ', match)
            
        node.description_dict['StartOfQuery'] = s
        node.description_dict['EndOfQuery'] = e
