# function to interpret the input file and return the objective function, number of variables, unit cost vector and constraints
def interpret(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

        # first line is the word "min" or "max", determining whether the objective function is to be minimized or maximized
        # followed by the number of variables
        obj, num_vars = lines[0].split()
        num_vars = int(num_vars)
        obj = 1 if obj.lower() == "min" else -1

        # the next line contains the unit cost vector, i.e. coefficients of the objective function
        unit_cost = list(map(float, lines[1].split()))

        # the next lines contain the constraints - can be equalitites or inequalities
        constraints = lines[2:]
        print(constraints)
        # each line contains the constant, followed by the type of constraint, followed by the coefficients of the variables
        for i in range(len(constraints)):
            constraint = constraints[i].strip().split()
            constraint[0] = float(constraint[0])
            constraint[2] = list(map(float, constraint[2:]))
            constraints[i] = constraint

        # the assumed constraints are that all variables are non-negative

        return obj, num_vars, unit_cost, constraints