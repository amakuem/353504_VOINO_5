import os
from geometric_lib import circle

r = int(input("Введите радиус круга: "))
print("Площадь круга = ", circle.area(r))
print("Периметр круга = ", circle.perimeter(r))
