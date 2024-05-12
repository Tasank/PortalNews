from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post
from .filters import PostFilter


class PostList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = ['-post_time']
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['next_sale'] = None
        return context

# Детализация новости
class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'

    def get_object(self):
        # Переопределение метода для фильтрации по типу 'NW'
        return get_object_or_404(Post, pk=self.kwargs.get('pk'), type='NW')

# Детализация статьи
class ArticleDetail(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        # Переопределение метода для фильтрации по типу 'AR'
        return get_object_or_404(Post, pk=self.kwargs.get('pk'), type='AR')

class PostDetail(DetailView):
    model = Post
    template_name = 'the_news.html'
    context_object_name = 'the_news'

# Представление для списка новостей
class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'  # Указываем имя шаблона, который будет использоваться
    context_object_name = 'news'

    def get_queryset(self):
        # Фильтруем посты по типу 'NW' для новостей
        return Post.objects.filter(type='NW')

# Представление для списка статей
class ArticleListView(ListView):
    model = Post
    template_name = 'article_list.html'  # Указываем имя шаблона, который будет использоваться
    context_object_name = 'articles'

    def get_queryset(self):
        # Фильтруем посты по типу 'AR' для статей
        return Post.objects.filter(type='AR')

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_initial(self):
        return {'type': 'NW'}

class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


# Аналогичные классы для статей, но с другим начальным значением для 'type'
class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_initial(self):
        return {'type': 'AR'}


class ArticleEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('article_list')