from django import template
from pymystem3 import Mystem
from pygtrie import Trie
import os
# Импортируем стороннюю библиотеку которая будет цензурить русский язык
# pymystem3 - мощный инструмент для работы с русским языком
# Trie - будет уменьшать сложность
# os - нужен для открытия файла с нежелательными словами

register = template.Library()
mystem = Mystem()

@register.filter
def censor(value):
    if isinstance(value, str):
        # Загружаем список матерных слов в Trie
        censored_words = Trie()

        file_path = os.path.join(os.path.dirname(__file__), 'censored_words.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            for word in file:
                # Убедимся, что добавляем только строки без пробелов
                censored_words[word.strip()] = True

        # Применяем lemmatize и убираем пробелы для каждого слова в результате
        words = mystem.lemmatize(value)
        words = [word.strip() for word in words if isinstance(word, str) and word.strip()]

        censored_text = []
        for word in words:
            # Проверяем, есть ли слово в списке цензурируемых, и заменяем его звездочками, если нужно
            if word in censored_words:
                censored_text.append('*' * len(word))
            else:
                censored_text.append(word)

        return ''.join(censored_text)

    return value

