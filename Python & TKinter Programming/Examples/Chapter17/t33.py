import time, string
start = time.time()

def local():
    asct 		= time.asctime
    ltime 		= time.localtime
    now		= time.time
    lower 		= string.lower
    for i in range(20000):
        strtime = asct(ltime(now()))
        lname = lower('UPPER')

local()

print time.time() - start
