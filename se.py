"""
>>> ParseExpr().parse("exp(x) + 2*y")
[(Plus(Exp(Var('x')), Times(Con(2), Var('y'))), '')]
"""

from pcomb import *

"""
<expr> ::= <term> + <expr> | <term>
<term> ::= <factor> * <term> | <factor>
<factor> ::= <expon>
<expon> ::= exp( <atom> ) | <atom>
<atom> ::= <con> | <var> | ( <expr> )
"""

class ParseExpr(Parser):
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
                      ParseExpr()      >> (lambda e:
                      ParseSymbol(')') >> (lambda _:
                      Return(e))))

class ParsePlus(Parser):
    def __init__(self):
        self.parser = ParseTerm()      >> (lambda t:
                      ParseSymbol('+') >> (lambda _:
                      ParseExpr()      >> (lambda e:
                      Return(Plus(t, e)))))

class ParseTimes(Parser):
    def __init__(self):
        self.parser = ParseFactor()    >> (lambda x:
                      ParseSymbol('*') >> (lambda _:
                      ParseTerm()      >> (lambda y:
                      Return(Times(x, y)))))

class ParseExp(Parser):
    def __init__(self):
        self.parser = ParseSymbol("exp") >> (lambda _:
                      ParseAtom()        >> (lambda a:
                      Return(Exp(a))))
        
class Expr:
    def __add__(self, other):
        return Plus(self, other)

    def __mul__(self, other):
        return Times(self, other)

    def diff(self, var):
        return "Error! diff not implemented"

class Con(Expr):
    def __init__(self, val):
        self.val = val
        
    def __str__(self):
        return str(self.val) # f"Con({self.val})"

    def ev(self, env):
        return self.val

    def diff(self, var):
        return Con(0)

    def simplify(self):
        return self

    def __eq__(self, other):
        if type(other).__name__ != "Con":
            return False
        return self.val == other.val
    
    def vars_(self):
        return []
    
class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name # f"Var({self.name})"

    def ev(self, env):
        return env[self.name]

    def diff(self, var):
        if self.name == var:
            return Con(1)
        else:
            return Con(0)

    def simplify(self):
        return self

    def __eq__(self, other):
        if type(other).__name__ != "Var":
            return False
        return self.name == other.name

    def vars_(self):
        return [self.name]
    
class BinOp(Expr):
    def __init__(self, left, right):
        self.left  = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})" # f"{self.name}({self.left}, {self.right})" # +

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))

    def __eq__(self, other):
        if not isinstance(other, BinOp):
            return False
        return self.name == other.name and self.left == other.left and self.right == other.right

    def vars_(self):
        return list(set(self.left.vars_() + self.right.vars_()))
    
    
class Plus(BinOp):
    name = "Plus"
    fun  = lambda _, x, y: x + y
    op   = '+'

    def diff(self, var):
        return self.left.diff(var) + self.right.diff(var)

    def simplify(self):
        simple_left  = self.left.simplify()
        simple_right = self.right.simplify()

        vl  = None
        vr = None
        if simple_left.vars_() == []:
            vl = simple_left.ev({})
        if simple_right.vars_() == []:
            vr = simple_right.ev({})

        if vl != None and vr != None:
            return Con(vl + vr)
        if vl == 0:
            return simple_right
        elif vr == 0:
            return simple_left
        else:
            return simple_left + simple_right
        
class Times(BinOp):
    name = "Times"
    fun  = lambda _, x, y: x * y
    op   = '*'

    def diff(self, var):
        return self.left.diff(var) * self.right + self.left * self.right.diff(var)

    def simplify(self):
        simple_left  = self.left.simplify()
        simple_right = self.right.simplify()
        vl  = None
        vr = None
        if simple_left.vars_() == []:
            vl = simple_left.ev({})
        if simple_right.vars_() == []:
            vr = simple_right.ev({})

        if vl != None and vr != None:
            return Con(vl * vr)
        if vl == 0 or vr == 0:
            return Con(0)
        elif vl == 1:
            return simple_right
        elif vr == 1:
            return simple_left
        else:
            return simple_left * simple_right
    
import math

class Exp(Expr):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return f"exp({self.arg})" # f"Exp({self.arg})"

    def ev(self, env):
        return math.exp(self.arg.ev(env))

    def diff(self, var):
        return Exp(self.arg) * self.arg.diff(var)

    def __eq__(self, other):
        if not isinstance(other, Exp):
            return False
        return self.arg == other.arg

    def simplify(self):
        simple_arg = self.arg.simplify()

        if simple_arg.vars_() == []:
            return Con(math.exp(simple_arg.ev({})))
        
        return Exp(simple_arg)

    def vars_(self):
        return self.arg.vars_()

def diff(string, var):
    res = ParseExpr().parse(string)
    if res != []:
       expr = result(res)
       return str(expr.diff(var).simplify())
   
    
if __name__ == "__main__":
     x = Var('x')
     y = Con(5)
     print(Times(x, Exp(Times(Con(3), Con(3)))).simplify())
     print(Times(Con(5), Plus(Con(3), Con(4))).simplify())
     print(Exp(Var("x") * (Var("y") + Con(5))).diff("x").simplify())
     print(Var("x") + Con(5) == Var("x") + Con(5))

