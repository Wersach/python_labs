import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.text import normalize, tokenize, count_freq, top_n
from io_txt_csv import read_text, write_csv


def count_words(text: str) -> dict[str, int]:
    """Нормализует текст, делит на слова и считает частоты."""
    return count_freq(tokenize(normalize(text)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Отчёт по частотам слов")
    parser.add_argument("--in", dest="inputs", nargs="+", default=["data/lab04/input.txt"])
    parser.add_argument("--out", "--total", dest="out", default="data/lab04/report.csv")
    parser.add_argument("--per-file", default=None)
    parser.add_argument("--encoding", default="utf-8")
    args = parser.parse_args()

    total = {}
    per_file_rows = []
    for path in args.inputs:
        try:
            text = read_text(path, args.encoding)
        except FileNotFoundError:
            print(f"Файл не найден: {path}")
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Не удалось прочитать {path} в кодировке {args.encoding}")
            sys.exit(1)

        freq = count_words(text)
        for word, count in freq.items():
            per_file_rows.append((Path(path).name, word, count))
            total[word] = total.get(word, 0) + count

    per_file_rows.sort(key=lambda row: (row[0], -row[2], row[1]))
    total_rows = top_n(total, len(total))
    write_csv(total_rows, args.out, header=("word", "count"))
    if args.per_file is not None:
        write_csv(per_file_rows, args.per_file, header=("file", "word", "count"))

    all_words = 0
    for word, count in total_rows:
        all_words += count
    print(f"Всего слов: {all_words}")
    print(f"Уникальных слов: {len(total)}")
    print("Топ-5:")
    for word, count in top_n(total, 5):
        print(f"{word}:{count}")


if __name__ == "__main__":
    main()