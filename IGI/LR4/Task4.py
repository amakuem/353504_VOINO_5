import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    @abstractmethod
    def area(self):
        pass

class Color:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

class Triangle(GeometricFigure):
    figure_name = "Треугольник"

    def __init__(self, a, B_deg, C_deg, color):
        self.a = a
        self.B_deg = B_deg
        self.C_deg = C_deg
        self.color = Color(color)
        self.A_deg = 180 - (B_deg + C_deg)
        if self.A_deg <= 0:
            raise ValueError("Сумма углов B и C должна быть меньше 180 градусов")

    def area(self):
        B_rad = math.radians(self.B_deg)
        C_rad = math.radians(self.C_deg)
        A_rad = math.radians(self.A_deg)
        area = (self.a ** 2 * math.sin(B_rad) * math.sin(C_rad)) / (2 * math.sin(A_rad))
        return area

    def __str__(self):
        return "{0} {1} цвета со стороной a={2}, углами B={3}°, C={4}°, площадью {5:.2f}".format(
            self.figure_name, self.color.color, self.a, self.B_deg, self.C_deg, self.area()
        )
    
def Task4_func():
    print("Введите параметры треугольника:")
    try:
        a = float(input("Сторона a: "))
        B_deg = float(input("Угол B в градусах: "))
        C_deg = float(input("Угол C в градусах: "))
        color = input("Цвет фигуры (например, 'blue', 'red'): ")
        label = input("Текст подписи: ")

        # Проверка корректности данных
        if a <= 0:
            print("Сторона a должна быть положительной.")
            return
        if not (0 < B_deg < 180 and 0 < C_deg < 180 and B_deg + C_deg < 180):
            print("Углы B и C должны быть в диапазоне (0, 180) и их сумма меньше 180.")
            return

        # Создание объекта Triangle
        triangle = Triangle(a, B_deg, C_deg, color)
        print(triangle)

        # Вычисление координат вершины A
        B_rad = math.radians(B_deg)
        C_rad = math.radians(C_deg)
        tan_B = math.tan(B_rad)
        tan_C = math.tan(C_rad)

        if tan_B + tan_C == 0:
            print("Невозможно построить треугольник с данными углами.")
            return

        x = (tan_C * a) / (tan_B + tan_C)
        y = tan_B * x

        # Координаты вершин
        vertices = [(0, 0), (a, 0), (x, y)]

        # Построение фигуры
        fig, ax = plt.subplots()
        polygon = Polygon(vertices, closed=True, fill=True, color=color)
        ax.add_patch(polygon)
        ax.set_xlim(min(0, x, a) - 1, max(0, x, a) + 1)
        ax.set_ylim(0, max(y, 0) + 1)
        ax.set_aspect('equal', 'box')
        ax.text(a/2, y/2, label, ha='center', va='center')

        # Сохранение в файл
        plt.savefig('triangle.png')
        print("Фигура сохранена в файл 'triangle.png'")

        # Вывод на экран
        plt.show()

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
