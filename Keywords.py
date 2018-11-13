syntax = {'select', 'from', 'where', 'inner', 'outer', 'join', 'distinct',
          'having', 'group by', 'on'}

binary_op = {'or', 'and', 'not'}

# In array, not set as we need to check things like ~~ before ~ or <= before <
comparators = ['like', 'not like', '<=', '<>', '>=', '<', '>', '=', '!~~', '~~', '!~*', '~*', '!~', '~']

### These not needed as I am using sympy library

# def parse_value(x):
#     return float(x)
#
# operators = {
#     '+': lambda(x, y): parse_value(x) + parse_value(y),
#     '-': lambda(x, y): parse_value(x) - parse_value(y),
#     '/': lambda(x, y): parse_value(x) / parse_value(y),
#     '*': lambda(x, y): parse_value(x) * parse_value(y),
#     '%': lambda(x, y): parse_value(x) % parse_value(y)
# }
