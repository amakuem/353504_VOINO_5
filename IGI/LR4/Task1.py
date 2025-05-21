import csv
import pickle

class Load:
    def __init__(self, class_name, hours):
        self.class_name = class_name
        self.hours = hours
    
    def __str__(self):
        return f"{self.class_name}: {self.hours} часов"
        

class Person:
    def __init__(self, surname):
        self.surname = surname
    
    def __str__(self):
        return self.surname

class Teacher(Person):
    def __init__(self, surname):
        super().__init__(surname)
        self.loads = []
    
    def add_load(self, load):
        self.loads.append(load)

    def total_hours(self):
        return  sum(load.hours for load in self.loads)
    
    def __str__(self):
        return  f"{self.surname}: {self.total_hours()} часов"
    
class SchoolLoadManager:
    def __init__(self):
        self.teachers = []

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def find_teacher(self, surname):
        for teacher in self.teachers:
            if teacher.surname == surname:
                return teacher
        return None
    
    def get_max_load_teacher(self):
        if not self.teachers:
            return None
        return max(self.teachers, key=lambda t: t.total_hours())
    
    def get_min_load_teacher(self):
        if not self.teachers:
            return None
        return min(self.teachers, key=lambda t: t.total_hours())
    
    def save_to_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Фамилия', 'Класс', 'Часы'])
            for teacher in self.teachers:
                for load in teacher.loads:
                    writer.writerow([teacher.surname, load.class_name, load.hours])

    def load_from_csv(self, filename):
        self.teachers = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропустить заголовок
            current_teacher = None
            for row in reader:
                surname, class_name, hours = row
                hours = int(hours)
                if current_teacher is None or current_teacher.surname != surname:
                    current_teacher = Teacher(surname)
                    self.add_teacher(current_teacher)
                load = Load(class_name, hours)
                current_teacher.add_load(load)
    
    def save_to_pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load_from_pickle(self, filename):
        with open(filename, 'rb') as f:
            loaded = pickle.load(f)
            self.teachers = loaded.teachers


data = {
    "Петров": [
        {"класс": "5А", "часы": 3},
        {"класс": "6Б", "часы": 4}
    ],
    "Иванов": [
        {"класс": "7В", "часы": 2},
        {"класс": "8Г", "часы": 3}
    ],
    "Сидоров": [
        {"класс": "9А", "часы": 5}
    ]
}

def Task1_func():
    manager = SchoolLoadManager()
    for surname, loads in data.items():
        teacher = Teacher(surname)
        for load_data in loads:
            load = Load(load_data['класс'], load_data['часы'])
            teacher.add_load(load)
        manager.add_teacher(teacher)

    # Сохранение данных в файлы
    manager.save_to_csv('school_load.csv')
    manager.save_to_pickle('school_load.pkl')

    # Загрузка данных из pickle (можно также использовать CSV)
    manager_pickle = SchoolLoadManager()
    manager_pickle.load_from_pickle('school_load.pkl')

    # Вывод нагрузки каждого преподавателя
    print("Нагрузка преподавателей:")
    for teacher in manager_pickle.teachers:
        print(teacher)

    # Определение преподавателей с максимальной и минимальной нагрузкой
    max_load_teacher = manager_pickle.get_max_load_teacher()
    min_load_teacher = manager_pickle.get_min_load_teacher()
    print(f"\nПреподаватель с самой большой нагрузкой: {max_load_teacher}")
    print(f"Преподаватель с самой низкой нагрузкой: {min_load_teacher}")

    # Поиск нагрузки преподавателя по введенной фамилии
    surname = input("\nВведите фамилию преподавателя: ")
    teacher = manager_pickle.find_teacher(surname)
    if teacher:
        print(f"Нагрузка преподавателя {surname}: {teacher.total_hours()} часов")
    else:
        print("Преподаватель не найден")

       