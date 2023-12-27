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

def gen_str():
    x = ''
    for i in range(32):
        x += str(random.randint(0,9))
        #print(x[2:])
    return x


def int_to_key(x):
    password = bytes(str(x), 'utf-8')

    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = bytes(str(x), 'utf-8'),
        iterations = 480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key
  

while 1:
####################0####################
    L = int(input('Введите длину модуля p. L = '))
    g = 0
    p = gen_p(L)
    g = gen_g(p)
    P = Fernet.generate_key()
    print('Общий секрет P = ', P)
    r = random.randint(10, 100)
    grp = pow(g, r, p)
    print('Порождающий элемент g = ', g)
    print('Модуль p = ', p)
    print('Общий секрет r = ', r)
    print('Открытый ключ g^r mod(p) = ', grp, '\n')

####################1####################
    A = 'Alice'
    s1 = (A, grp)
    print('1. Алиса отправляет Бобу (А, g^r mod(p)) = ', s1, '\n')

####################2####################
    K = random.randint(10, 1000000) % p
    K_key = int_to_key(K)
    #print(111, K_key)
    print('2. Боб генерирует сеансовый ключ k = ', K)
    R = random.randint(10, 100)
    print('Случайное число Боба R = ', R)
    s2_1 = pow(g, R, p)
    s2_2 = K * pow(g, r * R, p) % p
    s2 = encr(P, (str(s2_1), str(s2_2)))
    print('g^R mod(p) = ', s2_1)
    print('k*g^(r*R) mod(p) = ', s2_2)
    print('Боб отправляет Алисе (E_P(g^R mod(p), k*g^(r*R) mod(p))) = ', s2, '\n')

####################3####################    
    s2_decr = decr(P, s2)
    print('3. Алиса расшифровывает (E_P(g^R mod(p), k*g^(r*R) mod(p))). Получает ', s2_decr)
    g_rR = pow(int(s2_decr[0]), r, p)
    obr_g_rR = gcd_ex(g_rR, p)[1]
    A_K = obr_g_rR * int(s2_decr[1]) % p
    print('Алиса вычисляет k = k*g^(r*R) * ((g^R)^r)^(-1) mod(p) = ', A_K)
    A_K = int_to_key(A_K)
    R_A = gen_str()
    print('Алиса генерирует случайную строку R_A = ', R_A)
    s3 = encr(A_K, {R_A})
    print('Алиса отправляет Бобу (E_k(R_A)) = ', s3, '\n')

####################4####################    
    s3_decr = decr(K_key, s3)
    print('4. Боб расшифровывает E_k(R_A). Получает ', s3_decr[0])
    R_B = gen_str()
    print('Боб генерирует случайную строку R_B = ', R_B)
    s4 = encr(K_key, (s3_decr[0], R_B))
    print('Боб отправляет Алисе (E_k(R_A, R_B)) = ', s4, '\n')

####################5####################    
    s4_decr = decr(A_K, s4)
    print('5. Алиса расшифровывает E_k(R_A, R_B). Получает ', s4_decr)
    print('Алиса сравнивает отправленную и расшифрованную строку. Результат : ', s4_decr[0] == R_A)
    s5 = encr(A_K, {R_B})
    print('Алиса отправляет Бобу (E_k(R_B)) = ', s5, '\n')

####################6####################    
    s5_decr = decr(K_key, s5)
    print('6. Боб расшифровывает E_k(R_B). Получает ', s5_decr)
    print('Боб сравнивает отправленную и расшифрованную строку. Результат : ', s5_decr[0] == R_B, '\n\n\n')

