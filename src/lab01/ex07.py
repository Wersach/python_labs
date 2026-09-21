s = input()

start = next(i for i, c in enumerate(s) if c.isupper())
digit_i = next(i for i in range(start, len(s)) if s[i].isdigit())
step = (digit_i + 1) - start

result = []
i = start
while True:
    result.append(s[i])
    if s[i] == ".":
        break
    i += step

print("".join(result))