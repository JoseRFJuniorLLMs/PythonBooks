import time
start = time.time()

part1 = part2 = part3 = '1234567890'

for i in range(999999):
    longString = '%s %s %s' % (part1, part2, part3)

print time.time() - start
