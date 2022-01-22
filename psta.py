# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 15:56:10 2022

@author: mHiko|Amir
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

class Main():
    """
    >>> Main()
    >>> x + y +z = 10 (Insert problem: )
    >>> x < y         (Now Insert rule/s(type 'end' to stop): )       
    >>> x < 3         (Now Insert rule/s(type 'end' to stop): )
    >>> 0 < x         (Now Insert rule/s(type 'end' to stop): )
    >>> end           (Now Insert rule/s(type 'end' to stop): )
    A Possible Solution is: {z = 7, y = 2, x = 1}
    """

    def __init__(self):
        b=0
        expr = [input("Insert problem: ")]
        while b < 1:
            rule= input("Now Insert rule/s(type 'end' to stop): ")
            if rule == 'end':
                b = 1
            else:
                expr.append(rule)
        sol= str(Z3Solver.solve(expr))
        sol= sol.replace("[","{")
        sol= sol.replace("]","}")
        print("\n")
        print(f"A Possible Solution is: {sol}")
        print("\n")
        

class Expr:

    def printExpr(inp):
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
        prnt = se.ParseExpr().parse(inp)
        print(pcomb.result(prnt))

    def evalExpr(inp, env):
        """
        >>> env = {'x':1, 'y':2, 'z':3}
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
        evl = se.ParseExpr().parse(inp)
        print(pcomb.result(evl).ev(env))

class Z3Solver:
    def solve(expr):
        s = z3.Solver()
        for e in expr:
            s.add(pcomb.result(se.ParseExpr().parse(e)).toz3())
        checker = str(s.check())
        if checker == "sat":
            return s.model()
        elif checker == "unsat":
            print("No Solution!")

