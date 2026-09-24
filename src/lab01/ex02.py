def get_num(s):
    return float(s.replace(",", "."))

a = get_num(input("a: "))
b = get_num(input("b: "))
total = a + b
avg = total / 2
print(f"sum={total:.2f}; avg={avg:.2f}")