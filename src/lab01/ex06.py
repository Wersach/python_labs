n = int(input())
ochno = 0
zaochno = 0
for _ in range(n):
    parts = input().split()
    if parts[-1] == "True":
        ochno += 1
    else:
        zaochno += 1
print(ochno, zaochno)