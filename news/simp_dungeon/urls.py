from django.urls import path
from .views import (PostList, PostDetail, NewsListView, ArticleListView, NewsCreate, NewsEdit, NewsDelete,
                    ArticleCreate, ArticleEdit, ArticleDelete, subscribe)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path — означает путь.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),

    # Новости
    path('news/', NewsListView.as_view(), name='news-list'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', login_required(NewsEdit.as_view()), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # Статьи
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', login_required(ArticleEdit.as_view()), name='article_edit'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

    path('news/search', PostList.as_view(), name='news_search'),
    path('category/<int:pk>/subscribers', subscribe, name='subscribe'),
]
