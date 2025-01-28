import math
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


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
            "Показатель кривизны кривой, Kt"
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
            "Показатель кривизны кривой, Kt"]:
                # Преобразуем числовые значения
                try:
                    if field in ["Высота насыпи Н, м",
            "Показатель крутизны откосов n, -",
            "толщина слоя балластных материалов, hбм, м",
            "Показатель текучести WL",
            "Показатель кривизны кривой, Kt"]:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    messagebox.showwarning("Ошибка", f"Введите корректное числовое значение для {field}.")
                    return

            data[field] = value  # Сохраняем значения

        # Формирование итоговых переменных
        ## Константы
        """Ширина первого отсека, м:"""
        b0 = x1 = 2.2
        """Ширина основной площадки земполотна, м:"""
        B = 7.0
        """Объемный вес грунта, т\м^3:"""
        p = 2
        """Длинна шпалы, м:"""
        lш = 2.7
        ## ВВодимс
        self.H = data["Высота насыпи Н, м"]
        self.n = data["Показатель крутизны откосов n, -"]
        self.hбм = data["толщина слоя балластных материалов, hбм, м"]
        self.WL = data["Показатель текучести WL"]
        self.Kt = data["Показатель кривизны кривой, Kt"]



        messagebox.showinfo("Успех", "Все данные успешно введены!")

        self.root.destroy()  # Закрыть окно после подтверждения
        self.root.quit()  # Завершает цикл обработки событий Tkinter

        self.horda_2d = math.sqrt(((self.H - self.hбм)**2 + (self.n * self.H + x1)**2))
        self.d = self.horda_2d/2

        self.t = self.Kt * self.H
        self.R = (self.d**2 + self.t**2)/(2*self.t)
        self.α = math.asin((self.H - self.hбм) / self.horda_2d)

        #self.α_degrees = math.degrees(self.α)
        #print(f"Угол в радианах: {self.α_degrees}")

        self.μ = math.asin(self.d/self.R)
        self.XR = self.n * self.H + x1 + self.R * math.sin(self.α-self.μ)
        self.YR = self.R * math.cos(self.α-self.μ)
        self.N = self.find_max_N()
        self.b1 = self.n * self.H / self.N

        self.xn1 = App.b0
        self.xn2 = self.xn1 + self.b1
        self.xn3 = self.xn2 + self.b1
        self.xn4 = self.xn3 + self.b1
        self.xn5 = self.xn4 + self.b1

        self.xcp0 = App.b0/2
        self.xcp1 = (self.xcp0 + self.xn2)/2
        self.xcp2 = (self.xcp1 + self.xn3)/2
        self.xcp3 = (self.xcp2 + self.xn4)/2
        self.xcp4 = (self.xcp3 + self.xn5)/2

        self.β0 = math.asin((self.XR - self.xcp0)/self.R)
        self.β1 = math.asin((self.XR - self.xcp1)/self.R)
        self.β2 = math.asin((self.XR - self.xcp2)/self.R)
        self.β3 = math.asin((self.XR - self.xcp3)/self.R)
        self.β4 = math.asin((self.XR - self.xcp4)/self.R)

        self.yп1 = self.H - (self.xcp0 - x1)/2
        self.yп2 = self.H - (self.xcp1 - x1)/2
        self.yп3 = self.H - (self.xcp2 - x1)/2
        self.yп4 = self.H - (self.xcp3 - x1)/2
        self.yп5 = self.H - (self.xcp4 - x1)/2

        self.yk0 = self.YR - self.R * math.cos(self.β0)
        self.yk1 = self.YR - self.R * math.cos(self.β1)
        self.yk2 = self.YR - self.R * math.cos(self.β2)
        self.yk3 = self.YR - self.R * math.cos(self.β3)
        self.yk4 = self.YR - self.R * math.cos(self.β4)

        self.h0 = self.yп1 - self.yk0
        self.h1 = self.yп2 - self.yk1
        self.h2 = self.yп3 - self.yk2
        self.h3 = self.yп4 - self.yk3
        self.h4 = self.yп5 - self.yk4

        self.g0 = 2* self.h0 * b0
        self.g1 = 2* self.h1 * self.b1
        self.g2 = 2* self.h2 * self.b1
        self.g3 = 2* self.h3 * self.b1
        self.g4 = 2* self.h4 * self.b1

        self.Cpr = input(f"Введите значение Спр для WL = {self.WL} и h = {self.h0}")
        self.Cpr = input(f"Введите значение Спр для WL = {self.WL} и h = {self.h1}")
        self.Cpr = input(f"Введите значение Спр для WL = {self.WL} и h = {self.h2}")
        self.Cpr = input(f"Введите значение Спр для WL = {self.WL} и h = {self.h3}")
        self.Cpr = input(f"Введите значение Спр для WL = {self.WL} и h = {self.h4}")

        print(f'horda={self.horda_2d}\nd={self.d}\nt={self.t}\nR={self.R}\nα={self.α}\nμ={self.μ}\nXR={self.XR}\n'
              f'XY={self.YR}\nN={self.N}\nb={self.b}\nfind_max_N={self.find_max_N}')



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


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()