from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def _check_fio(fio) -> str:
    if type(fio) != str or fio.strip() == "":
        raise ValueError("fio: должна быть непустая строка")
    return fio.strip()


def _check_group(group) -> str:
    if type(group) != str or group.strip() == "":
        raise ValueError("group: должна быть непустая строка")
    return group.strip()


def _check_birthdate(birthdate) -> str:
    if type(birthdate) != str:
        raise ValueError("birthdate: должна быть строка YYYY-MM-DD")
    try:
        born = date.fromisoformat(birthdate)
    except ValueError:
        raise ValueError(f"birthdate: '{birthdate}' не дата в формате YYYY-MM-DD")
    if born > date.today():
        raise ValueError(f"birthdate: '{birthdate}' дата в будущем")
    return birthdate


def _check_gpa(gpa) -> float:
    # type(...) вместо isinstance: bool (True/False) сюда не проходит
    if type(gpa) != int and type(gpa) != float:
        raise ValueError("gpa: должно быть число (int или float)")
    if not 0 <= gpa <= 5:
        raise ValueError(f"gpa: {gpa} вне диапазона 0..5")
    return float(gpa)


def make_student(fio, birthdate, group, gpa) -> dict:
    """Собирает запись студента, проверяя каждое поле.

    ValueError: любое поле неверное (в сообщении указано какое и почему).
    """
    return {
        "fio": _check_fio(fio),
        "birthdate": _check_birthdate(birthdate),
        "group": _check_group(group),
        "gpa": _check_gpa(gpa),
    }


def validate_student(rec: dict) -> None:
    """Проверяет готовую запись: ровно нужные ключи и верные значения.

    ValueError: не словарь, неверный набор ключей, неверное значение.
    """
    if type(rec) != dict:
        raise ValueError("запись должна быть словарём")
    if set(rec) != set(STUDENT_FIELDS):
        missing = sorted(set(STUDENT_FIELDS) - set(rec))
        extra = sorted(set(rec) - set(STUDENT_FIELDS))
        raise ValueError(f"неверный набор ключей: не хватает {missing}, лишние {extra}")
    _check_fio(rec["fio"])
    _check_birthdate(rec["birthdate"])
    _check_group(rec["group"])
    _check_gpa(rec["gpa"])


def student_age(rec: dict, today=None) -> int:
    """Полных лет на дату today (по умолчанию сегодня)."""
    born = date.fromisoformat(rec["birthdate"])
    if today is None:
        today = date.today()
    age = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        age -= 1
    return age


def _years_word(n: int) -> str:
    if 11 <= n % 100 <= 14:
        return "лет"
    if n % 10 == 1:
        return "год"
    if 2 <= n % 10 <= 4:
        return "года"
    return "лет"


def format_student(rec: dict) -> str:
    """Например: Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30"""
    words = rec["fio"].split()
    initials = ""
    for word in words[1:3]:
        initials += word[0].upper() + "."
    age = student_age(rec)
    return (f"{words[0].capitalize()} {initials} ({rec['group']}), "
            f"{age} {_years_word(age)}, GPA {rec['gpa']:.2f}")


def student_to_dict(rec: dict) -> dict:
    """Копия записи для сериализации. ValueError, если запись неверная."""
    validate_student(rec)
    return {key: rec[key] for key in STUDENT_FIELDS}


def student_from_dict(d: dict) -> dict:
    """Запись из словаря: берёт ровно нужные ключи, проверяет значения.

    ValueError: не словарь, нет нужного ключа или неверное значение.
    Лишние ключи в d игнорируются.
    """
    if type(d) != dict:
        raise ValueError("запись должна быть словарём")
    for key in STUDENT_FIELDS:
        if key not in d:
            raise ValueError(f"нет ключа {key}")
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])