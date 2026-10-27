import json
from pathlib import Path

PEOPLE = [
    {"name": "Alice", "age": 22, "city": "SPB"},
    {"name": "Bob", "age": 25, "city": "Moscow"},
    {"name": "Carlos", "age": 30, "city": "Kazan"},
    {"name": "Dana", "age": 21, "city": "SPB"},
    {"name": "Andrey", "age": 27, "city": "Novosibirsk"},
]

STUDENTS = [
    {"fio": "Иванов Иван", "group": "БИВТ-26-6-1", "gpa": 4.5},
    {"fio": "Петрова Анна", "group": "БИВТ-26-6-2"},
    {"fio": "Сидоров Пётр", "group": "БИВТ-26-6-1", "gpa": 3.9},
]

FILES = {
    "data/samples/people.json": json.dumps(PEOPLE, ensure_ascii=False, indent=2),
    "data/samples/people.csv": "name,age,city\nAlice,22,SPB\nBob,25,Moscow\nCarlos,30,Kazan\nDana,21,SPB\nAndrey,27,Novosibirsk\n",
    "data/samples/cities.csv": "city,country,population\nSPB,Russia,5384342\nMoscow,Russia,13010112\nKazan,Russia,1306953\nNovosibirsk,Russia,1620162\nYekaterinburg,Russia,1493749\n",
    "data/samples/students.json": json.dumps(STUDENTS, ensure_ascii=False, indent=2),
    "data/samples/students.csv": "fio,group,gpa\nИванов Иван,БИВТ-26-6-1,4.5\nПетрова Анна,БИВТ-26-6-2,5.0\nСидоров Пётр,БИВТ-26-6-1,3.9\n",
    "data/samples/bad/empty.json": "[]",
    "data/samples/bad/dict.json": "{\"a\": 1}",
    "data/samples/bad/not_dicts.json": "[1, 2]",
    "data/samples/bad/broken.json": "{\"a\": 1,}",
    "data/samples/bad/extra_key.json": "[{\"a\": 1}, {\"a\": 2, \"b\": 3}]",
    "data/samples/bad/empty.csv": "",
    "data/samples/bad/header_only.csv": "name,age\n",
    "data/samples/bad/long_row.csv": "a,b\n1,2,3\n",
    "data/samples/bad/short_row.csv": "a,b\n1\n",
    "data/samples/bad/dup_header.csv": "a,a\n1,2\n",
}

if __name__ == "__main__":
    for path, text in FILES.items():
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text, encoding="utf-8")
        print("создан", path)