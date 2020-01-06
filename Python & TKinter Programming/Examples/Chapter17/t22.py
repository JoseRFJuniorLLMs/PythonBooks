import time
start = time.time()
l = []
for col in range(100):
	for row in range(10000):
		l.append('%d.%d' % (row, col))
print time.time()-start
