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

        # self.tableau is the tableau of the problem, which is built using the input parameters
        self.tableau = None

if __name__ == '__main__':
    n = len(sys.argv)
    if n < 2:
        print("Usage: python solution.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    obj, num_vars, unit_cost, constraints = interpret(filename)