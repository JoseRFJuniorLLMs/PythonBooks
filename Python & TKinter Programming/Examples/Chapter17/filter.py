def func(n):
    return `n`[-1] == '7' or ( n % 7 == 0 ) # Cocoricos!

print filter(func, range(1,50))
