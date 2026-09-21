fio = input("ФИО: ")
words = fio.split()
initials = "".join(w[0].upper() for w in words) + "."
clean = " ".join(words)
print(f"Инициалы: {initials}")
print(f"Длина (символов): {len(clean)}")