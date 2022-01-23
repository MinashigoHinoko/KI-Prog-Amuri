# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 15:56:10 2022

@author: mHiko|Amir
"""
#Neccessary Imports
import se
import pcomb
import z3

#This makes the program more useable for everyone, as it has a user friendly input
class Main():
    """
    The following is an example of how to use this class:
    >>> Main()
    >>> x + y +z = 10 (Insert problem: )
    >>> x < y         (Now Insert rule/s(type 'end' to stop): )
    >>> x < 3         (Now Insert rule/s(type 'end' to stop): )
    >>> 0 < x         (Now Insert rule/s(type 'end' to stop): )
    >>> end           (Now Insert rule/s(type 'end' to stop): )

    A Possible Solution is: {'y = 2', 'x = 1', 'z = 7'}

    """

    def __init__(self):
        b = 0
        expr = [input("Insert problem: ")]
        while b < 1:
            rule = input("Now Insert rule/s(type 'end' to stop): ")
            if rule == 'end':
                b = 1
            else:
                expr.append(rule)
        sol = str(solve(expr))
        print("\n")
        print(f"A Possible Solution is: {sol}")
        print("\n")

#This is for checking the print of the Expressions, a print should show the mathematical correct way to write the Expression down
def printExpr(inp):
    """
    The following are examples of uses of these functions:
    >>> printExpr("x = y")
    (x = y)
    >>> printExpr("x + 2 * y")
    (x + (2 * y))
    >>> printExpr("x < 2 and y < 1")
    ((x < 2) and (y < 1))
    >>> printExpr("(x + 2*y < 15 + x * x) or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    >>> printExpr("x + 2*y < 15 + x * x or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    """
    prnt = se.ParseExpr().parse(inp)
    print(pcomb.result(prnt))

#This is for evaluating the the Expression and the relates variables to it, saved in env. Outputs either if the Expression is bool True or False or gives a result if possible 
def evalExpr(inp, env):
    """
    The following are examples of uses of these functions:
    >>> env = {'x':1, 'y':2, 'z':3}
    >>> evalExpr("x = y", env)
    False
    >>> evalExpr("x + 2 * y", env)
    5
    >>> evalExpr("x < 2 and y < 1", env)
    False
    >>> evalExpr("(x + 2*y < 15 + x * x) or z = 5", env)
    True
    >>> evalExpr("x + 2*y < 15 + x * x or z = 5", env)
    True
    >>> evalExpr("x * 2 + 3 < x * (2 + 3)", env)
    False
    >>> evalExpr("y * 2 + 3 < y * (2 + 3)", env)
    True
    """
    evl = se.ParseExpr().parse(inp)
    print(pcomb.result(evl).ev(env))

#This is for the actuall sovling of equations and inequations. z3 is tasked with solving and the ParseExpr is handling the translation into z3.
#At the end the model gets formated correctly if there is a Solution, if not it outputs "No Solution"
def solve(expr):
    """
    The following are examples of uses of these functions:
    >>> exprs = ["x + y +z = 10", "x < y", "x < 3", "0 < x"]
    >>> sol = solve(exprs)
    >>> sol
    {'x = 1', 'y = 2', 'z = 7'}
    """
    s = z3.Solver()
    for e in expr:
        s.add(pcomb.result(se.ParseExpr().parse(e)).toz3())
    checker = str(s.check())
    if checker == "sat":
        mdl = s.model()
        models = set()
        for helper in mdl:
            var = helper
            val = mdl[helper]
            models.add(f'{var} = {val}')
        return models
    elif checker == "unsat":
        print("No Solution!")
