import re
import zipfile
import os

class TextAnalyzer:
    def __init__(self, text):
        self.text = text

    def count_sentences(self):
        """Подсчитывает количество предложений в тексте."""
        sentences = re.split(r'[.!?]+', self.text)
        return len([s for s in sentences if s.strip()])

    def count_sentence_types(self):
        """Подсчитывает количество предложений каждого типа."""
        narrative = len(re.findall(r'\.\s', self.text))
        interrogative = len(re.findall(r'\?\s', self.text))
        imperative = len(re.findall(r'!\s', self.text))
        return {
            'повествовательные': narrative,
            'вопросительные': interrogative,
            'побудительные': imperative
        }

    def average_sentence_length(self):
        """Вычисляет среднюю длину предложения в символах (только слова)."""
        sentences = re.split(r'[.!?]+', self.text)
        word_lengths = [sum(len(w) for w in re.findall(r'\w+', s)) for s in sentences if s.strip()]
        return sum(word_lengths) / len(word_lengths) if word_lengths else 0

    def average_word_length(self):
        """Вычисляет среднюю длину слова в тексте в символах."""
        words = re.findall(r'\w+', self.text)
        lengths = [len(word) for word in words]
        return sum(lengths) / len(lengths) if lengths else 0

    def count_smilies(self):
        """Подсчитывает количество смайликов по заданным правилам."""
        pattern = r'[:;]-*[\(\)\[\]]+' 
        smilies = re.findall(pattern, self.text)
        return len(smilies)
    
class MacAddressValidator(TextAnalyzer):
    def is_valid_mac(self, mac):
        """Проверяет, является ли строка правильным MAC-адресом."""
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return bool(re.match(pattern, mac))
    
class WordAnalyzer(TextAnalyzer):
    def words_starting_with_lowercase(self):
        """Возвращает слова, начинающиеся со строчной буквы."""
        return re.findall(r'\b[a-zа-яё]\w*\b', self.text)

    def punctuation_marks(self):
        """Возвращает все знаки препинания."""
        return re.findall(r'[^\w\s]', self.text)

    def count_words(self):
        """Подсчитывает количество слов в тексте."""
        return len(re.findall(r'\w+', self.text))

    def longest_word(self):
        """Находит самое длинное слово и его порядковый номер."""
        words = re.findall(r'\w+', self.text)
        if not words:
            return None, 0
        longest = max(words, key=len)
        index = words.index(longest) + 1
        return longest, index

    def odd_words(self):
        """Возвращает каждое нечетное слово."""
        words = re.findall(r'\w+', self.text)
        return [words[i] for i in range(0, len(words), 2)]
    

def Task2_func():
    # Чтение текста из файла
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("Файл input.txt не найден!")
        exit(1)

    # Создание объектов классов
    analyzer = WordAnalyzer(text)
    mac_validator = MacAddressValidator(text)

    # Пример MAC-адреса для проверки
    mac = "aE:dC:cA:56:76:54"
    is_valid_mac = mac_validator.is_valid_mac(mac)

    # Получение результатов анализа
    words_lowercase = analyzer.words_starting_with_lowercase()
    punctuation = analyzer.punctuation_marks()
    word_count = analyzer.count_words()
    longest_word, longest_index = analyzer.longest_word()
    odd_words = analyzer.odd_words()

    # Результаты общего задания
    sentence_count = analyzer.count_sentences()
    sentence_types = analyzer.count_sentence_types()
    avg_sentence_len = analyzer.average_sentence_length()
    avg_word_len = analyzer.average_word_length()
    smiley_count = analyzer.count_smilies()

    # Вывод результатов на экран
    print(f"Слова, начинающиеся со строчной буквы: {words_lowercase}")
    print(f"Знаки препинания: {punctuation}")
    print(f"Является ли '{mac}' правильным MAC-адресом: {is_valid_mac}")
    print(f"Количество слов: {word_count}")
    print(f"Самое длинное слово: '{longest_word}' с номером {longest_index}")
    print(f"Нечетные слова: {odd_words}")

    # Сохранение результатов в файл
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(f"Количество предложений: {sentence_count}\n")
        f.write(f"Типы предложений: {sentence_types}\n")
        f.write(f"Средняя длина предложения (символы, только слова): {avg_sentence_len:.2f}\n")
        f.write(f"Средняя длина слова (символы): {avg_word_len:.2f}\n")
        f.write(f"Количество смайликов: {smiley_count}\n")

    # Архивация файла с результатами
    with zipfile.ZipFile('output.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('output.txt')

    # Получение информации о файле в архиве
    with zipfile.ZipFile('output.zip', 'r') as zipf:
        print("\nИнформация о файле в архиве:")
        for info in zipf.infolist():
            print(f"Имя файла: {info.filename}")
            print(f"Размер файла: {info.file_size} байт")
            print(f"Сжатый размер: {info.compress_size} байт")