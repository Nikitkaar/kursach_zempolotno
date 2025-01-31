from pyautocad import Autocad, APoint
import math


class AutoCADLines:
    def __init__(self, scale_factor=100, **kwargs):
        self.acad = Autocad(create_if_not_exists=True)
        self.scale_factor = scale_factor  # Масштаб
        self.H = kwargs.get('H', 10) * 1000  # Высота в мм (преобразуем из метров)
        self.xnmax = kwargs.get('xnmax', 5) * 1000  # Максимальное значение x в мм (преобразуем из метров)
        self.hbm = kwargs.get('hbm', 1.2) * 1000  # Толщина слоя балластных материалов в мм (преобразуем из метров)
        self.arrow_size = kwargs.get('arrow_size', 0.5) * 10  # Размер стрелочки в мм (преобразуем из метров)
        self.b0 = kwargs.get('b0', 2.2) * 1000
        self.n = kwargs.get('n', 2.1) * 1000
        self.segments = []  # Хранение всех отрезков для проверки
        self.h0 = kwargs.get('h0', 1.98) * 1000
        self.h1 = kwargs.get('h1', 3.05) * 1000
        self.h2 = kwargs.get('h2', 3.18) * 1000
        self.h3 = kwargs.get('h3', 2.73) * 1000
        self.h4 = kwargs.get('h4', 1.75) * 1000
        self.h5 = kwargs.get('h5', 0.3) * 1000

        self.xn2 = kwargs.get('xn2', 7.16) * 1000
        self.xn3 = kwargs.get('xn3', 12.12) * 1000
        self.xn4 = kwargs.get('xn4', 17.08) * 1000
        self.xn5 = kwargs.get('xn5', 22.04) * 1000
        self.xn6 = kwargs.get('xn6', 27.0) * 1000

        self.xcp0 = kwargs.get('xcp0', 1.1) * 1000
        self.xcp1 = kwargs.get('xcp1', 4.68) * 1000
        self.xcp2 = kwargs.get('xcp2', 9.64) * 1000
        self.xcp3 = kwargs.get('xcp3', 14.6) * 1000
        self.xcp4 = kwargs.get('xcp4', 19.56) * 1000
        self.xcp5 = kwargs.get('xcp5', 24.52) * 1000

        self.yп1 = kwargs.get('yп1', 11.8) * 1000
        self.yп2 = kwargs.get('yп2', 10.56) * 1000
        self.yп3 = kwargs.get('yп3', 8.08) * 1000
        self.yп4 = kwargs.get('yп4', 5.6) * 1000
        self.yп5 = kwargs.get('yп5', 3.12) * 1000
        self.yп6 = kwargs.get('yп6', 0.64) * 1000

    def draw_lines(self):
        x_max = max(self.xnmax, 0) / self.scale_factor  # Применяем масштаб

        # Создание координатных точек
        hordastart = APoint(0, 0)
        vertical_end = APoint(x_max, 1.09 * self.H / self.scale_factor)
        horizontal_start = vertical_start = Hbmstart = APoint(x_max, 0)
        horizontal_end = APoint(-x_max * 0.09, 0)
        hordaend = hbmstart = Hbmend = APoint(x_max, (self.H - self.hbm) / self.scale_factor)
        hbmend = b0startUP = APoint(x_max, self.H / self.scale_factor)
        otkostart = b0endUP = APoint(x_max - self.b0 / self.scale_factor, self.H / self.scale_factor)
        h0end = APoint(x_max - self.xcp0 / self.scale_factor, (self.H - self.h0) / self.scale_factor)
        h0start = APoint(x_max-self.xcp0 / self.scale_factor, self.H / self.scale_factor)

        # Создание отрезков
        self.add_segment(vertical_start, vertical_end)
        self.add_segment(horizontal_start, horizontal_end)
        self.add_segment(Hbmstart, Hbmend)
        self.add_segment(hbmstart, hbmend)
        self.add_segment(b0startUP, b0endUP)
        self.add_segment(otkostart, hordastart)

        # Определение ближайшего пересечения по y координате
        hbm_horizontal_end_x = self.find_nearest_intersection(hbmstart.y)

        if hbm_horizontal_end_x:
            hbm_horizontal_end = APoint(hbm_horizontal_end_x, hbmstart.y)
            self.acad.model.AddLine(hbmstart, hbm_horizontal_end)  # Добавление горизонтального отрезка



        # Добавляем мешающий отрезок
        self.add_segment(hordastart, hordaend)
        self.add_segment(h0start, h0end)

        # Добавление размеров
        self._add_dimensions(Hbmstart, Hbmend, f'H = {(self.H - self.hbm) / 1000:.2f} м', offset_x=10)
        self._add_dimensions(hbmstart, hbmend, f'hбм = {(self.H - self.hbm) / 1000:.2f} м', offset_x=10)
        self._add_dimensions(horizontal_start, hordastart, f'L = {x_max:.1f} м', offset_y=-5)

        # Добавление текста без размерных линий
        self._add_text_to_segment(otkostart, hordastart, f'1 : {self.n / 1000:.1f}')
        self.acad.model.AddText("0", APoint(x_max + 4, -8), 5)
        self.acad.model.AddText("x", APoint(-x_max * 0.09, -8), 5)
        self.acad.model.AddText("y", APoint(x_max - 7, 1.09 * self.H / self.scale_factor), 5)

        # Добавление стрелочек
        self._create_arrow(vertical_end, 'vertical')
        self._create_arrow(horizontal_end, 'horizontal')

    def add_segment(self, start, end):
        # Добавление отрезка в коллекцию
        self.segments.append((start, end))
        self.acad.model.AddLine(start, end)

    def find_nearest_intersection(self, y_target):
        closest_x = None

        for start, end in self.segments:
            # Проверяем, попадает ли y_target в интервал
            if (start.y <= y_target <= end.y) or (end.y <= y_target <= start.y):
                # Определяем X для данной Y
                if start.x != end.x:  # если отрезок не вертикальный
                    k = (end.y - start.y) / (end.x - start.x)  # Наклон
                    b = start.y - k * start.x  # Свободный член
                    x_at_target = (y_target - b) / k  # X, соответствующий y_target

                    # Проверяем, что X находится на отрезке
                    if (min(start.x, end.x) <= x_at_target <= max(start.x, end.x)):
                        if closest_x is None or x_at_target > closest_x:  # Ищем ближайший X, который меньше
                            closest_x = x_at_target

        return closest_x

    def _add_text_to_segment(self, start, end, text):
        # Вычисляем середину отрезка
        mid_point = APoint(((start.x + end.x) / 2) + 5, ((start.y + end.y) / 2) + 5)

        # Добавление текста в середине отрезка
        mt = self.acad.model.AddText(text, mid_point, 4)  # Устанавливаем размер текста равным 4
        mt.Rotation = math.radians(25)  # 0.4363325 Установка угла наклона текста

    def _create_arrow(self, end, orientation):
        if orientation == 'vertical':
            # Стрелочки для вертикального отрезка (вниз)
            self.acad.model.AddLine(end, APoint(end.x - self.arrow_size * 0.5, end.y - self.arrow_size))  # Левая
            self.acad.model.AddLine(end, APoint(end.x + self.arrow_size * 0.5, end.y - self.arrow_size))  # Правая
        else:
            # Стрелочки для горизонтального отрезка (вправо)
            self.acad.model.AddLine(end, APoint(end.x + self.arrow_size, end.y - self.arrow_size * 0.5))  # Ниже
            self.acad.model.AddLine(end, APoint(end.x + self.arrow_size, end.y + self.arrow_size * 0.5))  # Выше

    def _add_dimensions(self, start, end, label, offset_x=0, offset_y=0):
        # Вычислим среднюю точку для размещения текста между началом и концом
        mid_point = APoint((start.x + end.x) / 2 + offset_x, (start.y + end.y) / 2 + offset_y)

        # Добавление размерной линии для отрезков
        dim_line = self.acad.model.AddDimAligned(start, end, mid_point)
        dim_line.TextOverride = label  # Установка текста размерной линии


# Пример использования класса
if __name__ == "__main__":
    cad_lines = AutoCADLines(H=11.8, xnmax=27.2, arrow_size=0.5, b0=2.2)
    cad_lines.draw_lines()
