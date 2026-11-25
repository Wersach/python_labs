import json

from src.lab04.io_txt_csv import ensure_parent_dir
from src.lab08.models import student_from_dict, student_to_dict
from src.lib.io_helpers import check_path


def students_to_json(students: list[dict], path: str) -> None:
    """Сохраняет список записей в JSON (массив объектов).

    TypeError: путь не строка. ValueError: не тот тип файла, students не
    список или запись неверная (с номером). Если проверка не прошла,
    файл не создаётся.
    """
    check_path(path, ".json")
    if type(students) != list:
        raise ValueError("students должен быть списком записей")
    data = []
    for i, rec in enumerate(students):
        try:
            data.append(student_to_dict(rec))
        except ValueError as e:
            raise ValueError(f"запись №{i}: {e}")

    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def students_from_json(path: str) -> list[dict]:
    """Читает JSON-массив и превращает каждый объект в запись студента.

    Политика strict: первая же битая запись даёт ValueError с номером
    записи (с 0) и причиной. Пустой массив даёт пустой список.
    TypeError: путь не строка. ValueError: не тот тип файла, битый JSON,
    не массив, битая запись. FileNotFoundError: нет файла.
    """
    check_path(path, ".json")
    with open(path, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"битый JSON: {e.msg} (строка {e.lineno})")

    if type(data) != list:
        raise ValueError("JSON должен быть массивом записей")
    students = []
    for i, item in enumerate(data):
        try:
            students.append(student_from_dict(item))
        except ValueError as e:
            raise ValueError(f"запись №{i}: {e}")
    return students


def show_error(func, *args) -> None:
    """Вызывает func(*args) и печатает, какая ошибка получилась."""
    try:
        func(*args)
        print("ошибки нет")
    except (TypeError, ValueError, FileNotFoundError) as e:
        print(type(e).__name__ + ":", e)


if __name__ == "__main__":
    from src.lab08.models import format_student, make_student

    inp = "data/lab08/students_input.json"
    out = "data/lab08/students_output.json"

    print("Туда-обратно")
    students = students_from_json(inp)
    for s in students:
        print(format_student(s))
    students_to_json(students, out)
    print("записей прочитано:", len(students), "| записей прочитано из output:",
          len(students_from_json(out)))

    print()
    print("Ошибки")
    print("битая запись (students_bad.json):", end=" ")
    show_error(students_from_json, "data/lab08/students_bad.json")
    print("нет файла:", end=" ")
    show_error(students_from_json, "data/lab08/net.json")
    print("не .json:", end=" ")
    show_error(students_from_json, "data/samples/people.csv")
    print("путь не строка:", end=" ")
    show_error(students_from_json, 5)
    print("не массив:", end=" ")
    show_error(students_from_json, "data/samples/bad/dict.json")
    print("битый JSON:", end=" ")
    show_error(students_from_json, "data/samples/bad/broken.json")
    print("неверная дата:", end=" ")
    show_error(make_student, "Иванов Иван", "2003-02-30", "БИВТ-26-6-1", 4.0)
    print("gpa = 7:", end=" ")
    show_error(make_student, "Иванов Иван", "2003-05-14", "БИВТ-26-6-1", 7)