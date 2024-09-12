def rref_no_swap(matrix):
    rows, cols = len(matrix), len(matrix[0])
    
    for r in range(rows):
        # find the first non-zero element in the row
        pivot = None
        for c in range(cols):
            if (matrix[r][c] != 0):
                pivot = c
                break
        
        # if there is no non-zero element in the row, skip
        if pivot is None:
            continue

        # divide the row by the pivot element
        matrix[r] = [matrix[r][c] / matrix[r][pivot] for c in range(cols)]

        # subtract the row from all other rows to make the other elements in the column zero
        for r2 in range(rows):
            if (r2 == r):
                continue
            factor = matrix[r2][pivot]
            matrix[r2] = [matrix[r2][c] - factor * matrix[r][c] for c in range(cols)]
    
    return matrix