import math
import tabulate
import statistics
import matplotlib.pyplot as plt

# Базовый класс для вычисления ряда Тейлора
class TaylorSeries:
    def taylor_exp(self, x, eps):
        """
        Вычисляет приближенное значение e^x с помощью ряда Тейлора.

        Аргументы:
        x (float): Значение аргумента.
        eps (float): Точность вычислений.

        Возвращает:
        tuple: (приближенное значение e^x, количество итераций, список частичных сумм).
        """
        sum_val = 0
        term = 1
        i = 0
        partial_sums = []  # Список частичных сумм для статистики
        while abs(term) > eps and i < 500:
            sum_val += term
            partial_sums.append(sum_val)
            i += 1
            term = term * x / i
        return sum_val, i, partial_sums

# Производный класс для дополнительных вычислений
class EnhancedTaylorSeries(TaylorSeries):
    def compute_stats(self, x, eps):
        """
        Вычисляет статистические параметры для частичных сумм ряда.

        Аргументы:
        x (float): Значение аргумента.
        eps (float): Точность вычислений.

        Возвращает:
        dict: Словарь со статистическими параметрами.
        """
        computed_value, n, partial_sums = self.taylor_exp(x, eps)

        math_value = math.exp(x)  

        table_data = [
            [x, n, computed_value, math_value, eps]
        ]

        table_headers = ["x", "n", "F(x)", "Math F(x)", "eps"]

        table = tabulate.tabulate(table_data, headers=table_headers, floatfmt=".8f")
        print(table)


        if not partial_sums:
            return None
        
        mean = statistics.mean(partial_sums)  # Среднее арифметическое
        median = statistics.median(partial_sums)  # Медиана
        try:
            mode = statistics.mode(partial_sums)  # Мода
        except statistics.StatisticsError:
            mode = "Нет уникальной моды"
        variance = statistics.variance(partial_sums)  # Дисперсия
        std_dev = statistics.stdev(partial_sums)  # СКО
        
        return {
            'Среднее арифметическое': mean,
            'Медиана': median,
            'Мода': mode,
            'Дисперсия': variance,
            'СКО': std_dev
        }

    def generate_plot_data(self, x_values, eps):
        """
        Генерирует данные для построения графиков.

        Аргументы:
        x_values (list): Список значений x.
        eps (float): Точность вычислений.

        Возвращает:
        tuple: (x_values, значения ряда Тейлора, значения math.exp).
        """
        taylor_values = []
        math_values = []
        for x in x_values:
            taylor_val, _, _ = self.taylor_exp(x, eps)
            taylor_values.append(taylor_val)
            math_values.append(math.exp(x))
        return x_values, taylor_values, math_values

# Класс для построения и сохранения графиков
class PlotGenerator:
    def __init__(self, enhanced_taylor):
        """
        Инициализирует объект с экземпляром EnhancedTaylorSeries.

        Аргументы:
        enhanced_taylor (EnhancedTaylorSeries): Экземпляр класса для вычислений.
        """
        self.enhanced_taylor = enhanced_taylor

    def create_plot(self, x_values, eps):
        """
        Строит и сохраняет графики.

        Аргументы:
        x_values (list): Список значений x.
        eps (float): Точность вычислений.
        """
        x, taylor_vals, math_vals = self.enhanced_taylor.generate_plot_data(x_values, eps)
        
        plt.plot(x, taylor_vals, label='F(x) Тейлор', color='blue')  # График ряда Тейлора
        plt.plot(x, math_vals, label='Math F(x)', color='red')  # График math.exp
        plt.xlabel('x')  # Подпись оси X
        plt.ylabel('F(x)')  # Подпись оси Y
        plt.title('Ряд Тейлора vs math.exp')  # Заголовок
        plt.legend()  # Легенда
        plt.grid(True)  # Сетка
        plt.annotate('Точность: ' + str(eps), xy=(0.05, 0.95), xycoords='axes fraction')  # Аннотация
        plt.savefig('taylor_plot.png')  # Сохранение в файл
        plt.show()  # Отображение графика

# Основная функция для взаимодействия с пользователем
def Task3_func():
    # Ввод данных от пользователя
    while True:
        try:
            x = float(input("Введите x: "))
            break
        except ValueError:
            print("Пожалуйста, введите корректное число.")
    while True:
        try:
            eps = float(input("Введите eps: "))
            break
        except ValueError:
            print("Пожалуйста, введите корректное число.")

    
    enhanced_taylor = EnhancedTaylorSeries()
    plot_gen = PlotGenerator(enhanced_taylor)

    # Вычисление и вывод статистических параметров
    stats = enhanced_taylor.compute_stats(x, eps)
    print("\nСтатистические параметры:")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Генерация данных для графика
    x_values = [i * 0.1 for i in range(-10, 11)]  # Диапазон x от -1 до 1 с шагом 0.1
    plot_gen.create_plot(x_values, eps)

