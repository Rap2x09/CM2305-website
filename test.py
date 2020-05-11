from datetime import datetime
import time
#import cProfile
#import fileinput
#import pstats
#import timeit
#import profile

code1 = 'C:\\Computer Science\\COMPSCI_Y2\\NEW WEBSITE\\CM2305-website\\test2.py'
code2 = 'C:\\Computer Science\\COMPSCI_Y2\\NEW WEBSITE\\CM2305-website\\test3.py'

codes = [code1, code2]
codetime = []
for i in codes:
    start_time = datetime.now()
    exec(open(i).read())
    end_time = datetime.now()
    codetime.append((end_time - start_time))

print(codetime)
if codetime[0] > codetime[1]:
    print("The first code is quicker by {} seconds!".format(codetime[0]-codetime[1]))
elif codetime[1] > codetime[0]:
    print("The first code is slower by {} seconds.".format(codetime[1]-codetime[0]))
elif codetime[1] == codetime[0]:
    print("The first code takes the same time as the second code!")

#pr = cProfile.Profile()
#pr.enable()
#for line in fileinput.input():
#    for i in range(10):
#        y = int(line.strip()) + int(line.strip())
#pr.disable()
#pr.print_stats(sort='time')

#cProfile.runctx('"{}"'.format(code1), globals(), locals(), "Profile1.prof")
#cProfile.runctx('"{}"'.format(code2), globals(), locals(), "Profile2.prof")

#r1 = pstats.Stats("Profile1.prof")
#r1_s = r1.strip_dirs().print_stats("cumtime")

#r2 = pstats.Stats("Profile2.prof")
#r2.strip_dirs().print_stats("cumtime")

#timeit.timeit("-".join(code1))
#timeit.timeit("-".join(code2))

#profile.run('"{}"'.format(code1))

#if r1.cumtime() > r2.cumtime():
#    print('Your code is slower than the fastest code by ' + (r1.cumtime() - r2.cumtime()) + ' seconds.')
#elif r2.cumtime() > r1.cumtime():
#    print('Your code is quicker than the fastest code by ' + (r2.cumtime() - r1.cumtime()) + ', congratulations!')
#r_output = []

#codes = [code1, code2]
#print(codes)

#for i in range(0, (len(codes))):
#    i+1
#    codey = codes[i]
#    p = cProfile.Profile()
#    p.enable()
#    importlib.import_module(codey)
#    p.disable()
#    p.print_stats(sort='time')

#def func1():
#    exec(open(code1).read())

#def func2():
#    exec(open(code1).read())

#def callfuncs():
#    func1()
#    func2()

#func1()
#func2()
