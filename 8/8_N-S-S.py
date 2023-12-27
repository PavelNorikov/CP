from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import time
import random
import math
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



def encr(key, x):
    data = ''
    for i in x:
        if type(i) == bytes:
            data += str(i, 'utf-8')
        else:
            data += str(i)
        data += '\n'
    data = data[:-1]
    cipher_suite = Fernet(key)
    data = bytes(data, 'utf-8')
    enc = cipher_suite.encrypt(data)
    return enc

def decr(key, enc):
    cipher_suite = Fernet(key)
    dec = cipher_suite.decrypt(enc)
    dec = str(dec, 'utf-8')
    res = dec.split('\n')
    return res
    

def gen_keys(N):
    C = random.choice(N)
    h = abs(int(hash(str(C))))
    q = gen_q(len(bin(h)) - 2)
    p = gen_p(q)
    g = gen_g(q, p)
    x = random.randint(1, q - 1)
    y = pow(g, x, p)
    
    return x, y, h, q, p, g

class B:

    def __init__(self, M, i, N, keys):
        x, y, h, q, p, g = keys

        C = random.choice(N)
        self.C = C

        self.h = h
        self.q = q
        self.g = g
        self.p = p
        self.k_z = x
        self.k_o = y
        self.k_s = Fernet.generate_key()
        self.M = M
        self.name = f"Избиратель {i}"
        self.s = []
    
    def B1(self, N):
        C = self.C
        #print(C)
        s = 0
        k = 0
        r = 0
        while s == 0 or r == 0:
            k = random.randint(1, self.q - 1)
            r = pow(self.g, k, self.p) % self.q
            s = (gcd_ex(k, self.q)[1] * (self.h + self.k_z*r)) % self.q
        s1 = (C, r, s)
        s2 = encr(self.k_s, (s1[0], s1[1], s1[2], self.M))
        s3 = (s2, self.M)
        self.s = s3
        print(f"{self.name}:\nВыбор: {C}\nПодпись: {s1}\nПрикладываем М и шифруем: {s2}")
        return s3
        



def V1(k):
    m = []
    for i in range (k):
        m.append(Fernet.generate_key())
    return m



while True:
    k = int(input('Введите количество избирателей: '))
    n = list(range(1, 1 + int(input('Введите количество кандидатов: '))))
    #k = 10
    #n = [1, 2, 3, 4, 5]


    m = V1(k)
    print('\n1. V отправляет М всем В до голосования')
    for i, el in enumerate(m):
        print(f"Избиратель {i}: {el}")

    print('\n2. V отправляет А весь набор М, но без информации о том, кому они принадлежат.')
    
    print("\n3. В создает свои ключи К_зак , К_отк и выкладывает в общий доступ К_отк , а также создает секретный ключ (К_сек ), который нужен, чтобы никто не узнал содержимое бюллетеня до нужного момента.")
    Bs = []
    keys = gen_keys(n)
    print("К_зак и К_отк будут одинаковыми для всех пользователей")
    print(keys[0], keys[1])
    print('\nК_сек:')
    for i in range(len(m)):
        b = B(m[i], i+1, n, keys)
        print(f"Избиратель {i+1}:", b.k_s)
        Bs.append(b)

    print('\n4. В формирует сообщение С, где выражает свой выбор, подписывает К_зак , прикладывает к нему полученную М и шифрует К_сек.')
    choices = []
    for b in Bs:
        choices.append(b.B1(n))
    

    print('\n5. К зашифрованному тексту В прикладывает М и отправляет А.')
    for b in Bs:
        print(f"Избиратель {i+1}:", b.s)

    print('\n6. А получает зашифрованный текст, по М определяет, что он пришел от В, но не знает от кого именно и как В проголосовал, после публикует его')
    valid_ch = []
    for ch in choices:
        if ch[1] in m:
            print(f"Голос принимается: {ch}")
            valid_ch.append(ch)
        else:
            print(f"Голос НЕ принимается: {ch}")

    print('\n7. Опубликованный зашифрованный текст служит информацией, чтобы В отправил К_сек.')

    keys_mass = []
    for b in Bs:
        if b.s in valid_ch:
            print(f"Для сообщения {b.s} ключ - {b.k_s}")
            keys_mass.append((b.k_s, b.s))

    print('\n8. А собирает ключи, расшифровывает текст, подсчитывает голоса и присоединяет к опубликованному зашифрованному тексту С без М')
    res = []
    for el in keys_mass:
        res.append(decr(el[0], el[1][0]))
        

    res_vote = [0] * len(n)   
    for el in res:
        res_vote[int(el[0]) - 1] += 1
    
    for i in range(len(valid_ch)):
        print(res[i][0], valid_ch[0])
    

    print('Результаты голосования:')
    for i in range(len(res_vote)):
        print(f'Кандидат {i+1}:', res_vote[i])
