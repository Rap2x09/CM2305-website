x=54321
if(x<0):
    x= -x
    y=str(x)+"-"
    if(abs(int(y[::-1])) > (2 ** 31 - 1)):
        print(0)
    else:
        print(int(y[::-1]))
x=str(x)
if(abs(int(x[::-1])) > (2 ** 31 - 1)):
    print(0)
else:
    print(int(x[::-1]))
