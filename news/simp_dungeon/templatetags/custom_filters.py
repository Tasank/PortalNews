from django import template
from pymystem3 import Mystem
# Импортируем стороннюю библиотеку которая будет цензурить русский язык
# pymystem3 - мощный инструмент для работы с русским языком
register = template.Library()
mystem = Mystem()

@register.filter
def censor(value):
    if isinstance(value, str):
        lemmas = mystem.lemmatize(value)
        censored_value = []
        ban_words = ['редиска']
        for lemma in lemmas:
            for ban_word in ban_words:
                if ban_word in lemma.lower():
                    censored_value.append("*" * len(lemma))
                    break
                else:
                    censored_value.append(lemma)
        return "".join(censored_value)
    else:
        return value
