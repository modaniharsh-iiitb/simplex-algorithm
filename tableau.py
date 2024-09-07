import fractions
import numpy as np

import time

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

        self.build_tableau()

    def build_tableau(self):
        # count the number of slack variables needed
        for c in self.constraints:
            if c[1] == '<=' or c[1] == '>=':
                self.slack_vars += 1

        # self.constraint_matrix is the matrix representation of the simplex tableau
        self.constraint_matrix = np.zeros((len(self.constraints), self.num_vars + self.slack_vars + 1))
        for i in range(len(self.constraints)):
            # the coefficient vector is the list of coefficients of the constraint including slack variables and the constant
            coeff_vector = np.array(self.constraints[i][2])
            # pad the coefficient vector with zeros to account for slack variables and the constant
            coeff_vector = np.pad(coeff_vector, (0, self.slack_vars + 1), 'constant', constant_values=(0))
            # add the constant to the end of the coefficient vector
            coeff_vector[-1] = self.constraints[i][0]

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

        objective_row = np.pad((self.obj * np.array(self.unit_cost)), (0, self.slack_vars + 1), 'constant', constant_values=(0))
        self.constraint_matrix = np.vstack([self.constraint_matrix, objective_row])
        print(self.constraint_matrix)

    def pivot(self, a, b):
        self.constraint_matrix[b] /= self.constraint_matrix[b, a]
        for i in range(len(self.constraint_matrix)):
            if i == b:
                continue
            self.constraint_matrix[i] -= self.constraint_matrix[i, a] * self.constraint_matrix[b]

    def solve(self):
        # # check for infeasibility
        # if np.all(self.constraint_matrix[:-1, -1] >= 0): # this is NOT YET the correct boolean
        #     return ("INFEASIBLE", None)
        
        # # check for unboundedness
        # if np.all(self.constraint_matrix[-1, :-1] <= 0): # this is NOT YET the correct boolean
        #     return ("UNBOUNDED", None)

        while (True):
            # if all values in the last row are non-negative, the solution is optimal
            if np.all(self.constraint_matrix[-1] >= 0):
                break
            # the pivot column (corresponding to the entering variable) is the first negative value in the last row
            a = np.argwhere(self.constraint_matrix[-1] < 0)[0][0]
            print(a)
            # the pivot row (corresponding to the leaving variable) is the row with the smallest ratio of the constant to the pivot column, given that the pivot element is positive
            ratios = self.constraint_matrix[:-1, -1] / self.constraint_matrix[:-1, a]
            ratios = np.where(self.constraint_matrix[:-1, a] > 0, ratios, np.inf)
            b = np.argmin(ratios)
            print(b)
            self.pivot(a, b)
            print(self.constraint_matrix)

            time.sleep(1)

        return ("OPTIMAL", self.constraint_matrix[-1, -1])
