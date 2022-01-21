# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 15:56:10 2022

@author: mHiko(Amir)
"""

import bool
import se
import pcomb
import z3

"""
The first task is to implement classes for representing the combined arithmetical and boolean expressions.
Feel free to reuse code we implemented in the course

<expr> ::= <boolean_expression> | <arithm_expression>
"""

"""
Next, implement parsers for the expressions, using parser combinators.

Implement two functions, one for printing, the other for evaluating the parsed expressions in an environment:
def printExpr(inp):
def evalExpr(inp, env):

"""
"""
The following are examples of uses of these functions:
>>> Expr.printExpr("x = y")
(x = y)
>>> Expr.printExpr("x + 2 * y")
(x + (2 * y))
>>> Expr.printExpr("x < 2 and y < 1")
((x < 2) and (y < 1))
>>> Expr.printExpr("(x + 2*y < 15 + x * x) or z = 5")
(((x + (2 * y)) < (15 + (x * x))) or (z = 5))
>>> Expr.printExpr("x + 2*y < 15 + x * x or z = 5")
(((x + (2 * y)) < (15 + (x * x))) or (z = 5))
"""
"""
>>> env = {’x’:1, ’y’:2, ’z’:3}
>>> Expr.evalExpr("x = y", env)
False
>>> Expr.evalExpr("x + 2 * y", env)
5
>>> Expr.evalExpr("x < 2 and y < 1", env)
False
>>> Expr.evalExpr("(x + 2*y < 15 + x * x) or z = 5", env)
True
>>> Expr.evalExpr("x + 2*y < 15 + x * x or z = 5", env)
True
>>> Expr.evalExpr("x * 2 + 3 < x * (2 + 3)", env)
False
>>> Expr.evalExpr("y * 2 + 3 < y * (2 + 3)", env)
True
"""
class Expr:
    
    def printExpr(inp):
        prnt = se.ParseExpr().parse(inp)
        print(pcomb.result(prnt))
        pass
    
    def evalExpr(inp, env):
        pass
    
class BoolExpr:
    
    def printExpr(inp):
        pass
        
    def evalExpr(inp, env):
        pass
    
class ArithmExpr:
    
    def printExpr(inp):
        pass
    
    def evalExpr(inp, env):
        pass

