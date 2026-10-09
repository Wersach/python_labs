import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """Приводит текст к нижнему регистру, меняет ё на е, убирает лишние пробелы."""
    if type(text) != str:
        raise TypeError("нужна строка")
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
    return " ".join(text.split())


def tokenize(text: str) -> list[str]:
    """Делит текст на слова: буквы, цифры, _ и дефис внутри слова."""
    return re.findall(r"\w+(?:-\w+)*", text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Считает, сколько раз встречается каждое слово."""
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Возвращает n самых частых слов. При равенстве частот идут по алфавиту."""
    if n < 0:
        raise ValueError("n не может быть отрицательным")
    items = sorted(freq.items(), key=lambda pair: (-pair[1], pair[0]))
    return items[:n]


if __name__ == "__main__":
    for s in ["ПрИвЕт\nМИр\t", "ёжик, Ёлка", "Hello\r\nWorld", "  двойные   пробелы  "]:
        print(repr(s), "->", repr(normalize(s)))
    print(repr("ёжик Ёлка"), "yo2e=False ->", repr(normalize("ёжик Ёлка", yo2e=False)))
    print(repr("Straße"), "casefold=False ->", repr(normalize("Straße", casefold=False)))
    print(repr("Straße"), "casefold=True ->", repr(normalize("Straße")))

    print()

    for s in ["привет мир", "hello,world!!!", "по-настоящему круто", "2025 год", "emoji 😀 не слово"]:
        print(repr(s), "->", tokenize(s))

    print()

    freq = count_freq(["a", "b", "a", "c", "b", "a"])
    print(freq, "->", top_n(freq, 2))
    freq = count_freq(["bb", "aa", "bb", "aa", "cc"])
    print(freq, "->", top_n(freq, 2))