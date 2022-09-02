import numpy as np
from scipy.stats import norm
from math import gamma


# тут ищем слова, встретившиеся ровно один раз и уникальные слова (с начала и с конца)
def word_process(txt_name):
    parsed_text = open(txt_name)

    unique_words_rev = set()
    unique_proc_rev = []
    unique_words = set()
    unique_proc = []

    once_words_rev = []
    once_words = []
    once_proc_rev = []
    once_proc = []

    unique_counter_rev = 0
    unique_counter = 0
    once_counter_rev = 0
    once_counter = 0

    words = parsed_text.read().split(" ")  # тут можно добавить запятую перед пробелом
    rev_words = words.copy()
    rev_words.reverse()

    # прямой подсчет уникальных и единственных слов (R)
    for word in words:
        if word not in unique_words:
            unique_words.add(word)
            once_words.append(word)
            unique_counter += 1
            unique_proc.append(unique_counter)
            once_counter += 1
            once_proc.append(once_counter)
        else:
            unique_proc.append(unique_counter)
            if word in once_words:
                once_words.remove(word)
                once_counter -= 1
                once_proc.append(once_counter)
            else:
                once_proc.append(once_counter)

    # обратный подсчет уникальных и единственных слов (R')
    for word in rev_words:
        if word not in unique_words_rev:
            unique_words_rev.add(word)
            once_words_rev.append(word)
            unique_counter_rev += 1
            unique_proc_rev.append(unique_counter_rev)
            once_counter_rev += 1
            once_proc_rev.append(once_counter_rev)
        else:
            unique_proc_rev.append(unique_counter_rev)
            if word in once_words_rev:
                once_words_rev.remove(word)
                once_counter_rev -= 1
                once_proc_rev.append(once_counter_rev)
            else:
                once_proc_rev.append(once_counter_rev)
    parsed_text.close()

    return unique_proc, once_proc, unique_proc_rev, once_proc_rev


# corollary 4.2, вынес в отдельную ф-ию т.к. используется в обоих p-value
def theta_hat(unique_proc, unique_proc_rev):
    word_amount = len(unique_proc)
    return np.log2(unique_proc[word_amount - 1] / np.sqrt(
        unique_proc[(word_amount - 1) // 2] * unique_proc_rev[(word_amount - 1) // 2]))


# p-value для уникальных слов (выводы из corollary 4.1)
def unique_p_value(txt_name):
    # по сути здесь once_proc, once_proc_rev не нужны, просто не нашел как взять лишь часть возвращаемых аргументов
    unique_proc, once_proc, unique_proc_rev, once_proc_rev = word_process(txt_name)
    word_amount = len(unique_proc)  # тут неважно что возьмем, т.к. длины списков одинаковы

    j_obs = 0
    for i in range(word_amount):
        j_obs += unique_proc[i] - unique_proc_rev[i]
    j_obs = abs(j_obs / (word_amount * np.sqrt(unique_proc[word_amount - 1])))

    theta = theta_hat(unique_proc, unique_proc_rev)
    return 1 - norm.cdf(j_obs * np.sqrt(1 + 2 / theta))
