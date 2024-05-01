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
        # 'r' означает на режим открытия файла
        # Чтобы всё заработало нужно указать кодировку encoding='utf-8'
        with open(file_path, 'r', encoding='utf-8') as file:
            for word in file:
                censored_words[word.strip()] = True
        words = mystem.lemmatize(value)
        censored_text = []
        # добавление в новый список цензурованного текста
        for word in words:
            if word.strip() in censored_words:
                censored_text.append('*' * len(word))
            else:
                censored_text.append(word)

        return ''.join(censored_text)

    return value
