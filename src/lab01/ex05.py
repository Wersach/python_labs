fio = input("ФИО: ")
words = fio.split()
initials = ""

i = 0
while i < len(words):
    initials += words[i][0].upper()
    i += 1
initials += "."

clean = " ".join(words)
print(f"Инициалы: {initials}")
print(f"Длина (символов): {len(clean)}")