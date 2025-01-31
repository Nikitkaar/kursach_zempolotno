import ezdxf
from ezdxf.math import Vec3
from ezdxf.entities import DimStyle

def create_angled_dimension_dxf(output_dxf_filename="angled_dimension.dxf"):
    """Создает DXF-файл с двумя линиями и угловым размером между ними."""

    doc = ezdxf.new("R2010")  # Создаем новый документ DXF (R2010 формат)
    msp = doc.modelspace()  # Получаем доступ к пространству модели


    # Определяем точки для линий и углового размера
    point1 = Vec3(0, 0)
    point2 = Vec3(10, 0)
    point3 = Vec3(10, 10)

    # Создаем две линии
    line1 = msp.add_line(point1, point2)
    line2 = msp.add_line(point2, point3)

    # Вычисляем точку для размещения текста углового размера. Эта точка должна находится примерно по центру дуги размера
    text_point = point2.lerp(point3, 0.2).lerp(point1,0.2) # Смещаем от точки 2 к точке 3 на 20% и от точки 2 к точке 1 на 20%

    # Создаем угловой размер
    dim = msp.add_angular_dim(
        base=point2,  # Начальная точка дуги
        p1=point1,  # Первая точка определяющая угол
        p2=point3,  # Вторая точка, определяющая угол
        location=text_point, # Точка, где будет расположен текст
        dimstyle="ISO-25",
    )

    # Обновляем блок размера для корректного отображения (по умолчанию он может быть пустым)
    dim.render()


    doc.saveas(output_dxf_filename) # Сохраняем DXF-файл
    print(f"DXF-файл '{output_dxf_filename}' создан.")


if __name__ == "__main__":
    create_angled_dimension_dxf() # Создаем DXF файл по умолчанию