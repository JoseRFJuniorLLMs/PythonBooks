import time
start = time.time()
l = []
for row in range(10000):
	for col in range(100):
		l.append('%d.%d' % (row, col))
print time.time()-start
