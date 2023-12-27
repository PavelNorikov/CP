from cryptography.fernet import Fernet
import time
import random

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

########1########
A_rand = random.randint(1, 10000000000)
A_key = Fernet.generate_key()
print('1. Алиса генерирует R_a =', A_rand)
s1 = ("Alice", str(A_rand))
print("Алиса отсылает Бобу {A, R_a} =", s1, '\n')

########2########
B_rand = random.randint(1, 10000000000)
B_key = Fernet.generate_key()
B_time = time.time()
print('2. Боб генерирует R_b =', B_rand)
print('Метка времени Боба T_b =', B_time)
s2 = ("Bob", str(B_rand), encr(B_key, (s1[0], s1[1], B_time)))
print("Боб отсылает Тренту {B, R_b, E_b(A, R_a, T_b)} =", s2, '\n')

########3########
K = Fernet.generate_key()
dec_s2 = decr(B_key, s2[2])
print('3. Трент расшифровывает E_b(A, R_a, T_b)')
print('A =', dec_s2[0])
print('R_a =', dec_s2[1])
print('T_b =', dec_s2[2])
print('Трент генерирует K =', K)
s3_1 = encr(A_key, (s2[0], dec_s2[1], K, dec_s2[2]))
s3_2 = encr(B_key, (dec_s2[0], K, dec_s2[2]))
s3 = (s3_1, s3_2, s2[1])
print("Трент отсылает Алисе {E_a(B, R_a, K, T_b), E_b(A, K, T_b), R_b} =", s3, '\n')

########4########
dec_s3_1 = decr(A_key, s3[0])
print('4. Алиса расшифровывает E_a(B, R_a, K, T_b)')
print('B =', dec_s3_1[0])
print('R_a =', dec_s3_1[1])
print('K =', dec_s3_1[2])
print('T_b =', dec_s3_1[3])
s4 = (s3[1], encr(dec_s3_1[2], {s3[2]}))
print("Алиса отсылает Бобу {E_b(A, K, T_b), E_k(R_b)} =", s4, '\n')

dec_s4_1 = decr(B_key, s4[0])
dec_s4_2 = decr(bytes(dec_s4_1[1], 'utf-8'), s4[1])
print('Боб расшифровывает E_b(A, K, T_b)')
print('A =', dec_s4_1[0])
print('K =', dec_s4_1[1])
print('T_b =', dec_s4_1[2])
print('Боб расшифровывает E_k(R_b)')
print('R_b =', dec_s4_2[0], '\n', '\n')


########ПРОВЕРКА ПОДЛИННОСТИ########
########1########
print('ПРОВЕРКА ПОДЛИННОСТИ')
A_rand2 = random.randint(1, 1000)
print('1. Алиса генерирует R2_a =', A_rand2)
ss1 = (s3_2, str(A_rand2))
print("Алиса отсылает Бобу {E_b(A, K, T_b), R2_a} =", ss1, '\n')

########2########
B_rand2 = random.randint(1, 1000)
print('2. Боб генерирует R2_b =', B_rand2)
ss2 = (str(B_rand2), encr(dec_s4_1[1], {ss1[1]}))
print("Боб отсылает Алисе {R2_b, E_k(R2_a)} =", ss2, '\n')

########3########
dec_ss2 = decr(dec_s3_1[2], ss2[1])
print('3. Алиса расшифровывает E_k(R2_a)')
print('R2_a =', dec_ss2[0])
ss3 = encr(dec_s4_1[1], {ss2[0]})
print("Алиса отсылает Бобу {E_k(R2_b)} =", ss3, '\n')

dec_ss3 = decr(bytes(dec_s4_1[1], 'utf-8'), ss3)
print('Боб расшифровывает E_k(R2_b)')
print('R2_b =', dec_ss3[0])
