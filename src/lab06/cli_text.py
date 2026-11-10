import argparse
import sys

from src.lib.text import normalize, tokenize, count_freq, top_n


def cat_file(path: str, numbered: bool) -> None:
    """Печатает файл построчно. При numbered=True перед строкой стоит её номер."""
    with open(path, encoding="utf-8") as f:
        number = 1
        for line in f:
            line = line.rstrip("\n")
            if numbered:
                print(f"{number:>4}  {line}")
            else:
                print(line)
            number += 1


def print_stats(path: str, top: int) -> None:
    """Печатает число слов, число уникальных слов и top самых частых слов."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    freq = count_freq(tokenize(normalize(text)))
    total = 0
    for count in freq.values():
        total += count
    print(f"Всего слов: {total}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{top}:")
    for word, count in top_n(freq, top):
        print(f"{word}:{count}")


def positive_int(text: str) -> int:
    """Тип для --top: целое число не меньше 1, иначе понятная ошибка argparse."""
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"нужно целое число, а не {text!r}")
    if value < 1:
        raise argparse.ArgumentTypeError("должно быть не меньше 1")
    return value


def build_parser() -> argparse.ArgumentParser:
    """Описывает команды и параметры программы."""
    parser = argparse.ArgumentParser(
        prog="python -m src.lab06.cli_text",
        description="Текстовые утилиты: вывод файла и частоты слов",
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="команда")

    p_cat = sub.add_parser("cat", help="вывести файл построчно")
    p_cat.add_argument("--input", required=True, help="путь к текстовому файлу")
    p_cat.add_argument("-n", action="store_true", help="нумеровать строки")

    p_stats = sub.add_parser("stats", help="частоты слов в тексте")
    p_stats.add_argument("--input", required=True, help="путь к текстовому файлу")
    p_stats.add_argument("--top", type=positive_int, default=5, help="сколько слов показать (по умолчанию 5)")
    return parser


def main() -> None:
    """Разбирает аргументы и запускает нужную команду."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "cat":
            cat_file(args.input, args.n)
        else:
            print_stats(args.input, args.top)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {args.input}", file=sys.stderr)
        sys.exit(1)
    except (IsADirectoryError, PermissionError):
        print(f"Ошибка: не удаётся открыть {args.input}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Ошибка: файл {args.input} не в кодировке UTF-8", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()