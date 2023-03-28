from random import randint

def generateNumber(n = 6):
    return ''.join(["%s" % randint(0, 9) for num in range(0, n)])
