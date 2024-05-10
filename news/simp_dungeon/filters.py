from django_filters import FilterSet, DateFilter, CharFilter
from django_filters.widgets import RangeWidget
from .models import Post

class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Имя автора')
    post_time = DateFilter(field_name='post_time', lookup_expr='gt', widget=RangeWidget(attrs={'type': 'date'}), label='Поиск по дате')

    class Meta:
        model = Post
        fields = []
    # Пустой список fields используется, т.к. все фильтры определены вручную выше. Автоматическая генерация фильтров не требуется.