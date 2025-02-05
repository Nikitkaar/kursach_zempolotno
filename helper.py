from math import radians

import numpy as np
import math


class AutoCADLines_0():
    def __init__(self, scale_factor=100, **kwargs):
        # Пример использования функции
        self.w10 = 16
        self.H = 3.4
        self.hp = self.interpolate_hp()

        self.h10 = 0.23 + 0.11 * self.H
        self.h20 = 0.23 + 0.22 * self.H

        self.λ = self.interpolate_lambda()
        print(f"Значение λ для hp = {self.hp} и W10 = {self.w10} λ = {self.λ}")
        self.B = 2.1
        self.D = 5 * self.B
        self.Ksh = 0.5
        self.m = 2
        self.β = 35
        self.hn = (((2 * self.Ksh * self.hp) / self.m) * (self.λ / self.hp)
                   ** (1 / 3) * ((1 + 2 * math.sin(radians(self.β))) / 3))
        self.Knag = 0.009
        self.g = 9.81
        self.ΔZ = self.Knag * self.w10 * self.w10 * self.D * math.cos(radians(self.β)) / (3 * self.g * self.H)
        self.ynuv = 69.5        self.ynuv = 69.5
        self.a = 0.25
        self.yyk = self.ynuv + self.hn + self.ΔZ + self.a
        self.k3 = 1.5
        self.n = 0.025
        self.yk = 2.6
        self.yvodi = 1

        self.Qk = (self.k3 * self.n * self.yk * self.hp * self.hp * self.λ) / (((self.yk / self.yvodi) - 1)
                                                                               ** (1 / 3) * (1 + self.m) ** (1 / 2))
        self.Dcp = 1.24 * ((self.Qk / self.yk) ** (1 / 3))
        self.t1 = 2.5 * ((self.Qk / self.yk) ** (1 / 3))
        self.qk = 0.05 * self.Qk
        self.dcp = 1.24 * ((self.qk / self.yk) ** (1 / 3))
        self.t2 = 2.5 * ((self.qk / self.yk) ** (1 / 3))
        self.Vd = 1.37 * ((self.g * self.Dcp) ** (1 / 2))

        self.table = {
            0.5: {8: 5.6, 12: 5.5, 16: 5.4, 20: 5.3},
            0.75: {8: 9.1, 12: 8.8, 16: 8.5, 20: 8.3},
            1.00: {8: 12.8, 12: 12.3, 16: 11.7, 20: 11.4},
            1.25: {8: 16.6, 12: 15.8, 16: 15.1, 20: 14.4}
        }

    def interpolate_hp(self):
        # Определяем граничные значения
        self.w10_1 = 10
        self.w10_2 = 20

        # Значения hp для граничных w10
        self.hp_10 = 0.23 + 0.11 * self.H
        self.hp_20 = 0.23 + 0.22 * self.H

        # Линейная интерполяция
        if self.w10 < self.w10_1:
            self.hp = self.hp_10 + (self.hp_10 - (self.hp_10 - self.hp_20) * ((self.w10_1 - self.w10) /
                                                                              (self.w10_1 - self.w10_2)))
        elif self.w10 > self.w10_2:
            self.hp = self.hp_20 + (self.hp_20 - (self.hp_20 - self.hp_10) * ((self.w10 - self.w10_2) /
                                                                              (self.w10_2 - self.w10_1)))
        else:  # w10 между 10 и 20
            self.hp = self.hp_10 + (self.hp_20 - self.hp_10) * ((self.w10 - self.w10_1) / (self.w10_2 - self.w10_1))

        return self.hp

    # Создаем словарь из таблицы


    # Функция для интерполяции значения λ
    def interpolate_lambda(self):
        hp_values = sorted(self.table.keys())
        w10_values = sorted(self.table[hp_values[0]].keys())

        # Находим ближайшие значения hp и w10 в таблице
        hp_index = np.searchsorted(self.hp_values, self.hp)
        w10_index = np.searchsorted(self.w10_values, self.w10)

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

        lambda_lower_lower = self.table[hp_lower][w10_lower]
        lambda_lower_upper = self.table[hp_lower][w10_upper]
        lambda_upper_lower = self.table[hp_upper][w10_lower]
        lambda_upper_upper = self.table[hp_upper][w10_upper]

        lambda_lower = (lambda_lower_lower + (lambda_lower_upper - lambda_lower_lower) *
                        (self.w10 - w10_lower) / (w10_upper - w10_lower))
        lambda_upper = (lambda_upper_lower + (lambda_upper_upper - lambda_upper_lower) *
                        (self.w10 - w10_lower) / (w10_upper - w10_lower))

        lambda_value = (lambda_lower + (lambda_upper - lambda_lower) *
                        (self.hp - hp_lower) / (hp_upper - hp_lower))

        return lambda_value





