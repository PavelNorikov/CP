import random
from sympy import isprime


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def gcd_ex(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = gcd_ex(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y 


def gen_p(q):
    res = 2 * q
    while not isprime(res + 1):
        res *= 2
    return res + 1


def gen_q(L):
    res = "0"
    while not isprime(int(res, 2)):
        res = ""
        for i in range (1, L - 1):
            random.seed()
            res += str(random.randint(0,100)%2)
        res = '1' + res + '1'
    return int(res, 2)



def gen_g(q, p):
    res = 1
    h = 2
    while res == 1:
        res = pow(h, (p - 1) // q, p)
        h = random. randint(2, p - 2)
    return res



def main(m):
    print('Генерация подписи:')
    #h = m
    h = abs(int(hash(str(m))))
    print('h =', h)
    q = gen_q(len(bin(h)) - 2)
    p = gen_p(q)
    g = gen_g(q, p)
    x = random.randint(1, q - 1)
    y = pow(g, x, p)
    print('Общие элементы:', '\np =', p, '\nq =', q, '\ng =', g, '\n')
    print('Открытый ключ:', '\ny =', y, '\n')
    print('Закрытый ключ:', '\nx =', x, '\n')

    s = 0
    k = 0
    while s == 0 or r == 0:
        k = random.randint(1, q - 1)
        #k = 3
        r = pow(g, k, p) % q
        s = (gcd_ex(k, q)[1] * (h + x*r)) % q
        #print(s)

    print('k =', k)
    print('r =', r)
    print('s =', s)
    print('A -> B: {', m, r, s, '}\n')

    print('\nПроверка подписи:')
    u = gcd_ex(s, q)[1]
    print('u =', u)
    a = (h * u) % q
    print('a =', a)
    b = (r * u) % q
    print('b =', b)
    v = (pow(g, a, p) * pow(y, b, p)) % p % q
    print('v =', v)
    print('Результат проверки:', v == r)


s = str(input('Введите сообщение: '))
main(s)