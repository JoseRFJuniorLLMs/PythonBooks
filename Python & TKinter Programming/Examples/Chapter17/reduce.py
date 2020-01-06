def func(n):
    return `n`[-1] == '7'  # Cocoricos!

def sum(n1, n2):
    return n1 + n2

seq = filter(func, range(1,50))
print reduce(sum, seq)
