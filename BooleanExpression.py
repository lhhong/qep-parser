import Keywords
import itertools
import sympy

class Variable():

    def __init__(self, t):
        self.t = t

class StringVar(Variable):

    def __init__(self, val):
        self.val = val
        super().__init__('Str')

class Relation(Variable):

    def __init__(self, rel):
        self.parse(rel)
        super().__init__('Rel')

    def parse(self, rel):
        entities = rel.split('.')
        self.column = entities[-1]
        if len(entities) >= 2:
            self.alias = entities[-2]

class Expression():

    def __init__(self, exp, variables):
        self.parse(exp, variables)

    def parse(self, exp, variables):
        # Use sympy library to parse mathematical expression
        for v in self.variables:
            exec(v + ' = sympy.Symbol("' + v + '")')
        self.exp = eval('sympy.symplify(' + exp + ')')



class BooleanExpression():

    def __init__(self, string, start):
        self.string = string
        self.start = start
        self.end = start + len(string)
        self.nr = 0
        self.variables = {}
        self.rev_variables = {}
        self.var_gen = (chr(x) for x in intertools.count(start=97))

        self.parse_string(string)

    def parse_string(self, string):

        # Replaces strings with variables (Hack to escape keywords in string)
        strings = re.findall(r'\'[^\']*\'', string)
        for s in strings:
            a = next(self.var_gen)
            variables[a] = StringVar(s)
            rev_variables[s] = a
            re.sub(re.escape(s), "'" + a + "'", string)

        for c in Keywords.comparators:
            if c in string.lower():
                if c == 'like':
                    c = '~~'
                if c == 'not like':
                    c = '!~~'
                self.comparator = c

        args = [x.strip() for x in string.split(self.comparator)]

        self.left = self.parse_operand(a[0])
        self.right = self.parse_operand(a[1])

    def parse_operand(self, op):
        # Assumes string operands will not have other stuff
        if op.startswith("'") and op.endswith("'"):
            # String was replaced with variables
            return variables[op[1:-1]]

        # Finds table and column names in operand
        matches = re.findall(r'[a-zA-Z.]+', op)
        for m in matches:
            if m in self.rev_variables:
                a = self.rev_variables[m]
            else:
                a = next(self.var_gen)
                self.variables[a] = Relation(m)
                self.rev_variables[m] = a
            re.replace(re.escape(m), a, op)

        return Expression(op, self.variables)




