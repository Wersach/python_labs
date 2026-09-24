s = input()

digits = "0123456789"
upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

start = -1
i = 0
while i < len(s):
    if s[i] in upper_letters:
        start = i
        break
    i += 1

digit_pos = -1
i = start
while i < len(s):
    if s[i] in digits:
        digit_pos = i
        break
    i += 1

step = (digit_pos + 1) - start

result = ""
i = start
while True:
    result = result + s[i]
    if s[i] == ".":
        break
    i = i + step

print(result)