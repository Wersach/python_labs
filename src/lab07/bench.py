import random
import timeit

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

SLOW_LIMIT = 100_000
SLOW_SORTS = [bubble_sort, insertion_sort, selection_sort]


def measure(fn, number: int = 1, repeat: int = 3) -> float:
    """Лучшее время одного запуска fn в секундах (минимум из repeat повторов)."""
    times = timeit.repeat(fn, number=number, repeat=repeat)
    return round(min(times) / number, 6)


def bench_sorts(n: int) -> list[tuple]:
    """Свои сортировки и sorted на одних и тех же n случайных числах."""
    data = []
    for _ in range(n):
        data.append(random.randint(-1_000_000, 1_000_000))
    expected = sorted(data)

    rows = [("sort", n, "sorted", measure(lambda: sorted(data), number=10, repeat=5))]
    for fn in SLOW_SORTS:
        if n >= SLOW_LIMIT:
            rows.append(("sort", n, fn.__name__, "> 60"))
            continue
        assert fn(data) == expected, f"{fn.__name__} сортирует неверно"
        rows.append(("sort", n, fn.__name__, measure(lambda: fn(data))))
    return rows


def bench_search(n: int = 100_000, queries_count: int = 10_000) -> list[tuple]:
    """10 000 запросов к списку из 100 000: линейный поиск против сортировки и бинарного."""
    data = []
    for _ in range(n):
        data.append(random.randint(0, 1_000_000))
    queries = []
    for _ in range(queries_count):
        if random.random() < 0.5:
            queries.append(random.choice(data))
        else:
            queries.append(random.randint(0, 1_000_000))
    sorted_data = sorted(data)

    def run_linear():
        for q in queries:
            linear_search(data, q)

    def run_binary():
        for q in queries:
            binary_search(sorted_data, q)

    return [
        ("search", n, "linear_search", measure(run_linear, repeat=1)),
        ("search", n, "sorted (подготовка)", measure(lambda: sorted(data), number=10, repeat=5)),
        ("search", n, "binary_search", measure(run_binary, repeat=5)),
    ]


def bench_two_sum(n: int) -> list[tuple]:
    """Оба two_sum, нужная пара стоит в самом конце списка."""
    nums = []
    for _ in range(n):
        nums.append(random.randint(0, 1_000_000_000))
    target = nums[-2] + nums[-1]
    assert two_sum_brute(nums, target) is not None
    return [
        ("two_sum", n, "two_sum_brute", measure(lambda: two_sum_brute(nums, target))),
        ("two_sum", n, "two_sum_fast", measure(lambda: two_sum_fast(nums, target), number=10, repeat=5)),
    ]


def format_seconds(value) -> str:
    """Время для таблицы: число с шестью знаками или строка как есть."""
    if type(value) == str:
        return value + " с"
    return f"{value:.6f} с"


def print_table(rows: list[tuple]) -> None:
    """Печатает замеры таблицей с выровненными колонками."""
    task, n, impl, seconds = "task", "n", "impl", "seconds"
    print(f"{task:<8} {n:>8}  {impl:<22} {seconds:>14}")
    print("-" * 56)
    for task, n, impl, seconds in rows:
        print(f"{task:<8} {n:>8}  {impl:<22} {format_seconds(seconds):>14}")


def print_growth(rows: list[tuple]) -> None:
    """Во сколько раз выросло время сортировки, когда n выросло в 10 раз."""
    times = {}
    for task, n, impl, seconds in rows:
        if task == "sort" and type(seconds) != str:
            times[(impl, n)] = seconds
    print()
    print("Рост времени при n x10:")
    for impl in ["sorted", "bubble_sort", "insertion_sort", "selection_sort"]:
        for n in [1_000, 10_000]:
            if (impl, n) in times and (impl, n * 10) in times:
                ratio = times[(impl, n * 10)] / times[(impl, n)]
                print(f"  {impl:<15} {n:>6} -> {n * 10:<7} x{ratio:.1f}")


if __name__ == "__main__":
    random.seed(42)
    rows = []
    for n in [1_000, 10_000, 100_000]:
        rows += bench_sorts(n)
    rows += bench_search()
    for n in [1_000, 10_000]:
        rows += bench_two_sum(n)

    print_table(rows)
    print_growth(rows)
    csv_rows = []
    for task, n, impl, seconds in rows:
        if type(seconds) != str:
            seconds = f"{seconds:.6f}"
        csv_rows.append((task, n, impl, seconds))
    write_csv(csv_rows, "data/lab07/bench.csv", header=("task", "n", "impl", "seconds"))
    print()
    print("Записано в data/lab07/bench.csv")