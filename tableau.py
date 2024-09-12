from fractions import Fraction

class Tableau:

    OPTIMIZE_SUCCESS = 0
    OPTIMIZE_UNBOUNDED = 1

    def __init__(self, obj: int, num_vars: list, unit_cost: list, constraints: list):
        # self.obj describes whether the objective function is to be maximized or minimized (1 for min, -1 for max)
        self.obj = obj
        # self.num_vars is the number of variables in the problem (excluding slack variables)
        self.num_vars = num_vars
        # self.unit_cost is the unit cost vector, i.e. the coefficients of the objective function
        self.unit_cost = unit_cost
        # self.constraints is a list of constraints, each represented as a list of the form [constant, type, coefficients]
        self.constraints = constraints
        # self.slack_vars is the number of slack variables needed to convert the constraints to standard form
        self.slack_vars = 0
        # self.art_vars is the number of artificial variables needed to check the feasibility of the problem
        self.art_vars = 0
        self.slack_var_counter = 0
        self.art_var_counter = 0

        # number of variables in string form
        self.num_vars_str = 'Number of variables: ' + str(self.num_vars)

        self.build_tableau()

    def build_tableau(self):
        # here, the inequalities are inverted because the input is given in the format h op g, where op is the operator
        # whereas the standard form is g op h

        # count the number of slack variables needed
        for c in self.constraints:
            if c[1] == '<=' or c[1] == '>=':
                self.slack_vars += 1
            if c[1] == '<=' or c[1] == '=':
                self.art_vars += 1

        # list of variable names
        self.variable_names = []
        for i in range(self.num_vars):
            self.variable_names.append('x' + str(i+1))
        for i in range(self.slack_vars):
            self.variable_names.append('s' + str(i+1))
        for i in range(self.art_vars):
            self.variable_names.append('a' + str(i+1))
        # objective function in string form
        self.obj_str = ''
        for i in range(len(self.unit_cost)):
            if (i != 0):
                if (self.unit_cost[i] < 0):
                    self.obj_str += ' - ' + str(-self.unit_cost[i]) + self.variable_names[i]
                elif (self.unit_cost[i] == 1):
                    self.obj_str += ' + ' + self.variable_names[i]
                elif (self.unit_cost[i] == 0):
                    continue
                else:
                    self.obj_str += ' + ' + str(self.unit_cost[i]) + self.variable_names[i]
            else:
                if (self.unit_cost[i] < 0):
                    self.obj_str += ' - ' + str(-self.unit_cost[i]) + self.variable_names[i]
                elif (self.unit_cost[i] == 1):
                    self.obj_str += self.variable_names[i]
                elif (self.unit_cost[i] == 0):
                    continue
                else:
                    self.obj_str += str(self.unit_cost[i]) + self.variable_names[i]
        self.obj_fun_str = 'Objective : ' + ('Minimize ' if self.obj == 1 else 'Maximize ') + self.obj_str
        # invert_map is a dictionary to invert the inequality operators
        invert_map = {
            '<=': '>=',
            '>=': '<=',
            '=': '='
        }
        # constrains in string form
        self.constraints_str = 'Constraints:\n'
        for c in self.constraints:
            for i in range(len(c[2])):
                if (i != 0):
                    if (c[2][i] < 0):
                        self.constraints_str += ' - ' + str(-c[2][i]) + self.variable_names[i]
                    elif (c[2][i] == 1):
                        self.constraints_str += ' + ' + self.variable_names[i]
                    elif (c[2][i] == 0):
                        continue
                    else:
                        self.constraints_str += ' + ' + str(c[2][i]) + self.variable_names[i]
                else:
                    if (c[2][i] < 0):
                        self.constraints_str += ' - ' + str(-c[2][i]) + self.variable_names[i]
                    elif (c[2][i] == 1):
                        self.constraints_str += self.variable_names[i]
                    elif (c[2][i] == 0):
                        continue
                    else:
                        self.constraints_str += str(c[2][i]) + self.variable_names[i]
            self.constraints_str += ' ' + invert_map[c[1]] + ' ' + str(c[0]) + '\n'
        
        print(self.num_vars_str)
        print(self.obj_fun_str)
        print()
        print(self.constraints_str)
        print('========================================')

        # self.art_rows is the rows where the artificial variables are present
        self.art_rows = []

        # self.constraint_matrix is the matrix representation of the simplex tableau
        self.constraint_matrix = [[Fraction(0, 1) for _ in range(self.num_vars + self.slack_vars + self.art_vars + 1)] for _ in range(len(self.constraints) + 1)]
        for i in range(len(self.constraints)):
            # the coefficient vector is the list of coefficients of the constraint including slack variables and the constant
            coeff_vector = self.constraints[i][2]
            # pad the coefficient vector with zeros to account for slack variables, artificial variables and the constant
            coeff_vector.extend([0 for _ in range(self.slack_vars + self.art_vars + 1)])
            # add the constant to the end of the coefficient vector
            coeff_vector[-1] = self.constraints[i][0]

            # in case of >= inequality, add one slack variable and one artificial variable to the coefficient vector
            if self.constraints[i][1] == '<=':
                coeff_vector[self.num_vars + self.slack_var_counter] = -1
                coeff_vector[self.num_vars + self.slack_vars + self.art_var_counter] = 1
                self.art_rows.append(i)
                self.slack_var_counter += 1
                self.art_var_counter += 1
            # in case of <= inequality, negate the coefficients and add one slack variable to the coefficient vector
            elif self.constraints[i][1] == '>=':
                coeff_vector[self.num_vars + self.slack_var_counter] = 1
                self.slack_var_counter += 1
            # in case of equality, add one artificial variable to the coefficient vector
            elif self.constraints[i][1] == '=':
                coeff_vector[self.num_vars + self.slack_vars + self.art_var_counter] = 1
                self.art_var_counter += 1
                self.art_rows.append(i)

            self.constraint_matrix[i] = coeff_vector

        # the last row of the tableau is the unit cost vector - which, for the feasibility check,
        # is the negative of the sum of the artificial variables
        initial_objective = [Fraction(0) for _ in range(self.num_vars + self.slack_vars)] + [Fraction(-1) for _ in range(self.art_vars)] + [Fraction(0)]
        self.constraint_matrix[-1] = initial_objective

        # self.basic_vars is the list of basic variables in the tableau
        self.basic_vars = [0 for _ in range(len(self.constraint_matrix) - 1)]

    def remove_artificial_vars(self):
        for i in range(len(self.constraint_matrix)):
            length = len(self.constraint_matrix[i])
            while length > self.num_vars + self.slack_vars + 1:
                # for each row in the matrix, delete the columns starting from the d + s + 1th column
                # where d and s are the number of variables and slack variables respectively;
                # do this until there are no more artificial variables left (i.e. until the length of the row is d + s + 1)
                del self.constraint_matrix[i][self.num_vars + self.slack_vars]
                length -= 1

    def solve(self):
        # setting the basic variables of the tableau for the artificial variables
        art_var_counter = self.num_vars + self.slack_vars
        slack_var_counter = self.num_vars
        for i in self.art_rows:
            self.constraint_matrix[-1] = [self.constraint_matrix[-1][j] + self.constraint_matrix[i][j] for j in range(len(self.constraint_matrix[i]))]
            self.basic_vars[i] = art_var_counter
            art_var_counter += 1
        for i in range(len(self.basic_vars)):
            if (self.basic_vars[i] == 0):
                self.basic_vars[i] = slack_var_counter
            if (self.constraints[i][1] != '='):
                slack_var_counter += 1

        # rermove later
        print('Tableau after setting basic variables for artificial variables:')
        self.print_tableau()
        print('Basic variables:', self.basic_vars)
        print()
        
        # initially, run the optimization over the artificial variables
        r = self.optimize(op = 1)
        if (r == self.OPTIMIZE_UNBOUNDED):
            return ('UNBOUNDED', None, None)
        
        # check for infeasibility
        for i in self.basic_vars:
            if i >= self.num_vars + self.slack_vars:
                return ('INFEASIBLE', None, None)
            
        # remove the artificial variables from the tableau
        self.remove_artificial_vars()

        # once we are done checking for infeasibility, we can start optimizing the objective function
        # so we update the actual objective function into the last row of the tableau
        # (the basic variables carry over from the previous optimization)
        self.constraint_matrix[-1] = [-c for c in self.unit_cost] + [0 for _ in range(self.slack_vars + 1)]

        # remove later
        print('Tableau after removing artificial variables and updating objective function:')
        self.print_tableau()
        print('Basic variables:', self.basic_vars)
        print()
        
        # run the optimization over the objective function
        r = self.optimize(op = self.obj)

        # if the optimization is unbounded, return 'UNBOUNDED'
        if (r == self.OPTIMIZE_UNBOUNDED):
            return ('UNBOUNDED', None, None)

        solution_string = ['' for _ in range(self.num_vars)]
        solution_string = 'Values of variables:\n'
        for i in range(self.num_vars):
            if i in self.basic_vars:
                solution_string += 'x' + str(i+1) + ' = ' + str(self.constraint_matrix[self.basic_vars.index(i)][-1]) + '\n'
            else:
                solution_string += 'x' + str(i+1) + ' = 0\n'
        # if the optimization is successful, return 'OPTIMAL', the optimal value and the optimal solution
        return ('OPTIMAL', self.constraint_matrix[-1][-1], solution_string, self.obj_str)

    def find_leaving_var(self, entering_var):
        min_ratio = float('inf')
        leaving_var = -1
        for i in range(len(self.constraint_matrix) - 1):
            if (self.constraint_matrix[i][entering_var] > 0):
                ratio = self.constraint_matrix[i][-1] / self.constraint_matrix[i][entering_var]
                if (ratio < min_ratio):
                    min_ratio = ratio
                    leaving_var = i
        if (min_ratio == float('inf')):
            return -1
        return leaving_var
    
    def optimize(self, op):
        # remove later
        print('Optimizing for', 'min' if op == 1 else 'max', 'with the tableau:')
        self.print_tableau()
        print('Basic variables:', self.basic_vars)
        print()

        # if any of the basis vectors have nonzero cost coefficients, make them 0 by subtracting the constraint row multiplied by the cost coefficient
        for row, col in enumerate(self.basic_vars):
            if (self.constraint_matrix[-1][col] != 0):
                self.constraint_matrix[-1] = [self.constraint_matrix[-1][j] - self.constraint_matrix[row][j]*self.constraint_matrix[-1][col] for j in range(len(self.constraint_matrix[row]))]
        
        # find the entering variable
        l = self.constraint_matrix[-1][:-1]
        entering_var = self.constraint_matrix[-1].index(max(l) if op == 1 else min(l))

        # remove later
        iter = 1

        while (op * self.constraint_matrix[-1][entering_var] > 0):
            # remove later
            print('Iteration', iter)
            iter += 1

            leaving_var = self.find_leaving_var(entering_var)
            if (leaving_var == -1):
                return self.OPTIMIZE_UNBOUNDED
            print(entering_var, leaving_var)
            self.basic_vars[leaving_var] = entering_var
            self.constraint_matrix[leaving_var] = [self.constraint_matrix[leaving_var][j] / self.constraint_matrix[leaving_var][entering_var] for j in range(len(self.constraint_matrix[0]))]

            # make the column containing the entering variable a unit vector
            for i in range(len(self.constraint_matrix)):
                if (i != leaving_var):
                    self.constraint_matrix[i] = [self.constraint_matrix[i][j] - self.constraint_matrix[leaving_var][j] * self.constraint_matrix[i][entering_var] for j in range(len(self.constraint_matrix[0]))]

            # remove later
            print('Tableau after iteration:')
            self.print_tableau()
            print('Basic variables:', self.basic_vars)
            print()
            
            # find the entering variable for the next iteration
            l = self.constraint_matrix[-1][:-1]
            entering_var = self.constraint_matrix[-1].index(max(l) if op == 1 else min(l))
        
        # remove later
        print('Optimization successful, obtained the tableau:')
        self.print_tableau()
        print('Basic variables:', self.basic_vars)
        print()
        return self.OPTIMIZE_SUCCESS

    def print_tableau(self):
        s = [[str(e) for e in row] for row in self.constraint_matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))