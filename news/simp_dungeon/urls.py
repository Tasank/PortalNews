from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, NewsListView, ArticleListView, NewsCreate, NewsEdit, NewsDelete,
                    ArticleCreate, ArticleEdit, ArticleDelete)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/', NewsListView.as_view(), name='news-list'),
    path('articles/', ArticleListView.as_view(), name='article-list'),

   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
   path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

   path('news/search', PostList.as_view(), name='news_search'),
]