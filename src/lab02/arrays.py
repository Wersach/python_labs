def min_max(nums):
    """Возвращает кортеж (минимум, максимум). Пустой список вызывает ValueError."""
    if len(nums) == 0:
        raise ValueError("список пуст")
    minimum = nums[0]
    maximum = nums[0]
    for num in nums:
        if num < minimum:
            minimum = num
        if num > maximum:
            maximum = num
    return minimum, maximum

for nums in [[3, -1, 5, 5, 0], [42], [-5, -2, -9], [1.5, 2, 2.0, -3.1]]:
    print(nums, "->", min_max(nums))
try:
    min_max([])
except ValueError as e:
    print([], "-> ValueError:", e)

print()



def unique_sorted(nums):
    """Возвращает уникальные значения списка по возрастанию."""
    unique = []
    for num in nums:
        if num not in unique:
            unique.append(num)
    n = len(unique)
    i = 0
    while i < n:
        j = 0
        while j < n - i - 1:
            if unique[j] > unique[j + 1]:
                unique[j], unique[j + 1] = unique[j + 1], unique[j]
            j += 1
        i += 1
    return unique

for nums in [[3, 1, 2, 1, 3], [], [-1, -1, 0, 2, 2], [1.0, 1, 2.5, 2.5, 0]]:
    print(nums, "->", unique_sorted(nums))

print()



def flatten(mat):
    """Собирает список списков или кортежей в один список. Иначе TypeError."""
    result = []
    for row in mat:
        if type(row) != list and type(row) != tuple:
            raise TypeError("строка матрицы должна быть списком или кортежем")
        for x in row:
            result.append(x)
    return result

for mat in [[[1, 2], [3, 4]], [[1, 2], (3, 4, 5)], [[1], [], [2, 3]]]:
    print(mat, "->", flatten(mat))
try:
    flatten([[1, 2], "ab"])
except TypeError as e:
    print([[1, 2], "ab"], "-> TypeError:", e)