def check_rect(mat):
    """Проверяет, что все строки одной длины. Иначе ValueError."""
    for row in mat:
        if len(row) != len(mat[0]):
            raise ValueError("матрица рваная")


def transpose(mat):
    """Меняет строки и столбцы местами. Рваная матрица вызывает ValueError."""
    check_rect(mat)
    if len(mat) == 0:
        return []
    result = []
    for col in range(len(mat[0])):
        new_row = []
        for row in mat:
            new_row.append(row[col])
        result.append(new_row)
    return result


def row_sums(mat):
    """Сумма по каждой строке. Рваная матрица вызывает ValueError."""
    check_rect(mat)
    sums = []
    for row in mat:
        total = 0
        for x in row:
            total += x
        sums.append(total)
    return sums


def col_sums(mat):
    """Сумма по каждому столбцу. Рваная матрица вызывает ValueError."""
    return row_sums(transpose(mat))


for mat in [[[1, 2, 3]], [[1], [2], [3]], [[1, 2], [3, 4]], []]:
    print(mat, "->", transpose(mat))
try:
    transpose([[1, 2], [3]])
except ValueError as e:
    print([[1, 2], [3]], "-> ValueError:", e)

print()

for mat in [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]]]:
    print(mat, "->", row_sums(mat))
try:
    row_sums([[1, 2], [3]])
except ValueError as e:
    print([[1, 2], [3]], "-> ValueError:", e)

print()

for mat in [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]]]:
    print(mat, "->", col_sums(mat))
try:
    col_sums([[1, 2], [3]])
except ValueError as e:
    print([[1, 2], [3]], "-> ValueError:", e)