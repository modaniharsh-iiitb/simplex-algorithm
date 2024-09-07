import fractions    

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
        # unit_cost = list(map(f, lines[1].split()))
        unit_cost = list(map(fractions.Fraction, lines[1].split()))

        # the next lines contain the constraints - can be equalitites or inequalities
        constraints = lines[2:]
        # each line contains the constant, followed by the type of constraint, followed by the coefficients of the variables

        act_constraints = []

        for constraint in constraints:
            constraint = constraint.strip().split()
            constant = fractions.Fraction(constraint[0])
            constraint_type = constraint[1]
            temp = [fractions.Fraction(0) for i in range(num_vars)]
            # 3 >= 2 2@1
            for i in range(2, len(constraint)):
                if('@' in constraint[i]):
                    temp[int(constraint[i].split('@')[1])-1] = fractions.Fraction(constraint[i].split('@')[0])
                else:
                    temp[i-2] = fractions.Fraction(constraint[i])
            act_constraints.append([constant, constraint_type, temp])


        # the assumed constraints are that all variables are non-negative
        print(obj, num_vars, unit_cost, act_constraints)
        return obj, num_vars, unit_cost, act_constraints
    
interpret('inp.csv')