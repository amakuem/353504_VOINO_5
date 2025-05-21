import numpy as np

class RandomMixer:
    def randomData(self, min_val=0, max_val=100):
        self.data = np.random.randint(min_val, max_val, size=(self.n, self.m))

class Matrix(RandomMixer):
    def __init__(self, n, m, min_val=0, max_val=100):
        """Инициализация матрицы размером n x m со случайными целыми числами."""
        self.n = n
        self.m = m
        #self.data = np.random.randint(min_val, max_val, size=(n, m))
        self.randomData(min_val, max_val)

    def get_array(self):
        """Возвращает матрицу как NumPy массив."""
        return self.data

    def display(self):
        """Выводит матрицу на экран."""
        print("Матрица:\n", self.data)

class SortedMatrix(Matrix):
    def __init__(self, n, m, min_val=0, max_val=100):
        """Инициализация с наследованием от Matrix."""
        super().__init__(n, m, min_val, max_val)
        self.sorted_last_row = None

    def sort_last_row(self):
        """Сортирует последнюю строку матрицы по возрастанию."""
        self.sorted_last_row = np.sort(self.data[self.n - 1])
        print("Отсортированная последняя строка:\n", self.sorted_last_row)

    def median_numpy(self):
        """Вычисляет медиану последней строки с помощью NumPy."""
        if self.sorted_last_row is None:
            self.sort_last_row()
        median = np.median(self.sorted_last_row)
        print("Медиана (NumPy):", median)
        return median

    def median_formula(self):
        """Вычисляет медиану последней строки через формулу."""
        if self.sorted_last_row is None:
            self.sort_last_row()
        m = len(self.sorted_last_row)
        if m % 2 == 1:
            median = self.sorted_last_row[m // 2]
        else:
            median = (self.sorted_last_row[m // 2 - 1] + self.sorted_last_row[m // 2]) / 2
        print("Медиана (формула):", median)
        return median
    
def Task5_func():
    # Задаем размеры матрицы
    n, m = 4, 5

    # Создаем объект производного класса
    matrix = SortedMatrix(n, m)

    # Выводим исходную матрицу
    matrix.display()

    # Сортируем последнюю строку
    matrix.sort_last_row()

    # Вычисляем медиану двумя способами
    matrix.median_numpy()
    matrix.median_formula()