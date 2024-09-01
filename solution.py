import sys
import numpy as np
from input_interpret import interpret

class Tableau:

    def __init__(self, obj, num_vars, unit_cost, constraints):
        # self.obj describes whether the objective function is to be maximized or minimized (1 for min, -1 for max)
        self.obj = obj
        # self.num_vars is the number of variables in the problem (excluding slack variables)
        self.num_vars = num_vars
        # self.unit_cost is the unit cost vector, i.e. the coefficients of the objective function
        self.unit_cost = unit_cost
        # self.constraints is a list of constraints, each represented as a list of the form [constant, type, coefficients]
        self.constraints = constraints
        self.slack_vars = 0
        self.slack_var_counter = 0

        # count the number of slack variables needed
        for c in self.constraints:
            if c[1] == '<=' or c[1] == '>=':
                self.slack_vars += 1

        # self.constraint_matrix is the matrix representation of the simplex tableau
        self.constraint_matrix = np.zeros((len(self.constraints), self.num_vars + self.slack_vars + 1))
        for i in range(len(self.constraints)):
            # the coefficient vector is the list of coefficients of the constraint including slack variables and the constant
            print(self.constraints[i][2])
            coeff_vector = np.array(self.constraints[i][2])
            print(coeff_vector)
            # pad the coefficient vector with zeros to account for slack variables and the constant
            coeff_vector = np.pad(coeff_vector, (0, self.slack_vars + 1), 'constant', constant_values=(0))
            # add the constant to the end of the coefficient vector
            coeff_vector[self.num_vars + self.slack_vars] = self.constraints[i][0]

            # in case of <= inequality, add one slack variable to the coefficient vector
            if self.constraints[i][1] == '>=':
                coeff_vector[self.num_vars + self.slack_var_counter] = 1
                self.slack_var_counter += 1
            # in case of >= inequality, negate the coefficients and add one slack variable to the coefficient vector
            elif self.constraints[i][1] == '<=':
                coeff_vector = np.negative(coeff_vector)
                coeff_vector[self.num_vars + self.slack_var_counter] = 1
                self.slack_var_counter += 1

            self.constraint_matrix[i] = coeff_vector

        print(self.constraint_matrix)

if __name__ == '__main__':
    n = len(sys.argv)
    if n < 2:
        print("Usage: python solution.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    obj, num_vars, unit_cost, constraints = interpret(filename)
    print(obj)
    print(num_vars)
    print(unit_cost)
    print(constraints)
    t = Tableau(obj, num_vars, unit_cost, constraints)