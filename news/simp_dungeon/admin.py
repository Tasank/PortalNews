from django.contrib import admin
from .models import Category, Post, Comment, Author
# импортируем модель амдинки (вспоминаем про переопределение стандартных админ-инструментов)
from modeltranslation.admin import TranslationAdmin
from .forms import GlassForm

# Функция обнуления рейтинга у всех постов
def reset_post_ratings(modeladmin, request, queryset):
    queryset.update(rating=0)
reset_post_ratings.short_description = 'Обнулить рейтинг у выбранных постов'

# создаём новый класс для представления постов в админке
class PostAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('title', 'type', 'post_time', 'rating')
    list_filter = ('type', 'rating', 'category')
    search_fields = ('title', 'category__Title')
    actions = [reset_post_ratings] # добавляем действия в список
    form = GlassForm
    model = Post
class CategoryAdmin(TranslationAdmin):
    model = Category

# Класс для представления авторов
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')

# Класс для представления комментариев
class CommentAdmin(TranslationAdmin,admin.ModelAdmin):
    list_display = ('user', 'comment_time', 'rating')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)

# разрегистрируем наши комментарии
# admin.site.unregister(Comment)