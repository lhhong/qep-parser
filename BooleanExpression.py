import Keywords
import itertools
import sympy
import re

class Variable():

    def __init__(self, t):
        self.t = t

class CountVar(Variable):

    def __init__(self, rel):
        self.rel = rel
        super().__init__('Cnt')

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

    def __init__(self, exp, symbols):
        self.parse(exp, symbols)

    def parse(self, exp, symbols):

        # Use sympy library to parse mathematical expression
        for v in symbols:
            exec(v + ' = sympy.Symbol("' + v + '")')
        self.exp = eval('sympy.simplify(' + exp + ')')



class BooleanExpression():

    def __init__(self, string, start=0, end=0, variables=None, rev_variables=None):
        self.string = string
        self.start = start
        self.end = end
        self.nr = 0

        start = 97

        if variables:
            self.variables = variables
        else:
            self.variables = {}
        if rev_variables:
            self.rev_variables = rev_variables
            start = ord(max(rev_variables.values()))
        else:
            self.rev_variables = {}

        self.var_gen = (chr(x) for x in itertools.count(start=start))

        self.parse_string(string)

    def parse_string(self, string):

        # Replaces strings with variables (Hack to escape keywords in string)
        strings = re.findall(r'\'[^\']*\'', string)
        for s in strings:
            a = next(self.var_gen)
            self.variables[a] = StringVar(s)
            self.rev_variables[s] = a
            string = re.sub(re.escape(s), "'" + a + "'", string)

        for c in Keywords.comparators:
            if c in string.lower():
                splitter = c
                if c == 'like':
                    c = '~~'
                if c == 'not like':
                    c = '!~~'
                self.comparator = c
                # Needs to break to prevent multiple match
                break

        args = [x.strip() for x in string.lower().split(splitter)]

        self.left = self.parse_operand(args[0])
        self.right = self.parse_operand(args[1])

    def parse_operand(self, op):
        # Assumes string operands will not have other stuff
        if op.startswith("'") and op.endswith("'"):
            # String was replaced with variables
            return self.variables[op[1:-1]]

        # Finds table and column names in operand
        matches = re.findall(r'count\(.+\)', op, flags=re.IGNORECASE)

        for m in matches:
            if m in self.rev_variables:
                a = self.rev_variables[m]
            else:
                a = next(self.var_gen)
                self.variables[a] = CountVar(m)
                self.rev_variables[m] = a
            op = re.sub(re.escape(m), a, op, flags=re.IGNORECASE)

        matches = re.findall(r'[a-zA-Z.]+', op)
        for m in matches:
            if m in self.rev_variables:
                a = self.rev_variables[m]
            else:
                a = next(self.var_gen)
                self.variables[a] = Relation(m)
                self.rev_variables[m] = a
            op = re.sub(re.escape(m), a, op)

        return Expression(op, self.variables)




