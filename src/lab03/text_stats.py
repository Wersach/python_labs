import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.text import normalize, tokenize, count_freq, top_n

text = sys.stdin.read()
tokens = tokenize(normalize(text))
freq = count_freq(tokens)
top = top_n(freq, 5)

print(f"Всего слов: {len(tokens)}")
print(f"Уникальных слов: {len(freq)}")
print("Топ-5:")

TABLE = False

if TABLE:
    width = len("слово")
    for word, count in top:
        if len(word) > width:
            width = len(word)
    print("слово".ljust(width) + " | частота")
    print("-" * (width + 10))
    for word, count in top:
        print(word.ljust(width) + " | " + str(count))
else:
    for word, count in top:
        print(f"{word}:{count}")