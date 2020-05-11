x=54321
y = str(x)[::-1]
if x < 0:
    y = "-" + y[:-1]
y = int(y)
if y >= 2**31 - 1 or y<= -2**31:
    print(0)
print(y)
