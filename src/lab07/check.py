import random

from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort


def random_list(max_len: int = 50) -> list[int]:
    """Случайный список длиной от 0 до max_len, числа от -100 до 100, с повторами."""
    n = random.randint(0, max_len)
    nums = []
    for _ in range(n):
        nums.append(random.randint(-100, 100))
    return nums


def check_sorting(fn, trials: int = 100) -> None:
    """Сравнивает fn(nums) со sorted(nums) и проверяет, что исходный список не изменён."""
    cases = [[], [5], [2, 1], [1, 2], [2, 2, 1], [3, -1, 0, -1]]
    for _ in range(trials):
        cases.append(random_list())
    for nums in cases:
        original = list(nums)
        result = fn(nums)
        assert result == sorted(original), f"{fn.__name__} ошиблась на {original}: {result}"
        assert nums == original, f"{fn.__name__} изменила исходный список {original}"
    print(f"OK: {fn.__name__}, {len(cases)} проверок")


def check_search(trials: int = 100) -> None:
    """linear_search против list.index, binary_search на отсортированных списках."""
    count = 0
    for _ in range(trials):
        nums = random_list()
        if len(nums) > 0 and random.random() < 0.5:
            x = random.choice(nums)
        else:
            x = random.randint(-110, 110)

        try:
            expected = nums.index(x)
        except ValueError:
            expected = -1
        assert linear_search(nums, x) == expected, f"linear_search({nums}, {x})"

        s = sorted(nums)
        queries = [x]
        if len(s) > 0:
            queries.append(s[0])
            queries.append(s[-1])
        for q in queries:
            i = binary_search(s, q)
            if q in s:
                assert i != -1 and s[i] == q, f"binary_search({s}, {q}) -> {i}"
            else:
                assert i == -1, f"binary_search({s}, {q}) -> {i}, а должно быть -1"
            count += 1
        count += 1

    fixed = [([], 5, -1), ([5], 5, 0), ([5], 3, -1), ([1, 3], 2, -1), ([1, 3], 3, 1), ([1, 3], 5, -1)]
    for s, q, expected in fixed:
        assert binary_search(s, q) == expected, f"binary_search({s}, {q})"
        count += 1
    print(f"OK: поиск, {count} проверок")


def check_pair(nums: list, target: int, pair, name: str) -> None:
    """Проверяет, что pair это (i, j), i < j и nums[i] + nums[j] == target."""
    i, j = pair
    assert i < j, f"{name}: {pair}, а должно быть i < j"
    assert nums[i] + nums[j] == target, f"{name}({nums}, {target}) -> {pair}"


def check_two_sum(trials: int = 100) -> None:
    """Оба способа должны вернуть пару с нужной суммой или оба None."""
    for _ in range(trials):
        nums = random_list(30)
        if len(nums) >= 2 and random.random() < 0.5:
            i, j = random.sample(range(len(nums)), 2)
            target = nums[i] + nums[j]
        else:
            target = random.randint(-250, 250)

        slow = two_sum_brute(nums, target)
        fast = two_sum_fast(nums, target)
        if slow is None:
            assert fast is None, f"two_sum_fast({nums}, {target}) -> {fast}, а пары нет"
        else:
            assert fast is not None, f"two_sum_fast({nums}, {target}) -> None, а пара есть"
            check_pair(nums, target, slow, "two_sum_brute")
            check_pair(nums, target, fast, "two_sum_fast")
    print(f"OK: two_sum, {trials} проверок")


if __name__ == "__main__":
    random.seed(42)
    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn)
    check_search()
    check_two_sum()
    print("OK")