def format_record(rec):
    """Возвращает строку вида: Иванов И.И., гр. BIVT-25, GPA 4.60.

    ValueError: в ФИО меньше двух слов, пустая группа, GPA не от 0 до 5.
    TypeError: GPA не число.
    """
    fio, group, gpa = rec
    words = fio.split()
    if len(words) < 2:
        raise ValueError("в ФИО должны быть фамилия и имя")
    if group.strip() == "":
        raise ValueError("пустая группа")
    if type(gpa) != int and type(gpa) != float:
        raise TypeError("GPA должен быть числом")
    if gpa < 0 or gpa > 5:
        raise ValueError("GPA должен быть от 0 до 5")

    initials = ""
    for word in words[1:3]:
        initials += word[0].upper() + "."
    return f"{words[0].capitalize()} {initials}, гр. {group.strip()}, GPA {gpa:.2f}"


records = [
    ("Иванов Иван Иванович", "BIVT-25", 4.6),
    ("Петров Пётр", "IKBO-12", 5.0),
    ("Петров Пётр Петрович", "IKBO-12", 5.0),
    ("  сидорова  анна   сергеевна ", "ABB-01", 3.999),
]
for rec in records:
    print(rec, "->", format_record(rec))

bad = [
    ("", "BIVT-25", 4.6),
    ("Иванов Иван", "", 4.6),
    ("Иванов Иван", "BIVT-25", "5"),
    ("Иванов Иван", "BIVT-25", 5.5),
]
for rec in bad:
    try:
        format_record(rec)
    except (ValueError, TypeError) as e:
        print(rec, "->", type(e).__name__ + ":", e)