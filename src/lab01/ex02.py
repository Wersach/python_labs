def parse_num(s):
    return float(s.strip().replace(",", "."))

a = parse_num(input("a: "))
b = parse_num(input("b: "))
total = a + b
avg = total / 2
print(f"sum={total:.2f}; avg={avg:.2f}")