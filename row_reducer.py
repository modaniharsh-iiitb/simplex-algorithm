import tableau

# get the constraints from input file (from the main file)
# iterate through rows
# first row is the objective function; rest are constraints
# make a tableau
# solve the tableau
# if the tableau is infeasible or unbounded, the row is not to be removed
# if the tableau is optimal and the value of the optimized function satisfies the inequality that the objective function is made out of,
# then the row is to be removed
# otherwise it is not