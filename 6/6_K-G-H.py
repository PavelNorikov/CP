import numpy as np
import random as rand

def gram_schmidt(vectors):
    basis = []
    for vector in vectors:
        for ex_v in basis:
            vector -= np.dot(vector, ex_v) // np.dot(ex_v, ex_v) * ex_v
        basis.append(vector)
    return basis

def gen_v(n, t):
    rand_vs = []
    while len(rand_vs) < n + 2:
        rand_v = np.random.randint(0, 100, size=t)
        rand_vs.append(rand_v)
        rand_vs = gram_schmidt(rand_vs)
    return rand_vs


def main():
    n = int(input('Введите количество участников. n = '))
    m = int(input('Введите минимальное количество участников для раскрытия секрета. m = '))
    V = gen_v(n, m)
    U = V[0]
    V = V[1:]

    print('U:', U, '\n')
    for i, vector in enumerate(V):
        print(f"V{i}: {vector}")


    M = np.matmul(U, V[0])
    print('\nСекрет: M =', M, '\n')

    print('\n')
    A_i = []
    for i in range(1, len(V)):
        A_i.append(np.dot(U, V[i]))
        print(f"A{i}: {A_i[i-1]}")


    all_members = list(range(1, n))
    members = []
    matrix = []
    vector = []
    for _ in range(m):
        x = rand.choice(all_members)
        matrix.append(V[x])
        vector.append(A_i[x-1])
        members.append(x)
        all_members.remove(x)

    print(m, 'случайных участников:', members, '\n')
    print('Полученная СЛУ:')
    for i in range(m):
        for j in range(m):
            print(matrix[i][j], end = ' ')
        print(vector[i])
    
    #TRY
    res = np.linalg.solve(matrix, vector)
    #print(res)
    res = [round(x) for x in res]
    print('\nРешение СЛУ:', res)
    UV0 = round(np.matmul(res, V[0]))

    print('\nВычисленный секрет:', UV0)


main()