import csv
from pathlib import Path


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт родительские папки файла, если их ещё нет."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает файл целиком и возвращает его содержимое одной строкой.

    Другая кодировка задаётся параметром, например encoding="cp1251".
    FileNotFoundError и UnicodeDecodeError не перехватываются.
    """
    return Path(path).read_text(encoding=encoding)


def write_csv(rows: list[tuple | list], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    """Записывает строки в CSV (разделитель запятая, кодировка UTF-8).

    Если указан header, он идёт первой строкой. Все строки должны быть
    одной длины, иначе ValueError. Файл перезаписывается.
    """
    rows = list(rows)
    for row in rows:
        if len(row) != len(rows[0]):
            raise ValueError("строки разной длины")
    if header is not None and len(rows) > 0 and len(header) != len(rows[0]):
        raise ValueError("длина заголовка не совпадает с длиной строк")

    ensure_parent_dir(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    write_csv([("word", "count"), ("test", 3)], "data/lab04/check.csv")
    print(repr(read_text("data/lab04/check.csv")))

    write_csv([], "data/lab04/empty_check.csv")
    print(repr(read_text("data/lab04/empty_check.csv")))

    write_csv([], "data/lab04/header_check.csv", header=("a", "b"))
    print(repr(read_text("data/lab04/header_check.csv")))

    try:
        write_csv([(1, 2), (3,)], "data/lab04/bad.csv")
    except ValueError as e:
        print("ValueError:", e)

    try:
        read_text("data/lab04/net_takogo.txt")
    except FileNotFoundError as e:
        print("FileNotFoundError:", e)