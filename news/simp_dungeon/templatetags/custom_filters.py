from django import template
from pygtrie import Trie
import os

register = template.Library()

@register.filter
def censor(value):
    if isinstance(value, str):
        censored_words = Trie()

        file_path = os.path.join(os.path.dirname(__file__), 'censored_words.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            for word in file:
                censored_words[word.strip()] = True

        words = value.split()
        censored_text = []

        for word in words:
            stripped_word = word.strip('.,!?')
            if stripped_word in censored_words:
                censored_word = word.replace(stripped_word, '*' * len(stripped_word))
                censored_text.append(censored_word)
            else:
                censored_text.append(word)

        return ' '.join(censored_text)

    return value
