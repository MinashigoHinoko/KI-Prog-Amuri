# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 15:56:10 2022

@author: mHiko
"""
# Neccessary imports
import se
import pcomb
import z3


class Main():
    """
    This class makes the program more useable for everyone, as it has a user friendly input.

    Below is an example of how to use this class:
    -------
        >>> Main()
        >>> x + y +z = 10 (Insert problem: )
        >>> x < y         (Now Insert rule/s(type 'end' to stop): )
        >>> x < 3         (Now Insert rule/s(type 'end' to stop): )
        >>> 0 < x         (Now Insert rule/s(type 'end' to stop): )
        >>> end           (Now Insert rule/s(type 'end' to stop): )
            A Possible Solution is: {'z = 5', 'y = 3', 'x = 2'}

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


def printExpr(inp):
    """
    This function is for checking the print of an expression. 
    A print should show the mathematically correct way to write an expression down.

    Parameters
    ----------
    inp : String
        A mathematical string you want to have formated.

    Below is an example of how to use this function:
    -------
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


def evalExpr(inp, env):
    """
    This function is for evaluating an expression and the related variables to it, saved in env. 
    It gives an output (true or false) if the expression is bool.
    It can also output a result if it is arithmetic.

    Parameters
    ----------
    inp : String
        A mathmatical string you want to have evaluated.
    env : dictionary
        Some given numbers to make a calculation possible.

    Below is an example of how to use this function:
    -------
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


def solve(expr):
    """
    This function is for the actual solving of equations and inequations.
    Z3 is tasked with solving and the se.ParseExpr is handling the translation into z3.
    If there is a solution, the model gets formated correctly and if not,
    it outputs "No solution!" at the end.

    Parameters
    ----------
    expr : array
        This array is the problem we want to solve and is followed by rules the solution has to follow.
            ['Problem','rule','rule','rule',..., and so on]

    Returns
    -------
    models : Int
        The formated solution to the problem, which follows all rules.

    Below is an example of how to use this function:
    -------
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
    else:
        print("No solution!")