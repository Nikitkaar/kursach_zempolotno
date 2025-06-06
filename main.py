import math
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

import numpy as np
from pyautocad import Autocad, APoint  # Импортируйте необходимые классы из библиотеки Autocad

from initial_data import WordEquationReplacer
from autocad import AutoCADLines, AutoCADLines_1



class App:
    def __init__(self, root):
        print("Инициализация началась")
        self.root = root
        self.root.title("Ввод данных")


        # Создание виджета Canvas для прокрутки
        self.canvas = tk.Canvas(root)
        self.scroll_y = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # Добавление обработчика события прокрутки мыши
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Создание полей ввода
        self.entries = {}
        entry_labels = [
            "Высота насыпи Н, м",
            "Показатель крутизны откосов n, -",
            "толщина слоя балластных материалов, hбм, м",
            "Показатель текучести WL",
            "Показатель кривизны кривой, Kt",

            "yb=",
            "ynuv=",
            "B=",
            "H_1=",
            "W10 =",
            "β=",
            "Vv=",
        ]

        # Добавление полей ввода в три столбца с выбором для определенных полей
        for index, label in enumerate(entry_labels):
            ttk.Label(self.scrollable_frame, text=label + ":").grid(row=index, column=0, sticky="w", pady=5)
            entry = ttk.Entry(self.scrollable_frame)
            #if label == "redaction":
                #entry = ttk.Combobox(self.scrollable_frame, values=["new", "old"])
            #elif label == "rail_type":
                #entry = ttk.Combobox(self.scrollable_frame, values=["Р65", "Р50"])
            #elif label == "material_of_sleepers":
                #entry = ttk.Combobox(self.scrollable_frame, values=["Дерево", "Железобетон"])
            #else:
                #entry = ttk.Entry(self.scrollable_frame)

            entry.grid(row=index, column=1, pady=5)
            entry.bind('<Return>', self.focus_next)  # Привязка клавиши Enter к функции
            self.entries[label] = entry  # Сохраняем ссылки на поля ввода

        # Кнопка для копирования значений
        self.copy_button = ttk.Button(self.scrollable_frame, text="Скопировать", command=self.copy_to_clipboard)
        self.copy_button.grid(row=len(entry_labels) + 1, column=0, columnspan=2, pady=5)

        # Кнопка для вставки значений
        self.paste_button = ttk.Button(self.scrollable_frame, text="Вставить", command=self.paste_from_clipboard)
        self.paste_button.grid(row=len(entry_labels) + 2, column=0, columnspan=2, pady=5)

        # Кнопка для подтверждения ввода
        self.confirm_button = ttk.Button(self.scrollable_frame, text="Подтвердить", command=self.confirm)
        self.confirm_button.grid(row=len(entry_labels), column=0, columnspan=2, pady=20)
        # Устанавливаем размер окна (ширина x высота)
        self.root.geometry("500x600")  # Значение можно изменить по вашему желанию
        print("Инициализация закончилась")

    def on_mouse_wheel(self, event):
        """Обработка прокрутки колесика мыши"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")  # Прокрутка на 1 единицу



    def focus_next(self, event):
        """Переход к следующему полю ввода"""
        current_widget = event.widget
        current_widget_index = list(self.entries.values()).index(current_widget)

        # Переход к следующему полю ввода
        next_widget = list(self.entries.values())[(current_widget_index + 1) % len(self.entries)]
        next_widget.focus_set()

    def copy_to_clipboard(self):
        """Копирует значения из полей ввода в буфер обмена"""
        clipboard_data = "\n".join([f"{label}: {entry.get()}" for label, entry in self.entries.items()])
        self.root.clipboard_clear()
        self.root.clipboard_append(clipboard_data)
        messagebox.showinfo("Копирование", "Данные скопированы в буфер обмена.")

    def paste_from_clipboard(self):
        """Вставляет значения из буфера обмена в поля ввода"""
        clipboard_data = self.root.clipboard_get().strip().split('\n')
        for line, label in zip(clipboard_data, self.entries.keys()):
            try:
                key, value = line.split(':', 1)
                if key.strip() == label:
                    self.entries[label].delete(0, tk.END)  # Очистить текущее значение
                    self.entries[label].insert(0, value.strip())  # Вставить новое значение
            except ValueError:
                continue  # Игнорируем строки, которые не в формате "label: value"

    def confirm(self):
        print("Инициализация давно закончилась")
        # Считываем значения из полей ввода в глобальный словарь
        data = {}
        for field, entry in self.entries.items():
            value = entry.get().strip()  # Убираем пробелы

            if field in ["Высота насыпи Н, м",
            "Показатель крутизны откосов n, -",
            "толщина слоя балластных материалов, hбм, м",
            "Показатель текучести WL",
            "Показатель кривизны кривой, Kt", "yb=", "ynuv=", "B=", "H_1=", "W10 =", "β=", "Vv="]:
                # Преобразуем числовые значения
                try:
                    if field in ["Высота насыпи Н, м",
            "Показатель крутизны откосов n, -",
            "толщина слоя балластных материалов, hбм, м",
            "Показатель текучести WL",
            "Показатель кривизны кривой, Kt", "yb=", "ynuv=", "B=", "H_1=", "W10 =", "β=", "Vv="]:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    messagebox.showwarning("Ошибка", f"Введите корректное числовое значение для {field}.")
                    return

            data[field] = value  # Сохраняем значения

        # Формирование итоговых переменных
        ## Константы первая часть
        """Ширина первого отсека, м:"""
        b0 = x1 = 2.2
        """Ширина основной площадки земполотна, м:"""
        B = 7.0
        """Объемный вес грунта, т\м^3:"""
        p = 2
        """Длинна шпалы, м:"""
        lш = 2.7
        """Вес воды:"""
        p_vodi = 1

        # Начал вторую часть но передумал, так как логичнее это посестить в переменные экземпляра
        "чет типа запаса высоты уровня низовой бермы над водой(для второго чертежа:"
        self.a=0.25
        self.Ksh = 0.5
        self.m = 2
        self.Knag = 0.009
        self.gg = 9.81
        self.yk = 2.6

        self.k3 = 1.5
        self.nn = 0.025
        self.yvodi = 1

        ## ВВодимс
        self.H = data["Высота насыпи Н, м"]
        self.n = data["Показатель крутизны откосов n, -"]
        self.hбм = data["толщина слоя балластных материалов, hбм, м"]
        self.WL = data["Показатель текучести WL"]
        self.Kt = data["Показатель кривизны кривой, Kt"]

        self.yb = data["yb="]
        self.ynuv = data["ynuv="]
        self.B = data["B="]
        self.H_1 = data["H_1="]
        self.W10 = data["W10 ="]
        self.β = data["β="]
        self.Vv = data["Vv="]

        self.horda_2d = math.sqrt(((self.H - self.hбм) ** 2 + (self.n * self.H + x1) ** 2))
        self.d = self.horda_2d / 2
        self.dsqrt = self.d * self.d

        self.t = self.Kt * self.H
        self.R = (self.d ** 2 + self.t ** 2) / (2 * self.t)
        self.α = math.asin((self.H - self.hбм) / self.horda_2d)

        self.α_degrees = math.degrees(self.α)
        # print(f"Угол в радианах: {self.α_degrees}")

        self.μ = math.asin(self.d / self.R)
        self.μ_degrees = math.degrees(self.μ)

        self.XR = round(self.n * self.H + x1 + self.R * math.sin(self.α - self.μ), 2)
        self.YR = round(self.R * math.cos(self.α - self.μ), 2)
        self.N = self.find_max_N()
        self.b1 = self.n * self.H / self.N

        self.xn1 = b0
        self.xn2 = self.xn1 + self.b1
        self.xn3 = self.xn2 + self.b1
        self.xn4 = self.xn3 + self.b1
        self.xn5 = self.xn4 + self.b1
        self.xn6 = 0
        self.xn7 = 0
        if self.N > 4:
            self.xn6 = self.xn5 + self.b1
            if self.N > 5:
                self.xn7 = self.xn6 + self.b1


        self.xcp0 = b0 / 2
        self.xcp1 = (self.xn2 + self.xn1) / 2
        self.xcp2 = (self.xn3+ self.xn2) / 2
        self.xcp3 = (self.xn4+ self.xn3) / 2
        self.xcp4 = (self.xn5+ self.xn4) / 2
        self.xcp5 = 0
        self.xcp6 = 0
        if self.N > 4:
            self.xcp5 = (self.xn6 + self.xn5) / 2
            if self.N > 5:
                self.xcp6 = (self.xn7 + self.xn6) / 2


        self.β0 = math.asin((self.XR - self.xcp0) / self.R)
        self.β1 = math.asin((self.XR - self.xcp1) / self.R)
        self.β2 = math.asin((self.XR - self.xcp2) / self.R)
        self.β3 = math.asin((self.XR - self.xcp3) / self.R)
        self.β4 = math.asin((self.XR - self.xcp4) / self.R)
        self.β5 = 0
        self.β6 = 0
        if self.N > 4:
            self.β5 = math.asin((self.XR - self.xcp5) / self.R)

            if self.N > 5:
                self.β6 = math.asin((self.XR - self.xcp6) / self.R)

        self.yп1 = self.H
        self.yп2 = self.H - ((self.xcp1 - x1) / self.n)
        self.yп3 = self.H - ((self.xcp2 - x1) / self.n)
        self.yп4 = self.H - ((self.xcp3 - x1) / self.n)
        self.yп5 = self.H - ((self.xcp4 - x1) / self.n)
        self.yп6 = 0
        self.yп7 = 0
        if self.N > 4:
            self.yп6 = self.H - ((self.xcp5 - x1) / self.n)
            if self.N > 5:
                self.yп7 = self.H - ((self.xcp6 - x1) / self.n)

        self.yk0 = self.YR - self.R * math.cos(math.radians(math.degrees(self.β0)))
        self.yk1 = self.YR - self.R * math.cos(self.β1)
        self.yk2 = self.YR - self.R * math.cos(self.β2)
        self.yk3 = self.YR - self.R * math.cos(self.β3)
        self.yk4 = self.YR - self.R * math.cos(self.β4)
        self.yk5 = 0
        self.yk6 = 0
        if self.N > 4:
            self.yk5 = self.YR - self.R * math.cos(self.β5)
            if self.N > 5:
                self.yk6 = self.YR - self.R * math.cos(self.β6)

        self.h0 = self.yп1 - self.yk0
        self.h1 = self.yп2 - self.yk1
        self.h2 = self.yп3 - self.yk2
        self.h3 = self.yп4 - self.yk3
        self.h4 = self.yп5 - self.yk4
        self.h5 = 0
        self.h6 = 0
        if self.N > 4:
            self.h5 = self.yп6 - self.yk5
            if self.N > 5:
                self.h6 = self.yп7 - self.yk6

        self.g0 = 2 * self.h0 * b0
        self.g1 = 2 * self.h1 * self.b1
        self.g2 = 2 * self.h2 * self.b1
        self.g3 = 2 * self.h3 * self.b1
        self.g4 = 2 * self.h4 * self.b1
        self.g5 = 0
        self.g6 = 0
        if self.N > 4:
            self.g5 = 2 * self.h5 * self.b1
            if self.N > 5:
                self.g6 = 2 * self.h6 * self.b1

        self.Cpr0 = float(input(f"Введите значение Спр для WL = {self.WL} и h0 = {self.h0}"))
        self.Cpr1 = float(input(f"Введите значение Спр для WL = {self.WL} и h1 = {self.h1}"))
        self.Cpr2 = float(input(f"Введите значение Спр для WL = {self.WL} и h2 = {self.h2}"))
        self.Cpr3 = float(input(f"Введите значение Спр для WL = {self.WL} и h3 = {self.h3}"))
        self.Cpr4 = float(input(f"Введите значение Спр для WL = {self.WL} и h4 = {self.h4}"))
        self.Cpr5 = float(input(f"Введите значение Спр для WL = {self.WL} и h5 = {self.h5}"))
        self.Cpr6 = float(input(f"Введите значение Спр для WL = {self.WL} и h6 = {self.h6}"))

        self.φ = (float(input(f"Введите значение φ =")))

        #self.Cpr0 = 1.20
        #self.Cpr1 = 1.72
        #self.Cpr2 = 1.82
        #self.Cpr3 = 1.73
        #self.Cpr4 = 1.39
        #self.Cpr5 = 1.73
        #self.Cpr6 = 0.70
        #self.φ = 18.2

        self.f = math.tan(math.radians(self.φ - 2))

        self.Tydc0 = self.Cpr0 * b0 / math.cos(self.β0)
        self.Tydc1 = self.Cpr1 * self.b1 / math.cos(self.β1)
        self.Tydc2 = self.Cpr2 * self.b1 / math.cos(self.β2)
        self.Tydc3 = self.Cpr3 * self.b1 / math.cos(self.β3)
        self.Tydc4 = self.Cpr4 * self.b1 / math.cos(self.β4)
        self.Tydc5 = 0
        self.Tydc6 = 0

        self.Tydf0 = self.f * self.g0 * math.cos(self.β0)
        self.Tydf1 = self.f * self.g1 * math.cos(self.β1)
        self.Tydf2 = self.f * self.g2 * math.cos(self.β2)
        self.Tydf3 = self.f * self.g3 * math.cos(self.β3)
        self.Tydf4 = self.f * self.g4 * math.cos(self.β4)
        self.Tydf5 = 0
        self.Tydf6 = 0

        self.Tcd0 = self.g0 * math.sin(self.β0)
        self.Tcd1 = self.g1 * math.sin(self.β1)
        self.Tcd2 = self.g2 * math.sin(self.β2)
        self.Tcd3 = self.g3 * math.sin(self.β3)
        self.Tcd4 = self.g4 * math.sin(self.β4)
        self.Tcd5 = 0
        self.Tcd6 = 0

        if self.N > 4:
            self.g5 = 2 * self.h5 * self.b1
            self.Tydc5 = self.Cpr5 * self.b1 / math.cos(self.β5)
            self.Tcd5 = self.g5 * math.sin(self.β5)
            self.Tydf5 = self.f * self.g5 * math.cos(self.β5)
            if self.N > 5:
                self.g6 = 2 * self.h6 * self.b1
                self.Tydc6 = self.Cpr6 * self.b1 / math.cos(self.β6)
                self.Tcd6 = self.g6 * math.sin(self.β6)
                self.Tydf6 = self.f * self.g6 * math.cos(self.β6)
        self.ΣTydc = self.Tydc0 + self.Tydc1 + self.Tydc2 + self.Tydc3 + self.Tydc4 + self.Tydc5 + self.Tydc6
        self.ΣTydf = self.Tydf0 + self.Tydf1 + self.Tydf2 + self.Tydf3 + self.Tydf4 + self.Tydf5 + self.Tydf6
        self.ΣTcd = self.Tcd0 + self.Tcd1 + self.Tcd2 + self.Tcd3 + self.Tcd4+ + self.Tcd5 + self.Tcd6

        self.Km = (self.ΣTydc + self.ΣTydf) / (
        self.ΣTcd + (p_vodi * (max(self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6)) ** 2) / 2)


        # Начинаем расчеты второй части

        self.hp = self.interpolate_hp()

        self.h10 = 0.23 + 0.11 * self.H_1
        self.h20 = 0.23 + 0.22 * self.H_1

        self.λ = self.interpolate_lambda()

        self.D = 5 * self.B
        self.hn = (((2 * self.Ksh * self.hp) / self.m) * (self.λ / self.hp)
                   ** (1 / 3) * ((1 + 2 * math.sin(math.radians(self.β))) / 3))
        self.ΔZ = self.Knag * self.W10 * self.W10 * self.D * math.cos(math.radians(self.β)) / (3 * self.gg * self.H)
        self.yyk = (self.ynuv + self.hn + self.ΔZ + self.a)/100
        self.Qk = (self.k3 * self.nn * self.yk * self.hp * self.hp * self.λ) / (((self.yk / self.yvodi) - 1)
                                                                               ** (1 / 3) * (1 + self.m) ** (1 / 2))
        self.Dcp = 1.24 * ((self.Qk / self.yk) ** (1 / 3))
        self.t1 = 2.5 * ((self.Qk / self.yk) ** (1 / 3))
        self.qk = 0.05 * self.Qk
        self.dcp = 1.24 * ((self.qk / self.yk) ** (1 / 3))
        self.t2 = 2.5 * ((self.qk / self.yk) ** (1 / 3))
        self.Vd = 1.37 * ((self.gg * self.Dcp) ** (1 / 2))


        messagebox.showinfo("Успех", "Все данные успешно введены!")

        self.root.destroy()  # Закрыть окно после подтверждения
        self.root.quit()  # Завершает цикл обработки событий Tkinter

        print(f'horda={self.horda_2d}\n'
              f'd={self.d}\nt={self.t}\n'
              f'R={self.R}\nα={self.α}\n'
              f'μ={self.μ}\n'
              f'XR={self.XR}\n'
              f'XY={self.YR}\n'
              f'N={self.N}\n'
              f'b={self.b1}\n'
              f'find_max_N={self.find_max_N}\n'
              f'xn1={self.xn1}\n'
              f'xn2={self.xn2}\n'
              f'xn3={self.xn3}\n'
              f'xn4={self.xn4}\n'
              f'xn5={self.xn5}\n'
              f'xcp0={self.xcp0}\n'
              f'xcp1={self.xcp1}\n'
              f'xcp2={self.xcp2}\n'
              f'xcp3={self.xcp3}\n'
              f'xcp4={self.xcp4}\n'
              
              f'β0={self.β0}\n'
              f'β1={self.β1}\n'
              f'β2={self.β2}\n'
              f'β3={self.β3}\n'
              f'β4={self.β4}\n'
              f'β5={self.β5}\n'
              
              f'yп1={self.yп1}\n'
              f'yп2={self.yп2}\n'
              f'yп3={self.yп3}\n'
              f'yп4={self.yп4}\n'
              f'yп5={self.yп5}\n'
              f'yk0={self.yk0}\n'
              f'yk1={self.yk1}\n'
              f'yk2={self.yk2}\n'
              f'yk3={self.yk3}\n'
              f'yk4={self.yk4}\n'
              f'yk5={self.yk5}\n'
              f'h0={self.h0}'
              f'h1={self.h1}\n'
              f'h2={self.h2}\n'
              f'h3={self.h3}\n'
              f'h4={self.h4}\n'
              f'h5={self.h5}\n'
              f'g0={self.g0}\n'
              f'g1={self.g1}\n'
              f'g2={self.g2}\n'
              f'g3={self.g3}\n'
              f'g4={self.g4}\n'
              f'g5={self.g5}\n'
              f'Cpr0={self.Cpr0}\n'
              f'Cpr1={self.Cpr1}\n'
              f'Cpr2={self.Cpr2}\n'
              f'Cpr3={self.Cpr3}\n'
              f'Cpr4={self.Cpr4}\n'
              f'Cpr5={self.Cpr5}\n'
              f'φ={self.φ}\nf={self.f}\n'
              f'Tydc0={self.Tydc0}\n'
              f'Tydc1={self.Tydc1}\n'
              f'Tydc2={self.Tydc2}\n'
              f'Tydc3={self.Tydc3}\n'
              f'Tydc4={self.Tydc4}\n'
              f'Tydc5={self.Tydc5}\n'
              f'ΣTydc={self.ΣTydc}\n'
              f'Tydf0={self.Tydf0}\n'
              f'Tydf1={self.Tydf1}\n'
              f'Tydf2={self.Tydf2}\n'
              f'Tydf3={self.Tydf3}\n'
              f'Tydf4={self.Tydf4}\n'
              f'Tydf5={self.Tydf5}\n'
              f'ΣTydf={self.ΣTydf}\n'
              f'Tcd0={self.Tcd0}\n'
              f'Tcd1={self.Tcd1}\n'
              f'Tcd2={self.Tcd2}\n'
              f'Tcd3={self.Tcd3}\n'
              f'Tcd4={self.Tcd4}\n'
              f'Tcd5={self.Tcd5}\n'
              f'ΣTcd={self.ΣTcd}\n'
              f'Km={self.Km}\n\n\n'
              f'hp={self.hp}\n'
              f'ynuv={self.ynuv}\n'
              f'B={self.B}\n'
              f'W10={self.W10}\n'
              f'λ={self.λ}\n'
              f'D={self.D}\n'
              f'hn={self.hn}\n'
              f'yyk={self.yyk}\n'
              f'yk={self.yk}\n')


        autocader_1 = AutoCADLines_1(100,
                                     H=self.H_1,
                                     hp=self.hp,
                                     yb=self.yb,
                                     ynuv=self.ynuv,
                                     B=self.B,
                                     W10=self.W10,
                                     β=self.β,
                                     Vv=self.Vv,
                                     h10=self.h10,
                                     h20=self.h20,
                                     lam=self.λ,
                                     D=self.D,
                                     hn=self.hn,
                                     deltaZ=self.ΔZ,
                                     yyk=self.yyk,
                                     Qk=self.Qk,
                                     Dcp=self.Dcp,
                                     t1=self.t1,
                                     qk=self.qk,
                                     dcp=self.dcp,
                                     t2=self.t2,
                                     Vd=self.Vd,
                                     a=self.a,
                                     Ksh=self.Ksh,
                                     Knag=self.Knag,
                                     k3=self.k3,
                                     n=self.nn,
                                     arrow_size=0.5)
        autocader_1.draw_lines()

        # Создание экземпляра WordEquationReplacer
        replacer = WordEquationReplacer('Zapiska.docx',
                                        horda=f'{round(self.horda_2d,2)}',
                                        dd=f'{round(self.d,2)}',
                                        dsqrt=f'{round(self.dsqrt,2)}',
                                        HH=f'{round(self.H,2)}',
                                        nn=f"{round(self.n,2)}",
                                        hbm=f'{round(self.hбм,2)}',
                                        wl=f'{round(self.WL,2)}',
                                        kt=f'{round(self.Kt,2)}',
                                        b0=f'{b0}',  # Нужно убедиться, что это определено
                                        tt=f'{round(self.t,2)}',
                                        tsqrt=f'{round(self.t**2,2)}',
                                        αα=f'{round(self.α_degrees,3)}',  # Преобразование в градусы
                                        RR=f'{round(self.R,2)}',
                                        μμ=f'{round(self.μ_degrees,3)}',
                                        XR=f'{round(self.XR,2)}',
                                        YR=f'{round(self.YR,2)}',
                                        NN=f'{self.N}',
                                        b1=f'{round(self.b1,2)}',
                                        bOne=f'{round(self.b1, 2)}',
                                        xn1=f'{round(self.xn1,2)}',
                                        xn2=f'{round(self.xn2,2)}',
                                        xn3=f'{round(self.xn3,2)}',
                                        xn4=f'{round(self.xn4,2)}',
                                        xn5=f'{round(self.xn5,2)}',
                                        xn6=f'{round(self.xn6,2)}',
                                        xn7=f'{round(self.xn7, 2)}',

                                        xcp0=f'{round(self.xcp0,2)}',
                                        xcp1=f'{round(self.xcp1,2)}',
                                        xcp2=f'{round(self.xcp2,2)}',
                                        xcp3=f'{round(self.xcp3,2)}',
                                        xcp4=f'{round(self.xcp4,2)}',
                                        xcp5=f'{round(self.xcp5,2)}',
                                        xcp6=f'{round(self.xcp6, 2)}',

                                        β0=f'{round(math.degrees(self.β0),2)}',
                                        β1=f'{round(math.degrees(self.β1),2)}',
                                        β2=f'{round(math.degrees(self.β2),2)}',
                                        β3=f'{round(math.degrees(self.β3),2)}',
                                        β4=f'{round(math.degrees(self.β4),2)}',
                                        β5=f'{round(math.degrees(self.β5),2)}',
                                        β6=f'{round(math.degrees(self.β6), 2)}',

                                        yп1=f'{round(self.yп1,2)}',
                                        yп2=f'{round(self.yп2,2)}',
                                        yп3=f'{round(self.yп3,2)}',
                                        yп4=f'{round(self.yп4,2)}',
                                        yп5=f'{round(self.yп5,2)}',
                                        yп6=f'{round(self.yп6,2)}',
                                        yп7=f'{round(self.yп7, 2)}',

                                        yk0=f'{round(self.yk0,2)}',
                                        yk1=f'{round(self.yk1,2)}',
                                        yk2=f'{round(self.yk2,2)}',
                                        yk3=f'{round(self.yk3,2)}',
                                        yk4=f'{round(self.yk4,2)}',
                                        yk5=f'{round(self.yk5,2)}',
                                        yk6=f'{round(self.yk6, 2)}',

                                        h0=f'{round(self.h0,2)}',
                                        h1=f'{round(self.h1,2)}',
                                        h2=f'{round(self.h2,2)}',
                                        h3=f'{round(self.h3,2)}',
                                        h4=f'{round(self.h4,2)}',
                                        h5=f'{round(self.h5,2)}',
                                        h6=f'{round(self.h6, 2)}',

                                        g0=f'{round(self.g0,2)}',
                                        g1=f'{round(self.g1,2)}',
                                        g2=f'{round(self.g2,2)}',
                                        g3=f'{round(self.g3,2)}',
                                        g4=f'{round(self.g4,2)}',
                                        g5=f'{round(self.g5,2)}',
                                        g6=f'{round(self.g6, 2)}',

                                        Cpr0=f'{round(self.Cpr0,2)}',
                                        Cpr1=f'{round(self.Cpr1,2)}',
                                        Cpr2=f'{round(self.Cpr2,2)}',
                                        Cpr3=f'{round(self.Cpr3,2)}',
                                        Cpr4=f'{round(self.Cpr4,2)}',
                                        Cpr5=f'{round(self.Cpr5,2)}',
                                        Cpr6=f'{round(self.Cpr6, 2)}',

                                        Tydc0=f'{round(self.Tydc0,2)}',
                                        Tydc1=f'{round(self.Tydc1,2)}',
                                        Tydc2=f'{round(self.Tydc2,2)}',
                                        Tydc3=f'{round(self.Tydc3,2)}',
                                        Tydc4=f'{round(self.Tydc4,2)}',
                                        Tydc5=f'{round(self.Tydc5,2)}',
                                        Tydc6=f'{round(self.Tydc6, 2)}',
                                        ΣTydc=f'{round(self.ΣTydc,2)}',
                                        φφ=f'{round(self.φ,2)}',
                                        ff=f'{round(self.f,3)}',
                                        Tydf0=f'{round(self.Tydf0,2)}',
                                        Tydf1=f'{round(self.Tydf1,2)}',
                                        Tydf2=f'{round(self.Tydf2,2)}',
                                        Tydf3=f'{round(self.Tydf3,2)}',
                                        Tydf4=f'{round(self.Tydf4,2)}',
                                        Tydf5=f'{round(self.Tydf5,2)}',
                                        Tydf6=f'{round(self.Tydf6, 2)}',
                                        ΣTydf=f'{round(self.ΣTydf,2)}',

                                        Tcd0=f'{round(self.Tcd0,2)}',
                                        Tcd1=f'{round(self.Tcd1,2)}',
                                        Tcd2=f'{round(self.Tcd2,2)}',
                                        Tcd3=f'{round(self.Tcd3,2)}',
                                        Tcd4=f'{round(self.Tcd4,2)}',
                                        Tcd5=f'{round(self.Tcd5,2)}',
                                        Tcd6=f'{round(self.Tcd6, 2)}',
                                        ΣTcd=f'{round(self.ΣTcd,2)}',

                                        ρρ=f'{p_vodi}',  # Убедитесь, что p_vodi определено
                                        hhmax2=f'{round(max(self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6) ** 2, 2)}',
                                        km=f'{round(self.Km,3)}',


                                        gg = f'{self.gg}',
                                        H1 =f'{self.H_1}',
                                        hpp = f'{round(self.hp,2)}',
                                        hpp2 = f'{round(self.hp**2,2)}',
                                        yb=f'{self.yb}',
                                        ynuv= f'{self.ynuv}',
                                        BB= f'{self.B}',

                                        W100= f'{self.W10}',
                                        W102= f'{self.W10**2}',
                                        ββ= f'{self.β}',
                                        Vv= f'{self.Vv}',

                                        h100 = f'{round(self.h10,3)}',
                                        h200 = f'{round(self.h20,3)}',
                                        λλ = f'{round(self.λ,2)}',
                                        DD = f'{round(self.D,1)}',
                                        hn = f'{round(self.hn,2)}',
                                        ZZ = f'{round(self.ΔZ,2)}',
                                        yyk = f'{round(self.yyk,2)}',
                                        Qk = f'{round(self.Qk,2)}',
                                        Dcp = f'{round(self.Dcp,2)}',
                                        tt1 = f'{round(self.t1,2)}',
                                        qqk = f'{round(self.qk,3)}',
                                        dcp = f'{round(self.dcp,2)}',
                                        tt2 = f'{round(self.t2,2)}',
                                        Vd = f'{round(self.Vd,2)}',
                                        aa = f'{self.a}',
                                        Ksh = f'{self.Ksh}',
                                        Knag = f'{self.Knag}',

                                        k33 = f'{self.k3}',
                                        n2 = f'{self.nn}',
                                        yvody = f'{self.yvodi}',
                                        yk = f'{self.yk}'
                                        )


        """autocader = AutoCADLines(100, horda=self.horda_2d,
                                 d=self.d,
                                 dsqrt=self.dsqrt,
                                 H=self.H,
                                 n=self.n,
                                 hbm=self.hбм,
                                 wl=self.WL,
                                 kt=self.Kt,
                                 b0=b0,  # Нужно убедиться, что это определено
                                 t=self.t,
                                 tsqrt=self.t**2,
                                 α=self.α_degrees,  # Преобразование в градусы
                                 RR=self.R,
                                 μ=self.μ_degrees,
                                 XR=self.XR,
                                 YR=self.YR,
                                 NN=self.N,
                                 b1=self.b1,

                                 xn1=self.xn1,
                                 xn2=self.xn2,
                                 xn3=self.xn3,
                                 xn4=self.xn4,
                                 xn5=self.xn5,
                                 xn6=self.xn6,
                                 xn7=self.xn6,

                                 xcp0=self.xcp0,
                                 xcp1=self.xcp1,
                                 xcp2=self.xcp2,
                                 xcp3=self.xcp3,
                                 xcp4=self.xcp4,
                                 xcp5=self.xcp5,
                                 xcp6=self.xcp6,

                                 β0=math.degrees(self.β0),
                                 β1=math.degrees(self.β1),
                                 β2=math.degrees(self.β2),
                                 β3=math.degrees(self.β3),
                                 β4=math.degrees(self.β4),
                                 β5=math.degrees(self.β5),
                                 β6=math.degrees(self.β6),

                                 yп1=self.yп1,
                                 yп2=self.yп2,
                                 yп3=self.yп3,
                                 yп4=self.yп4,
                                 yп5=self.yп5,
                                 yп6=self.yп6,
                                 yп7=self.yп7,

                                 yk0=self.yk0,
                                 yk1=self.yk1,
                                 yk2=self.yk2,
                                 yk3=self.yk3,
                                 yk4=self.yk4,
                                 yk5=self.yk5,
                                 yk6=self.yk6,

                                 h0=self.h0,
                                 h1=self.h1,
                                 h2=self.h2,
                                 h3=self.h3,
                                 h4=self.h4,
                                 h5=self.h5,
                                 h6=self.h6,

                                 g0=self.g0,
                                 g1=self.g1,
                                 g2=self.g2,
                                 g3=self.g3,
                                 g4=self.g4,
                                 g5=self.g5,
                                 g6=self.g6,

                                 hhmax2=max(self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6) ** 2,
                                 km=self.Km,
                                 xnmax=max(self.xn1, self.xn2, self.xn3, self.xn4, self.xn5, self.xn6, self.xn7),
                                 arrow_size=0.5)
        autocader.draw_lines()"""


        # Обработка документа
        replacer.process_document()
        replacer.save_document('Черновая_заготовка_1.docx')

    def find_max_N(self):
        """
        Находит наибольшее целое N (N >= 4), при котором b <= 6,
        где b = (n * H) / N.

        Returns:
            int: Наибольшее целое N, удовлетворяющее условиям.
        """
        min_N = (self.n * self.H) / 6  # вычиление минимального значения
        min_N = math.ceil(min_N)  # округление в большую сторону
        N = max(4, int(min_N))  # проверка ограничений

        while True:  # поиск нужного значения N
            b = (self.n * self.H) / N
            if b > 6:  # если b больше 6
                N -= 1  # уменьшаем N, чтобы b стало меньше или равно 6
                if N < 4:  # если N меньше 4, выходим из цикла
                    break
            else:
                return N  # N удовлетворяет условию, возвращаем его

    def interpolate_hp(self):
        # Определяем граничные значения
        w10_1 = 10
        w10_2 = 20

        # Значения hp для граничных w10
        hp_10 = 0.23 + 0.11 * self.H_1
        hp_20 = 0.23 + 0.22 * self.H_1

        # Линейная интерполяция
        if self.W10 < w10_1:
            hp = hp_10 + (hp_10 - (hp_10 - hp_20) * ((w10_1 - self.W10) /
                                                     (w10_1 - w10_2)))
        elif self.W10 > w10_2:
            hp = hp_20 + (hp_20 - (hp_20 - hp_10) * ((self.W10 - w10_2) /
                                                     (w10_2 - w10_1)))
        else:  # w10 между 10 и 20
            hp = hp_10 + (hp_20 - hp_10) * ((self.W10 - w10_1) / (w10_2 - w10_1))

        return hp

    # Создаем словарь из таблицы

    # Функция для интерполяции значения λ
    def interpolate_lambda(self):
        table = {
            0.5: {8: 5.6, 12: 5.5, 16: 5.4, 20: 5.3},
            0.75: {8: 9.1, 12: 8.8, 16: 8.5, 20: 8.3},
            1.00: {8: 12.8, 12: 12.3, 16: 11.7, 20: 11.4},
            1.25: {8: 16.6, 12: 15.8, 16: 15.1, 20: 14.4}
        }
        hp_values = sorted(table.keys())
        w10_values = sorted(table[hp_values[0]].keys())

        # Находим ближайшие значения hp и w10 в таблице
        hp_index = np.searchsorted(hp_values, self.hp)
        w10_index = np.searchsorted(w10_values, self.W10)

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

        lambda_lower = lambda_lower_lower + (lambda_lower_upper - lambda_lower_lower) * (self.W10 - w10_lower) / (w10_upper - w10_lower)
        lambda_upper = lambda_upper_lower + (lambda_upper_upper - lambda_upper_lower) * (self.W10 - w10_lower) / (w10_upper - w10_lower)
        lambda_value = lambda_lower + (lambda_upper - lambda_lower) * (self.hp - hp_lower) / (hp_upper - hp_lower)
        print(lambda_value)
        return lambda_value

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()

    app = App(root)
    root.mainloop()
