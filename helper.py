from pyautocad import Autocad, APoint  # Импортируйте необходимые классы из библиотеки Autocad


class AutoCADLinesPlacer:
    def __init__(self, **kwargs):
        self.data = kwargs
        self.coordinates = {
            'tranzit_AB_coal': (436, 925),
            'tranzit_AB_rock': (10, 30),
            # Добавьте остальные координаты
        }

    def place_text(self):
        """Размещает текст в AutoCAD по заданным координатам"""
        try:
            # Подключение к AutoCAD
            self.acad = Autocad(create_if_not_exists=True)
            self.acad.Visible = True

            # Размещаем каждый параметр
            for param, value in self.data.items():
                if param in self.coordinates:
                    x, y = self.coordinates[param]
                    point = APoint(x, y)
                    self.acad.model.AddText(str(value), point, 2.5)  # 2.5 - высота текста
                    print(f"Размещен параметр {param} = {value} в точке ({x}, {y})")

        except Exception as e:
            print(f"Ошибка: {e}")

# Использование
placer = AutoCADLinesPlacer(
    tranzit_AB_coal=50,
    tranzit_AB_rock=30
)
placer.place_text()