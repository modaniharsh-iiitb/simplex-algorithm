import sys
from tableau import Tableau
from input_interpret import interpret
from row_reducer import rref_no_swap

if __name__ == '__main__':
    n = len(sys.argv)
    if (n < 2):
        print("Usage: python solution.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    obj, num_vars, unit_cost, constraints = interpret(filename)
    
    invmap = {'>=': '<=', '<=': '>=', '=': '='}

    ss = "\nInitial Constraints are: \n"
    for c in constraints:
        for i in range(len(c[2])):
            if (i != 0):
                if (c[2][i] < 0):
                    ss += ' - ' + str(-c[2][i]) + 'x' + str(i+1)
                elif (c[2][i] == 1):
                    ss += ' + ' + 'x' + str(i+1)
                elif (c[2][i] == 0):
                    continue
                else:
                    ss += ' + ' + str(c[2][i]) + 'x' + str(i+1)
            else:
                if (c[2][i] < 0):
                    ss += ' - ' + str(-c[2][i]) + 'x' + str(i+1)
                elif (c[2][i] == 1):
                    ss += 'x' + str(i+1)
                elif (c[2][i] == 0):
                    continue
                else:
                    ss += str(c[2][i]) + 'x' + str(i+1)
        ss += ' ' + invmap[c[1]] + ' ' + str(c[0]) + '\n'

    print(ss)

    m = []
    ind = []

    for i in range(len(constraints)):
        if(constraints[i][1] == '='):
            ind.append(i)
            m.append(constraints[i][2]+[constraints[i][0]])

    m = rref_no_swap(m)
    rem_constraints = []
    for i in range(len(m)):
        #if the row is all zeros
        if all([x == 0 for x in m[i]]):
            rem_constraints.append(ind[i])
    
    s = "Constraints removed: \n"
    for i in rem_constraints:
        c = constraints[i]
        for i in range(len(c[2])):
            if (i != 0):
                if (c[2][i] < 0):
                    s += ' - ' + str(-c[2][i]) + 'x' + str(i+1)
                elif (c[2][i] == 1):
                    s += ' + ' + 'x' + str(i+1)
                elif (c[2][i] == 0):
                    continue
                else:
                    s += ' + ' + str(c[2][i]) + 'x' + str(i+1)
            else:
                if (c[2][i] < 0):
                    s += ' - ' + str(-c[2][i]) + 'x' + str(i+1)
                elif (c[2][i] == 1):
                    s += 'x' + str(i+1)
                elif (c[2][i] == 0):
                    continue
                else:
                    s += str(c[2][i]) + 'x' + str(i+1)
        s += ' ' + '=' + ' ' + str(c[0]) + '\n'
    
    #printing the removed constraints
    print(s)

    for i in rem_constraints:
        constraints[i] = None

    constraints = [x for x in constraints if x is not None]


    t = Tableau(obj, num_vars, unit_cost, constraints)
    k = t.solve()
    print(k[0])
    if k[0] == "OPTIMAL":
        print(k[2])
        print('FINAL SOLUTION:', k[3], '=', k[1])