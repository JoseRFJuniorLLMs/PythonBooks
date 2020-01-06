import random

from tempdata import data

fd =open ('t3ddata.py', 'w')
fd.write('data = [\n')

l = 1.0
r = 0.0

for i in range(10):
    fd.write('(')
    tuple = data[i]
    for x in range(100):
        v = tuple[x]
        lf = l * (100./(100.-x))
        rf = r * (x/100.)*1.
        v = int(float(v) * lf) + int(float(v) * rf) + random.choice(range(-5, 3))
        if v > 100: v = 100
        if v < 0: v = 0
        fd.write('%d,' % v)
    fd.write('),\n')
    l = l - 0.1
    r = r + 0.2
fd.write(']\n')
fd.close
