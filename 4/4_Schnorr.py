import random
from sympy import isprime

def gen_p(L, L2, q):
    iter = pow(2, L - L2)
    res = iter * q
    while not isprime(res + 1):
        res += q
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
    res = 2
    while pow(res, q, p) != 1:
        res += 1
        #print(res)
    return res



def gen_key(L_p, L_q):
    q = gen_q(L_q)
    p = gen_p(L_p, L_q, q)
    g = gen_g(q, p)
    w = random.randint(1, q - 1)
    y = pow(g, q - w, p)
    print('Открытый ключ:', '\np =', p, '\nq =', q, '\ng =', g, '\ny =', y, '\n')
    print('Закрытый ключ:', '\nw =', w, '\n')
    return (p, q, g, y, w)




def main(L_p, L_q, t):
    print('Генерация ключей:')
    p, q, g, y, w = gen_key(L_p, L_q)

    print('Проверка подлинности:')
    r = random.randint(1, q)
    print('r =', r)
    x = pow(g, r, p)
    print('x =', x)
    e = random.randint(0, pow(2, t) - 1)
    print('e =', e)
    s = (r + w*e) % q
    print('s =', s)
    x2 = pow(g, s, p) * pow(y, e, p) % p
    print('(g^s)(y^e) (mod p) =', x2)
    print('Результат проверки:', x == x2)

L_p = int(input('Введите длину p: '))
L_q = int(input('Введите длину q: '))
t = int(input('Введите параметр надежности t: '))
main(L_p, L_q, t)
#main(40, 20, 72)
    
