import sys
from tableau import Tableau
from input_interpret import interpret

if __name__ == '__main__':
    n = len(sys.argv)
    if n < 2:
        print("Usage: python solution.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    obj, num_vars, unit_cost, constraints = interpret(filename)
    t = Tableau(obj, num_vars, unit_cost, constraints)
    k = t.solve()
    print(k[0])
    print(k[1])