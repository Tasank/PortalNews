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
        for lemma in lemmas:
            if 'редиска' in lemma.lower():
                censored_value.append("*" * len(lemma))
            else:
                censored_value.append(lemma)
        return "".join(censored_value)
    else:
        return value
