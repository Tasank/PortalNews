from .models import Category, Post, Comment
from modeltranslation.translator import register, \
    TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('Title',)  # указываем, какие именно поля надо переводить в виде кортежа

@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('text', 'title')