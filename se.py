"""
@author: Cezar Ionescu
@Editor: mHiko|Amir
"""

# Neccessary Imports
import math
from pcomb import *
import bool
import z3

"""
The first task is to implement classes for representing the combined arithmetical and boolean expressions.
Feel free to reuse code we implemented in the course

<expr> ::= <boolean_expression> | <arithm_expression>
"""


class ParseExpr(Parser):
    def __init__(self):
        self.parser = bool.ParseBExpr() ^ ParseArithmExpr()


class ParseArithmExpr(Parser):
    def __init__(self):
        self.parser = ParsePlus() ^ ParseTerm()


class ParseTerm(Parser):
    def __init__(self):
        self.parser = ParseTimes() ^ ParseFactor()


class ParseFactor(Parser):
    def __init__(self):
        self.parser = ParseExpon()


class ParseExpon(Parser):
    def __init__(self):
        self.parser = ParseExp() ^ ParseAtom()


class ParseAtom(Parser):
    def __init__(self):
        self.parser = ParseCon() ^ ParseVar() ^ ParseParen()


class ParseCon(Parser):
    def __init__(self):
        self.parser = ParseInt() >> (lambda n:
                                     Return(Con(n)))


class ParseVar(Parser):
    def __init__(self):
        self.parser = ParseIdent() >> (lambda name:
                                       Return(Var(name)))


class ParseParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol('(') >> (lambda _:
                                           ParseArithmExpr() >> (lambda e:
                                                                 ParseSymbol(')') >> (lambda _:
                                                                                      Return(e))))


class ParsePlus(Parser):
    def __init__(self):
        self.parser = ParseTerm() >> (lambda t:
                                      ParseSymbol('+') >> (lambda _:
                                                           ParseArithmExpr() >> (lambda e:
                                                                                 Return(Plus(t, e)))))


class ParseTimes(Parser):
    def __init__(self):
        self.parser = ParseFactor() >> (lambda x:
                                        ParseSymbol('*') >> (lambda _:
                                                             ParseTerm() >> (lambda y:
                                                                             Return(Times(x, y)))))


class ParseExp(Parser):
    def __init__(self):
        self.parser = ParseSymbol("exp") >> (lambda _:
                                             ParseAtom() >> (lambda a:
                                                             Return(Exp(a))))


class Expr:
    pass


class Con(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)  # f"Con({self.val})"

    def ev(self, env):
        return self.val

    def toz3(self):
        return self.val


class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name  # f"Var({self.name})"

    def ev(self, env):
        return env[self.name]

    def toz3(self):
        return z3.Int(self.name)


class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))


class Plus(BinOp):
    name = "Plus"
    def fun(_, x, y): return x + y
    op = '+'

    def toz3(self):
        return self.left.toz3() + self.right.toz3()


class Times(BinOp):
    name = "Times"
    def fun(_, x, y): return x * y
    op = '*'

    def toz3(self):
        return self.left.toz3() * self.right.toz3()