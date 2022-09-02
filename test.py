import random
import numpy as np
import json
import time
import seaborn as sns
import matplotlib.pyplot as plt
from main import word_process

"""
    побираю вероятности, следуя формуле: p_i = c * (q + i)**(-theta)
    её на паре дали АС, ПИ, а им АП
    ограничения: 0 < q0 < 40; 0 < theta < 1
    (upd оказалось, что для текстов в 25000 слов theta < 0.5 смысла не имеет так что в программе theta >= 0.5)
    q, theta подбираю сам, c восстанавливаю по ним так, чтобы сумма p_i равнялась 1
"""
start_time = time.time()

N = 25000  # примерное кол-во слов в ЕО
q, theta = 1, 0.99
test_stat_proc = []  # разные статистики при фиксированных q, theta, по ним строим гистограмму

for i in range(1000):
    distr_prob = []  # вероятности слов, из формулы => p_1 > p_2 > ... > p_N
    sum_prob = 0  # нужно чтобы подобрать константу c (по сути c = 1/sum_prob)
    for j in range(N):
        sum_prob += (q + j) ** (-theta)

    for j in range(N):
        p_j = ((q + j) ** (-theta)) / sum_prob
        distr_prob.append(p_j)

    """
        для данного теста слово = число
        далее предполагаю, что есть словарь (dictionary) на 25000 разных слов(чисел)
        больше не надо, т.к. в тексте не м.б. > 25000 слов
        вероятность появления числа(слова) i в тестовом тексте(test_txt) = p_i
        далее нахожу кол-во слов, встретившихся ровно один раз, и считаю статистику
    """

    dictionary = []
    for j in range(N):
        dictionary.append(j)

    test_txt = random.choices(dictionary, weights=distr_prob, k=N)

    # создаю файл со словами из test_txt (он нужен, т.к. функция word_process ожидает текстовый файл, а не массив
    with open('file.txt', 'w') as fw:
        json.dump(test_txt, fw)
    fw.close()

    R_n, R_n1, R_n_prime, R_n1_prime = word_process('file.txt')

    test_stat = 0
    for j in range(N):
        test_stat += R_n1[j] - R_n1_prime[j]
    test_stat = test_stat / (N * np.sqrt(R_n1[len(R_n) - 1]))

    test_stat_proc.append(test_stat)

"""
    далее нормирую test_stat_proc, если правильно понял нужно отнять среднее арифметичское
    затем поделить на отклонение
"""

mean = sum(test_stat_proc) / len(test_stat_proc)
st_dev = np.std(test_stat_proc)
renormed=[]
for i in test_stat_proc:
    renormed.append((i - mean) / st_dev)

test_stat_proc = renormed

print("--- %s seconds ---" % (time.time() - start_time))

x = np.sort(test_stat_proc)
y = np.arange(len(x)) / float(len(x))
plt.plot(x, y)  # тут график емпирического чего-то

plt.show(block=True)

# sns.displot(test_stat_proc) # тут гистограмма плотности
# sns.displot(test_stat_proc, kind="kde") # тут гладкий график плотности
