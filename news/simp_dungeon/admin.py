from django.contrib import admin
from .models import Category, Post, Comment, Author

from .forms import GlassForm

# Функция обнуления рейтинга у всех постов
def reset_post_ratings(modeladmin, request, queryset):
    queryset.update(rating=0)
reset_post_ratings.short_description = 'Обнулить рейтинг у выбранных постов'

# создаём новый класс для представления постов в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'post_time', 'rating')
    list_filter = ('type', 'rating', 'category')
    search_fields = ('title', 'category__Title')
    actions = [reset_post_ratings] # добавляем действия в список
    form = GlassForm

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)

# разрегистрируем наши товары
# admin.site.unregister(Comment)
