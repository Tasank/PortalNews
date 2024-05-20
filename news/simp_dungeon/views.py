from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import get_object_or_404


from .forms import PostForm
from .models import Post
from .filters import PostFilter


class PostList(ListView, LoginRequiredMixin):
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

class PostDetail(DetailView):
    model = Post
    template_name = 'the_news.html'
    context_object_name = 'the_news'




# Детализация новости
class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'

    def get_object(self):
        # Переопределение метода для фильтрации по типу 'NW'
        return get_object_or_404(Post, pk=self.kwargs.get('pk'), type='NW')

# Представление для списка новостей
class NewsListView(ListView, LoginRequiredMixin):
    model = Post
    template_name = 'news_list.html'  # Указываем имя шаблона, который будет использоваться
    context_object_name = 'news'

    def get_queryset(self):
        # Фильтруем посты по типу 'NW' для новостей
        return Post.objects.filter(type='NW')

class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('simp_dungeon.add_post',)
    success_url = reverse_lazy('post_list')

    def get_initial(self):
        return {'type': 'NW'}

    def form_valid(self, form):
        post = form.save(commit=False)
        return super().form_valid(form)

class NewsEdit(PermissionRequiredMixin, UpdateView): # Добавление LoginRequiredMixin для проверки аунтификации
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('simp_dungeon.change_post',)
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().filter(type='NW')


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')



# Детализация статьи
class ArticleDetail(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        # Переопределение метода для фильтрации по типу 'AR'
        return get_object_or_404(Post, pk=self.kwargs.get('pk'), type='AR')

# Представление для списка статей
class ArticleListView(ListView, LoginRequiredMixin):
    model = Post
    template_name = 'article_list.html'  # Указываем имя шаблона, который будет использоваться
    context_object_name = 'articles'

    def get_queryset(self):
        # Фильтруем посты по типу 'AR' для статей
        return Post.objects.filter(type='AR')


# Аналогичные классы для статей, но с другим значением для 'type'
class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('simp_dungeon.add_post')
    success_url = reverse_lazy('post_list')

    def get_initial(self):
        return {'type': 'AR'}

    def form_valid(self, form):
        post = form.save(commit=False)
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('simp_dungeon.change_post')
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().filter(type='AR')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')