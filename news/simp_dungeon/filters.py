from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'name': ['icontains'],
           # количество товаров должно быть больше или равно
           'quantity': ['gt'],
           'price': [
               'lt',  # цена должна быть меньше или равна указанной
               'gt',  # цена должна быть больше или равна указанной
           ],
       }