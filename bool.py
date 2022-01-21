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
        self.parser = ParseEqlLess() ^ ParseBParen()

class ParseEqlLess(Parser):
    def __init__(self):
        self.parser = se.ParseExtrExpr() >> (lambda l:
                        (ParseSymbol("=") ^ ParseSymbol("<")) >> (lambda eqlless:
                                                                  se.ParseExtrExpr() >> (lambda r:
                        Return(Lesser(l, r)) if eqlless == "<" else Return(Equals(l, r)))))#
            
class ParseBParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol("(") >> (lambda _:
                      ParseBExpr()     >> (lambda e:
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
        self.left  = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))
    
class Or(Op2):
    op = "or"
    fun = lambda _, x, y: x or y

class And(Op2):
    op = "and"
    fun = lambda _, x, y: x and y
    
class Lesser(Op2):
    op = "<"
    fun = lambda _, x, y: x < y
    
class Equals(Op2):
    op = "="
    fun = lambda _, x, y: x == y    
    
