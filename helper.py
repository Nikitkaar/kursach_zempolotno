from math import radians

import numpy as np
import math


def interpolate_hp(w10, H):
    # Определяем граничные значения
    w10_1 = 10
    w10_2 = 20

    # Значения hp для граничных w10
    hp_10 = 0.23 + 0.11 * H
    hp_20 = 0.23 + 0.22 * H

    # Линейная интерполяция
    if w10 < w10_1:
        hp = hp_10 + (hp_10 - (hp_10 - hp_20) * ((w10_1 - w10) / (w10_1 - w10_2)))

    elif w10 > w10_2:
        hp = hp_20 + (hp_20 - (hp_20 - hp_10) * ((w10 - w10_2) / (w10_2 - w10_1)))
    else:  # w10 между 10 и 20
        hp = hp_10 + (hp_20 - hp_10) * ((w10 - w10_1) / (w10_2 - w10_1))

    return hp
# Создаем словарь из таблицы
table = {
    0.5: {8: 5.6, 12: 5.5, 16: 5.4, 20: 5.3},
    0.75: {8: 9.1, 12: 8.8, 16: 8.5, 20: 8.3},
    1.00: {8: 12.8, 12: 12.3, 16: 11.7, 20: 11.4},
    1.25: {8: 16.6, 12: 15.8, 16: 15.1, 20: 14.4}
}
# Функция для интерполяции значения λ
def interpolate_lambda(hp, w10):
    hp_values = sorted(table.keys())
    w10_values = sorted(table[hp_values[0]].keys())

    # Находим ближайшие значения hp и w10 в таблице
    hp_index = np.searchsorted(hp_values, hp)
    w10_index = np.searchsorted(w10_values, w10)

    # Если значения находятся на границах таблицы, возвращаем соответствующее значение λ
    if hp_index == 0:
        hp_index = 1
    if w10_index == 0:
        w10_index = 1
    if hp_index == len(hp_values):
        hp_index = len(hp_values) - 1
    if w10_index == len(w10_values):
        w10_index = len(w10_values) - 1

    # Интерполируем значение λ
    hp_lower = hp_values[hp_index - 1]
    hp_upper = hp_values[hp_index]
    w10_lower = w10_values[w10_index - 1]
    w10_upper = w10_values[w10_index]

    lambda_lower_lower = table[hp_lower][w10_lower]
    lambda_lower_upper = table[hp_lower][w10_upper]
    lambda_upper_lower = table[hp_upper][w10_lower]
    lambda_upper_upper = table[hp_upper][w10_upper]

    lambda_lower = lambda_lower_lower + (lambda_lower_upper - lambda_lower_lower) * (w10 - w10_lower) / (w10_upper - w10_lower)
    lambda_upper = lambda_upper_lower + (lambda_upper_upper - lambda_upper_lower) * (w10 - w10_lower) / (w10_upper - w10_lower)

    lambda_value = lambda_lower + (lambda_upper - lambda_lower) * (hp - hp_lower) / (hp_upper - hp_lower)

    return lambda_value

# Пример использования функции
w10 = 16
H = 3.4
hp = interpolate_hp(w10, H)

h10 = 0.23 + 0.11 *H
h20 = 0.23 +  0.22*H

λ = interpolate_lambda(hp, w10)
print(f"Значение λ для hp = {hp} и W10 = {w10} λ = {λ}")
B = 2.1
D =5 * B
Ksh = 0.5
m=2
β = 35
hn=((2*Ksh*hp)/m)*(λ/hp)**(1/3)*((1+2*math.sin(radians(β)))/3)
Knag = 0.009
g = 9.81
ΔZ = Knag * w10 * w10 * D * math.cos(radians(β))/(3*g*H)
ynuv = 69.5
a = 0.25
yyk = ynuv + hn + ΔZ +a
k3 =1.5
n = 0.025
yk=2.6
yvodi = 1

Qk= (k3*n*yk*hp*hp*λ)/(((yk/yvodi)-1)**(1/3)* (1+m)**(1/2))
Dcp = 1.24*((Qk/yk)**(1/3))
t1 = 2.5*((Qk/yk)**(1/3))
qk=0.05*Qk
dcp = 1.24*((qk/yk)**(1/3))
t2 = 2.5*((qk/yk)**(1/3))
Vd = 1.37*((g*Dcp)**(1/2))




