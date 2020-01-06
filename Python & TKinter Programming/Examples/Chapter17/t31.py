import time, string
start = time.time()

for i in range(20000):
	strtime = time.asctime(time.localtime(time.time()))
	lname = string.lower('UPPER')

print time.time() - start
