"""
<bool> ::= <disj> or <bool> | <disj>
<disj> ::= <conj> and <disj> | <conj>
<conj> ::= <var> | ( <bool> )

P or (Q and R or P)
"""
from pcomb import *
import se


class ParseBExpr(Parser):
    def __init__(self):
        self.parser = ParseOr() ^ ParseDisj()


class ParseDisj(Parser):
    def __init__(self):
        self.parser = ParseAnd() ^ ParseConj()


class ParseConj(Parser):
    def __init__(self):
        self.parser = ParseEqlLess() ^ ParseLesser()

class ParseEqlLess(Parser):
    def __init__(self):
        self.parser = ParseEqual() ^ ParseBParen()

class ParseEqual(Parser):
    def __init__(self):
        self.parser = se.ParseExtrExpr() >> (lambda d:
                                             (ParseSymbol("=") >> (lambda _:
                                                                                       se.ParseExtrExpr() >> (lambda e:
                                                                                                              Return(Equals(d, e))))))
class ParseLesser(Parser):
    def __init__(self):
        self.parser = se.ParseExtrExpr() >> (lambda d:
                                             (ParseSymbol("<") >> (lambda _:
                                                                                       se.ParseExtrExpr() >> (lambda e:
                                                                                                              Return(Lesser(d, e))))))

class ParseBParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol("(") >> (lambda _:
                                           ParseBExpr() >> (lambda e:
                                                            ParseSymbol(")") >> (lambda _:
                                                                                 Return(e))))


class ParseOr(Parser):
    def __init__(self):
        self.parser = ParseDisj() >> (lambda d:
                                      ParseSymbol("or") >> (lambda _:
                                                            ParseBExpr() >> (lambda e:
                                                                             Return(Or(d, e)))))


class ParseAnd(Parser):
    def __init__(self):
        self.parser = ParseConj() >> (lambda x:
                                      ParseSymbol("and") >> (lambda _:
                                                             ParseDisj() >> (lambda y:
                                                                             Return(And(x, y)))))


class BExpr:
    pass


class BVar(BExpr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def ev(self, env):
        return env[self.name]


class Op2(BExpr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))


class Or(Op2):
    op = "or"
    def fun(_, x, y): return x or y


class And(Op2):
    op = "and"
    def fun(_, x, y): return x and y


class Lesser(Op2):
    op = "<"
    def fun(_, x, y): return x < y


class Equals(Op2):
    op = "="
    def fun(_, x, y): return x == y
