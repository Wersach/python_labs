import argparse
import sys

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def build_parser() -> argparse.ArgumentParser:
    """Описывает три команды конвертации, у каждой --in и --out."""
    parser = argparse.ArgumentParser(
        prog="python -m src.lab06.cli_convert",
        description="Конвертеры данных: JSON, CSV, XLSX",
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="команда")

    p1 = sub.add_parser("json2csv", help="JSON в CSV")
    p1.add_argument("--in", dest="input", required=True, help="входной .json")
    p1.add_argument("--out", dest="output", required=True, help="выходной .csv")

    p2 = sub.add_parser("csv2json", help="CSV в JSON")
    p2.add_argument("--in", dest="input", required=True, help="входной .csv")
    p2.add_argument("--out", dest="output", required=True, help="выходной .json")

    p3 = sub.add_parser("csv2xlsx", help="CSV в XLSX")
    p3.add_argument("--in", dest="input", required=True, help="входной .csv")
    p3.add_argument("--out", dest="output", required=True, help="выходной .xlsx")
    return parser


def main() -> None:
    """Разбирает аргументы и вызывает нужную функцию из ЛР5."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "json2csv":
            json_to_csv(args.input, args.output)
        elif args.command == "csv2json":
            csv_to_json(args.input, args.output)
        else:
            csv_to_xlsx(args.input, args.output)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {args.input}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка в данных: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Готово: {args.output}")


if __name__ == "__main__":
    main()