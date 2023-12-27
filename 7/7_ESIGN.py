#import numpy
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
    

def gen_q(L):
    res = "0"
    while not isprime(int(res, 2)):
        res = ""
        for i in range (1, L - 1):
            random.seed()
            res += str(random.randint(0,100)%2)
        res = '1' + res + '1'
    return int(res, 2)


def main(L, m, k, m_):
    print('Генерация подписи:')
    p = gen_q(L)
    q = gen_q(L)
    r = gen_q(L)
    n = p*p*q*r
    print('Открытый ключ:', '\nn =', n, '\nk =', k, '\n')
    print('Закрытый ключ:', '\np =', p, '\nq =', q, '\nr =', r, '\n')
    h = abs(int(hash(str(m)))) % n
    print('h =', h)
    u = random.randint(1, p*q - 2)
    x = m_ + u*r
    print('x =', x)
    w = math.ceil((h - pow(x, k, n)) / p*q*r)
    #a = math.ceil((h - pow(x, k, n)) / (p*q*r)) % p
    a = math.ceil((h - pow(x, k, n)) / (p*q*r))
    print('a =', a)
    b = (a * gcd_ex(k*pow(x, k-1, p) % p, p)[1]) % p
    print('b =', b)
    s = x + b*p*q*r
    #s = x + ((w * gcd_ex(k * pow(x, k-1, p), p)[1]) % p) * p * q * r
    print('s =', s)
    #print('s2 =', s2)
    print('A -> W(B): {', m, s, '}\n')


    print('\nПроверка подписи:')
    h2 = abs(int(hash(str(m)))) % n
    print('h =', h2)
    c = math.ceil((3 * math.log2(n)) / 4)
    #c = math.ceil((2 * math.log2(n)) / 3)
    #c= math.ceil(math.log2(n))
    print('c =', c)
    print('Результат проверки:', h2 <= pow(s, k, n) and pow(s, k, n) <= h2 + pow(2, c))
    print(h2, pow(s, k, n), h2 + pow(2, c))
    
    
    print('\nПолучение секретного сообщения:')
    B_m_ = s % r
    print('m* =', B_m_)


L = int(input('Введите длину p, q и r: '))
m = int(input('Введите безобидное сообщение m: '))
k = L_q = int(input('Введите параметр безопасности k: '))
m_= int(input('Введите секретное сообщение m*: '))
main(L, m, k, m_)
#main(30, 9999, 5, 321)
