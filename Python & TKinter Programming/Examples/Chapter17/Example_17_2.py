import time
import string

start = time.time()

def splitter():
    list = string.split('A B C D E F G H', ' ')

for i in range(123456):
    splitter()

print time.time() - start

