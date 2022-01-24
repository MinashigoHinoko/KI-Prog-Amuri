"""
@author: Cezar Ionescu
@Editor: mHiko|Amir
"""


# Neccessary Imports
from pcomb import *
import se
import z3


class ParseBExpr(Parser):
    def __init__(self):
        self.parser = ParseOr() ^ ParseDisj()


class ParseDisj(Parser):
    def __init__(self):
        self.parser = ParseAnd() ^ ParseConj()


class ParseConj(Parser):
    def __init__(self):
        # Adjusted this so the Parser is also be able to work with = and < Symbols
        self.parser = ParseEqlLess() ^ ParseLesser()


class ParseEqlLess(Parser):
    def __init__(self):
        self.parser = ParseEqual() ^ ParseBParen()


class ParseEqual(Parser):
    def __init__(self):
        self.parser = se.ParseArithmExpr() >> (lambda d:
                                               (ParseSymbol("=") >> (lambda _:
                                                                     se.ParseArithmExpr() >> (lambda e:
                                                                                              Return(Equals(d, e))))))


class ParseLesser(Parser):
    def __init__(self):
        self.parser = se.ParseArithmExpr() >> (lambda d:
                                               (ParseSymbol("<") >> (lambda _:
                                                                     se.ParseArithmExpr() >> (lambda e:
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

    def toz3(self):
        return z3.Or(self.left.toz3(), self.right.toz3())


class And(Op2):
    op = "and"
    def fun(_, x, y): return x and y

    def toz3(self):
        return z3.And(self.left.toz3(), self.right.toz3())


class Lesser(Op2):
    op = "<"
    def fun(_, x, y): return x < y

    def toz3(self):
        return self.left.toz3() < self.right.toz3()


class Equals(Op2):
    op = "="
    def fun(_, x, y): return x == y

    def toz3(self):
        return self.left.toz3() == self.right.toz3()