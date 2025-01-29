from pyautocad import Autocad, APoint

# Инициализация AutoCAD
acad = Autocad(create_if_not_exists=True)

# Установка начальной точки
start_point = APoint(0, 0)

# Создание прямоугольника
width = 100  # 100 мм
height = 50  # 50 мм

# Рисование прямоугольника с помощью линий
acad.model.AddLine(start_point, APoint(start_point.x + width, start_point.y))
acad.model.AddLine(APoint(start_point.x + width, start_point.y), APoint(start_point.x + width, start_point.y + height))
acad.model.AddLine(APoint(start_point.x + width, start_point.y + height), APoint(start_point.x, start_point.y + height))
acad.model.AddLine(APoint(start_point.x, start_point.y + height), start_point)

print("Прямоугольник создан.")
