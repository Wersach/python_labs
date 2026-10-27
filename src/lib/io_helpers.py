from pathlib import Path


def check_path(path: str, suffix: str) -> None:
    """Проверяет, что путь это строка с нужным расширением.

    TypeError: путь не строка. ValueError: расширение не совпадает.
    """
    if type(path) != str:
        raise TypeError("путь должен быть строкой")
    if Path(path).suffix.lower() != suffix:
        raise ValueError(f"неверный тип файла (нужен {suffix}): {path}")