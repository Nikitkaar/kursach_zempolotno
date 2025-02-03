from pyautocad import Autocad, APoint  # Импортируйте необходимые классы из библиотеки Autocad
import math


class AutoCADLines():
    def __init__(self, scale_factor=100, **kwargs):
        self.acad = Autocad(create_if_not_exists=True)
        self.scale_factor = scale_factor  # Масштаб
        self.H = kwargs.get('H') * 1000  # Высота в мм (преобразуем из метров)
        self.xnmax = kwargs.get('xnmax') * 1000  # Максимальное значение x в мм (преобразуем из метров)
        self.hbm = kwargs.get('hbm') * 1000  # Толщина слоя балластных материалов в мм (преобразуем из метров)
        self.arrow_size = kwargs.get('arrow_size', 0.5) * 10  # Размер стрелочки в мм (преобразуем из метров)
        self.b0 = kwargs.get('b0') * 1000
        self.n = kwargs.get('n') * 1000
        self.segments = []  # Хранение всех отрезков для проверки
        self.h0 = kwargs.get('h0') * 1000
        self.h1 = kwargs.get('h1') * 1000
        self.h2 = kwargs.get('h2') * 1000
        self.h3 = kwargs.get('h3') * 1000
        self.h4 = kwargs.get('h4') * 1000
        self.h5 = kwargs.get('h5') * 1000

        self.xn2 = kwargs.get('xn2') * 1000
        self.xn3 = kwargs.get('xn3') * 1000
        self.xn4 = kwargs.get('xn4') * 1000
        self.xn5 = kwargs.get('xn5') * 1000
        self.xn6 = kwargs.get('xn6') * 1000

        self.xcp0 = kwargs.get('xcp0') * 1000
        self.xcp1 = kwargs.get('xcp1') * 1000
        self.xcp2 = kwargs.get('xcp2') * 1000
        self.xcp3 = kwargs.get('xcp3') * 1000
        self.xcp4 = kwargs.get('xcp4') * 1000
        self.xcp5 = kwargs.get('xcp5') * 1000

        self.yп1 = kwargs.get('yп1') * 1000
        self.yп2 = kwargs.get('yп2') * 1000
        self.yп3 = kwargs.get('yп3') * 1000
        self.yп4 = kwargs.get('yп4') * 1000
        self.yп5 = kwargs.get('yп5') * 1000
        self.yп6 = kwargs.get('yп6') * 1000

        self.t = kwargs.get('t') * 1000
        self.α = kwargs.get('α')
        self.μ = kwargs.get('μ')
        self.d = kwargs.get('d')

    def draw_arc_through_points(self, start, mid, end):
        """Рисует дугу через три точки: start, mid и end."""
        # Высчитываем радиус и центр дуги через три точки
        center = self.calculate_circle_center(start, mid, end)

        # Вычисляем радиус
        radius = start.distance_to(center)

        # Рассчитываем углы для дуги
        start_angle = math.degrees(math.atan2(start.y - center.y, start.x - center.x))
        end_angle = math.degrees(math.atan2(end.y - center.y, end.x - center.x))

        # Добавление дуги
        arc = self.acad.model.AddArc(center, radius, start_angle, end_angle)

        return arc

    def calculate_circle_center(self, A, B, C):
        """Находит центр окружности, описанной через точки A, B и C."""
        D = 2 * (A.x * (B.y - C.y) + B.x * (C.y - A.y) + C.x * (A.y - B.y))
        if D == 0:
            raise ValueError("Точки A, B и C находятся на одной прямой.")

        Ux = ((A.x ** 2 + A.y ** 2) * (B.y - C.y) + (B.x ** 2 + B.y ** 2) * (C.y - A.y) + (C.x ** 2 + C.y ** 2) * (
                    A.y - B.y)) / D
        Uy = ((A.x ** 2 + A.y ** 2) * (C.x - B.x) + (B.x ** 2 + B.y ** 2) * (A.x - C.x) + (C.x ** 2 + C.y ** 2) * (
                    B.x - A.x)) / D

        return APoint(Ux, Uy)

    def rotate_point(self, point, angle_degrees, origin):
        """Поворачивает точку point вокруг точки origin на angle_degrees."""
        angle_radians = math.radians(angle_degrees)
        cos_angle = math.cos(angle_radians)
        sin_angle = math.sin(angle_radians)

        # Перемещение точки в начало координат
        translated_x = point.x - origin.x
        translated_y = point.y - origin.y

        # Применение матрицы поворота
        rotated_x = translated_x * cos_angle - translated_y * sin_angle
        rotated_y = translated_x * sin_angle + translated_y * cos_angle

        # Возврат точки в исходную систему координат
        return APoint(rotated_x + origin.x, rotated_y + origin.y)


    def draw_lines(self):
        xnmax = self.xnmax / self.scale_factor  # Применяем масштаб

        # Создание координатных точек
        hordastart = APoint(0, 0)
        vertical_end = APoint(xnmax, 1.09 * self.H / self.scale_factor)
        horizontal_start = vertical_start = Hbmstart = APoint(xnmax, 0)
        horizontal_end = APoint(-xnmax * 0.09, 0)
        hordaend = hbmstart = Hbmend = APoint(xnmax, (self.H - self.hbm) / self.scale_factor)
        hbmend = b0startUP = APoint(xnmax, self.H / self.scale_factor)
        otkostart = b0endUP = APoint(xnmax - self.b0 / self.scale_factor, self.H / self.scale_factor)
        h0end = APoint(xnmax - self.xcp0 / self.scale_factor, (self.H - self.h0) / self.scale_factor)
        h0start = APoint(xnmax-self.xcp0 / self.scale_factor, self.H / self.scale_factor)

        h1end = APoint(xnmax - self.xcp1 / self.scale_factor, self.yп2 / self.scale_factor)
        h1start = APoint(xnmax - self.xcp1 / self.scale_factor, (self.yп2 - self.h1) / self.scale_factor)

        h2end = APoint(xnmax - self.xcp2 / self.scale_factor, self.yп3 / self.scale_factor)
        h2start = APoint(xnmax - self.xcp2 / self.scale_factor, (self.yп3 - self.h2) / self.scale_factor)
        h3end = APoint(xnmax - self.xcp3 / self.scale_factor, self.yп4 / self.scale_factor)
        h3start = APoint(xnmax - self.xcp3 / self.scale_factor, (self.yп4 - self.h3) / self.scale_factor)
        h4end = APoint(xnmax - self.xcp4 / self.scale_factor, self.yп5 / self.scale_factor)
        h4start = APoint(xnmax - self.xcp4 / self.scale_factor, (self.yп5 - self.h4) / self.scale_factor)
        h5end = APoint(xnmax - self.xcp5 / self.scale_factor, self.yп6 / self.scale_factor)
        h5start = APoint(xnmax - self.xcp5 / self.scale_factor, (self.yп6 - self.h5) / self.scale_factor)
        # Создание линий...

        tstart = APoint(xnmax / 2, (self.H - self.hbm) / 2 / self.scale_factor)
        tend = APoint(xnmax / 2, ((self.H - self.hbm) / 2 - self.t) / self.scale_factor)

        d1 = APoint(0, 0)
        d1_ = APoint(xnmax / 2, (self.H - self.hbm) / 2 / self.scale_factor)
        d2 = APoint(xnmax / 2, (self.H - self.hbm) / 2 / self.scale_factor)
        d2_ = APoint(xnmax, (self.H - self.hbm) / self.scale_factor)

        # Поворот tstart и tend на угол α относительно точки origin
        #tstart = self.rotate_point(tstart, self.α, origin)  # Поворачиваем tstart
        tend = self.rotate_point(tend, self.α, tstart)  # Поворачиваем tend

        # Создание отрезков
        self.add_segment(vertical_start, vertical_end)
        self.add_segment(horizontal_start, horizontal_end)
        self.add_segment(Hbmstart, Hbmend)
        self.add_segment(hbmstart, hbmend)
        self.add_segment(b0startUP, b0endUP)
        self.add_segment(otkostart, hordastart)
        self.add_segment(tstart, tend)

        # Определение ближайшего пересечения по y координате
        hbm_horizontal_end_x = self.find_nearest_intersection(hbmstart.y)

        if hbm_horizontal_end_x:
            hbm_horizontal_end = APoint(hbm_horizontal_end_x, hbmstart.y)
            self.acad.model.AddLine(hbmstart, hbm_horizontal_end)  # Добавление горизонтального отрезка



        # Добавляем мешающий отрезок
        self.add_segment(hordastart, hordaend)
        self.draw_arc_through_points(hordastart, tend, Hbmend)

        # Добавление размеров
        self._add_dimensions(Hbmstart, Hbmend, f'H - hбм = {(self.H - self.hbm) / 1000:.2f} м', offset_x=10)
        self._add_dimensions(hbmstart, hbmend, f'hбм = {(self.hbm) / 1000:.2f} м', offset_x=10)
        self._add_dimensions(horizontal_start, hordastart, f'L = {xnmax/10:.1f} м', offset_y=-5)
        self._add_dimensions(h0start, h0end, f'h0 = {self.h0*10:.1f} м', offset_y=-100)
        self._add_dimensions(h1start, h1end, f'h1 = {self.h1*10:.1f} м', offset_y=-100)
        self._add_dimensions(h2start, h2end, f'h2 = {self.h2*10:.1f} м', offset_y=-1700)
        self._add_dimensions(h3start, h3end, f'h3 = {self.h3*10:.1f} м', offset_y=-160)
        self._add_dimensions(h4start, h4end, f'h4 = {self.h4*10:.1f} м', offset_y=-150)
        self._add_dimensions(h5start, h5end, f'h5 = {self.h5*10:.1f} м', offset_y=-100)

        # Добавление текста без размерных линий
        self._add_text_to_segment(otkostart+5, hordastart, 25,f'1 : {self.n / 1000:.1f}')
        self._add_text_to_segment(d1, d1_, 21.449,f'd = {self.d:.2f} м')
        self._add_text_to_segment(d2, d2_, 21.449,f'd = {self.d:.2f} м')

        self.acad.model.AddText("0", APoint(xnmax + 4, -8), 5)
        self.acad.model.AddText("x", APoint(-xnmax * 0.09, -8), 5)
        self.acad.model.AddText("y", APoint(xnmax - 7, 1.09 * self.H / self.scale_factor), 5)

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

    def _add_text_to_segment(self, start, end, rotation, text):
        # Вычисляем середину отрезка
        mid_point = APoint(((start.x + end.x) / 2) + 5, ((start.y + end.y) / 2) + 5)

        # Добавление текста в середине отрезка
        mt = self.acad.model.AddText(text, mid_point, 4)  # Устанавливаем размер текста равным 4
        mt.Rotation = math.radians(rotation)  # 0.4363325 Установка угла наклона текста

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

