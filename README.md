# Solving Systems of Equations and Inequations
KI Programmierung PStA by Matr-nummer: 00818023

This program can be used to solve systems of equations and inequations with the help of z3. It is also able to calculate simple expressions while respecting basic math rules.

The "greater than" sign(>) is not implemented, since the "lesser than" sign(<) makes it obsolete if used correctly. 
Overall, this code has been specifically tuned to the uses stated in the docstrings.


It can parse the text of your input and transform it into the language of z3 with the help of the solve function.
Z3 will find a possible solution - if there is one - and returns it.
See the docstring of the solve function for more details.

Another way to use this programm is by calling the Main class: Its function automatically asks you for the (in)equation and if there are any rules for it.
See the docstring of the Main class for more details.

I have also implemented printExpr and evalExpr, as requested by the task. 
The first one prints the expression you type in in a mathematically correct format and the other one evaluates if the problem is solvable with the given variables.
See the docstring of the printExpr and evalExpr function for more details.


PLEASE NOTE:	This program is only usable if you have installed the z3, z3-Solver package and every file in the zip, which should be collected in the same folder.
				The main code is written down in psta.py. The other files are for assisting and formatting the code (aka they are adjusted libraries).