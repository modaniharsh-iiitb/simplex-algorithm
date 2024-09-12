# simplex-algorithm
A program written in Python that implements the simplex algorithm of solving linear programming problems.

## Theory behind linear programming

**Linear programming** is the optimization (i.e. minimization or maximization) of a linear function

```
f(x) = u.T * x
```

given constraints of the form

```
Ax = b
x >= 0
```

where `u` and `x` are `d`-dimensional vectors, `b` is a `c`-dimensional vector and `A` is a matrix of dimension `c * d`.

We can note that since `x` is a `d`-dimensional vector, any one equation from the matrix `Ax = b` can be described as

```
a_i.T * x = b_i
```

where `a_i` is the `i`th row of `A` and `b_i` is the `i`th component of `b` (i.e. a scalar). It is easy to see that this describes a hyperplane in the given dimensional space.

Thus, the **feasibility polytope** (the region where the constraints are all satisfied) is formed with each constraint equation as a **supporting hyperplane** (specifically, a facet) of the polytope.

### Basic and feasible solutions

Given the constraints

```
Ax = b
x >= 0
```

if we can find an `x` that satisfies the same, it is called a **feasible solution**.

Now, suppose we row-reduce the given matrix `[A b]`. Then, assuming `c < d`, we get

```
[I, N]x = h
x >= 0
```

Where

- `I` is the `c x c` identity matrix (whose columns need not be right next to each other - they can be interspersed throughout the matrix)
- `N` is a `c x (d - c)` matrix
- `h` is a `c`-dimensional vector

If we further separate `x` into the vectors `x_B` and `x_N` corresponding to the columns of `A` which are in `I` and `N` respectively, we get

```
[I, N][x_B] = h
      [x_N]
x_B, x_N >= 0
```

or

```
(I * x_B) + (N * x_N) = h
=> x_B = h - N * x_N
x_B, x_N >= 0
```

A very simple way to obtain the solution of the newly formulated problem is

```
x_B = b, x_N = 0
```

This is known as a **basic solution**. For the same to be a feasible solution, we must have `b >= 0`.

If a solution is both basic and feasible, then the same is known as a **Basic Feasible Solution**.

It can be proved that the basic feasible solutions for any set of constraints can be found at the vertex of the feasibility polytope formed with the same set of constraints in the form of supporting hyperplanes.

### Optimizing a BFS - the simplex method

We can prove that the maximization or minimization of each linear function of `x` can be found at a supporting hyperplane parallel to the same function.

The intersection of any supporting hyperplane of a polytope and the polytope itself is a face of the polytope, and each face of a polytope must be a superset of a vertex of a polytope (i.e. a face with dimension 0).

This means that the optimum of any linear function of `x` must also occur at some vertex of the polytope, i.e. a **BFS** to the same constraint equation `Ax = b, x >= 0`.

The **simplex method** of optimization utilizes the fact that the optimum of any function must occur at a BFS, and iterates through the possible BFSs by changing one variable at a time, in such a manner that the objective function is pushed further towards its optimum in each iteration of changing the basis variables.

It does so by employing a **tableau**, which is a data structure used to solve linear programming problems by arranging all relevant values in a manner that facilitates swapping basic variables and evaluating the objective function at every single iteration.

### Converting inequalities - adding slack variables

We will not always be given constraints of the form

```
a_i.T * x = b_i
```

Sometimes, the constraints may be of `>=` and `<=` forms. For `<=` inequalities, we can add a nonzero quantity `s_i` such that

```
[a_i.T 1][ x ] = b_i
         [s_i]
```

Here, `s_i` is called a **slack variable**. Since it is not present in the objective function at all, it does not affect the optimization of the objective.

Similarly, for `>=` problems we can re-write the condition as

```
[a_i.T -1][ x ] = b_i
          [s_i]
```

## Implementation

The implementation of the same is described in detail in the comments.

## Running the program

No external libraries were required in the making of this project.

To clone the repository, run

```
git clone https://github.com/modaniharsh-iiitb/simplex-algorithm.git
```

Then, navigate to the `simplex-algorithm` folder and run

```
python main.py <filename>
```

where `<filename>` is the name of your input file.

### Input format

The `inp.csv` file is provided as a template as well for the same. The format of the input is as follows:

```
<problem> <num_vars>
<unit_cost_vector>
<constant> <op> <coefficients>
...
...
```

- `<problem>`: `MIN` or `MAX`. Signifies whether the problem is a minimization or a maximization problem.
- `<num_vars>`: the number of variables required, does not include the number of slack or artificial variables added. Must be an `int`.
- `<unit_cost_vector>`: space-separated `float` values that determine the objective function.
- `constraint`: defines each constraint `b_i <op> a_i.T * x` in the problem. Is split into three components - 
- `<constant>`: signifies `b_i` in the matrix. Must be a `float`.
- `<op>`: `<=`, `>=`, or `=`. Signifies the nature of the constraint.
- `<coefficients>`: space-separated `float` values that signify `a_i`.

**Note:** both `<unit_cost_vector>` and `<coefficients>` can be positionally as well as explicitly indexed, using the `@` symbol. For example, `k@i` would indicate that `k` is the `i`th component, 1-indexed.

## Contributors
- Dhruv Kothari (IMT2022114)
- Harsh Modani (IMT2022055)