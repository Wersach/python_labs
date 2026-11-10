def bubble_sort(nums: list) -> list:
    """Новый список, отсортированный по возрастанию. Исходный не меняется.

    Если за проход не было ни одного обмена, список уже отсортирован
    и сортировка заканчивается раньше.

    bubble_sort([3, 1, 2]) -> [1, 2, 3]
    bubble_sort([2, 2, 1]) -> [1, 2, 2]
    bubble_sort([]) -> []
    """
    if type(nums) != list:
        raise TypeError("nums должен быть списком")
    a = list(nums)
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(nums: list) -> list:
    """Тот же контракт, что у bubble_sort.

    Берём очередной элемент и сдвигаем большие элементы слева
    на одну позицию вправо, пока не найдём ему место.
    """
    if type(nums) != list:
        raise TypeError("nums должен быть списком")
    a = list(nums)
    for i in range(1, len(a)):
        current = a[i]
        j = i - 1
        while j >= 0 and a[j] > current:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = current
    return a


def selection_sort(nums: list) -> list:
    """Тот же контракт, что у bubble_sort.

    Находим минимум оставшейся части и меняем его с первым элементом этой части.
    """
    if type(nums) != list:
        raise TypeError("nums должен быть списком")
    a = list(nums)
    n = len(a)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
    return a