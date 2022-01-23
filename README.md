# Solving Systems of Equations and Inequations
KI Programmierung PStA by Amir Amuri Alnasag Matr-nummer: 00818023

This programm can be used to solve systems of Equations and Inequations with the help of z3. And also to calculate simple expressions while respecting basic math rules.

Not working is the "greater than" sign(>) because the "lesser than" sign(<) makes it obsolete if correclty used.


It can parse the text of your input and transform it into the language of z3 with the solve function.
z3 will find a possible solution and returns it, if there is one.
One way this can be tested is written inside the solve function as a comment.

Another way to use this programm is via calling the Main class, this automatically ask you what the problem is and if there are any rules for it.
One way this can be tested is written inside the solve function as a comment.

As requested by the Task, I have also implemented printExpr and evalExpr, one prints the Expression you type in in a mathematical correct format and the other evaluates if the problem has a Solution with the given Variables.
One way this can be tested is written inside the solve function as a comment.
