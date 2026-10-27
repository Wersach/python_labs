import csv
import json

from src.lab04.io_txt_csv import ensure_parent_dir
from src.lib.io_helpers import check_path


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл (список словарей) в CSV.

    Колонки берутся из ключей первого объекта, в том же порядке. Если в
    другом объекте поля нет, ячейка остаётся пустой. Лишнее поле, которого
    нет в первом объекте, вызывает ValueError.
    TypeError: путь не строка. ValueError: не тот тип файла, битый, пустой
    или неподходящий JSON. FileNotFoundError: нет входного файла.
    """
    check_path(json_path, ".json")
    check_path(csv_path, ".csv")

    with open(json_path, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"битый JSON: {e.msg} (строка {e.lineno})")

    if type(data) != list or len(data) == 0:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    for item in data:
        if type(item) != dict:
            raise ValueError("JSON должен быть списком словарей")

    fieldnames = list(data[0].keys())
    if len(fieldnames) == 0:
        raise ValueError("в первом объекте нет полей")
    for item in data:
        for key in item:
            if key not in fieldnames:
                raise ValueError(f"поле {key} есть не в первом объекте")

    ensure_parent_dir(csv_path)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV в JSON (список словарей, все значения строки).

    Заголовок обязателен. CSV, в котором нет строк с данными, считается пустым.
    TypeError: путь не строка. ValueError: не тот тип файла, пустой CSV,
    повторяющиеся колонки, строка не совпадает с заголовком по длине.
    FileNotFoundError: нет входного файла.
    """
    check_path(csv_path, ".csv")
    check_path(json_path, ".json")

    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    if fieldnames is None or len(rows) == 0:
        raise ValueError("Пустой CSV или нет строк с данными")
    if len(set(fieldnames)) != len(fieldnames):
        raise ValueError("в заголовке CSV повторяются колонки")
    for row in rows:
        if None in row or None in row.values():
            raise ValueError("строка CSV не совпадает с заголовком по длине")

    ensure_parent_dir(json_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def show_error(func, *args) -> None:
    """Вызывает func(*args) и печатает, какая ошибка получилась."""
    try:
        func(*args)
        print("ошибки нет")
    except (TypeError, ValueError, FileNotFoundError) as e:
        print(type(e).__name__ + ":", e)


if __name__ == "__main__":
    print("JSON -> CSV")
    for name in ["people", "students"]:
        src = f"data/samples/{name}.json"
        dst = f"data/out/{name}_from_json.csv"
        json_to_csv(src, dst)
        with open(src, encoding="utf-8") as f:
            count_json = len(json.load(f))
        with open(dst, encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        print(dst, "| заголовок:", rows[0])
        print("  записей в JSON:", count_json, "| строк данных в CSV:", len(rows) - 1)

    print()
    print("CSV -> JSON")
    for name in ["people", "students"]:
        src = f"data/samples/{name}.csv"
        dst = f"data/out/{name}_from_csv.json"
        csv_to_json(src, dst)
        with open(src, encoding="utf-8", newline="") as f:
            count_csv = len(list(csv.DictReader(f)))
        with open(dst, encoding="utf-8") as f:
            objects = json.load(f)
        print(dst, "| ключи:", list(objects[0].keys()))
        print("  строк данных в CSV:", count_csv, "| объектов в JSON:", len(objects))

    print()
    print("Ошибки json_to_csv")
    json_cases = [
        ("нет файла", "data/samples/net.json"),
        ("не .json", "data/samples/people.csv"),
        ("пустой список", "data/samples/bad/empty.json"),
        ("не список", "data/samples/bad/dict.json"),
        ("не словари", "data/samples/bad/not_dicts.json"),
        ("битый JSON", "data/samples/bad/broken.json"),
        ("лишнее поле", "data/samples/bad/extra_key.json"),
    ]
    for label, path in json_cases:
        print(label + ":", end=" ")
        show_error(json_to_csv, path, "data/out/x.csv")
    print("путь не строка:", end=" ")
    show_error(json_to_csv, 5, "data/out/x.csv")

    print()
    print("Ошибки csv_to_json")
    csv_cases = [
        ("нет файла", "data/samples/net.csv"),
        ("не .csv", "data/samples/people.json"),
        ("пустой файл", "data/samples/bad/empty.csv"),
        ("только заголовок", "data/samples/bad/header_only.csv"),
        ("лишнее значение", "data/samples/bad/long_row.csv"),
        ("не хватает значения", "data/samples/bad/short_row.csv"),
        ("повтор колонки", "data/samples/bad/dup_header.csv"),
    ]
    for label, path in csv_cases:
        print(label + ":", end=" ")
        show_error(csv_to_json, path, "data/out/x.json")