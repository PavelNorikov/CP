import random
import math
from sympy import isprime

def gcd_ex(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = gcd_ex(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y 


def gen_p(L):
    res = "0"
    while not isprime(int(res, 2)):
        res = '0'
        while int(res, 2) % 4 != 1:
            res = ""
            for i in range (1, L - 1):
                random.seed()
                res += str(random.randint(0,100)%2)
            res = '1' + res + '1'
    return int(res, 2) 


def gen_g(p):
    fact = []
    phi = p - 1
    n = phi
    for i in range(2, math.floor(math.sqrt(n) + 1)):
        if(n % i == 0):
            fact.append(i)
            while(n % i == 0):
                n /= i
    if n > 1:
        fact.append(n)
    for res in range (2, p + 1):
        ok = True
        for i in range(len(fact)):
            if not ok:
                break
            ok = ok and pow(res, int(phi // fact[i]), p) != 1
        if ok:
            return res
    return -1


def gen_y(p):
    y = random.randint(2, p-1)
    while math.gcd(y, p - 1) != 1:
        y = random.randint(2, p-1)
    return y

while 1:
####################0####################
    L = int(input('Введите длину модуля p. L = '))
    g = 0
    p = gen_p(L)
    g = gen_g(p)
    x = random.randint(2, p-1)
    K = pow(g, x, p)
    print('Модуль p =', p)
    print('Порождающий элемент g =', g)
    print('Случайное секретное число Алисы x =', x)
    print('Алиса генерирует сеансовый ключ K = g^x mod(p) =', K)

    y = gen_y(p)
    print('Случайное секретное число Боба y =', y)
    Y = pow(g, y, p)
    print('Боб отправляет Алисе Y = g^y mod(p) =', Y)

    X = pow(Y, x, p)
    print('Алиса отправляет Бобу X = Y^x mod(p) =', X)

    z = gcd_ex(y, p - 1)[1]
    K_ = pow(X, z, p)
    print('Боб вычисляет z = y^(-1) mod(p-1) =', z)
    print('Боб вычисляет K\' = X^z mod(p) =', K_)

    print("Проверка K = K\':", K == K_, '\n\n')




