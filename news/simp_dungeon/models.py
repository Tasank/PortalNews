from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self):
        # .aggregate() для вычислительных операций
        post_rating = Post.objects.filter(author=self).aggregate(models.Sum('rating'))
        comments_rating = Comment.objects.filter(user=self.user).aggregate(models.Sum('rating'))
        total_rating_posts = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))

        print()
        print(post_rating)
        print()
        print(comments_rating)
        print()
        print(total_rating_posts)

        self.rating = post_rating['rating__sum'] * 3 + \
           comments_rating['rating__sum'] + total_rating_posts['rating__sum']
        self.save()


class Category(models.Model):
    Title = models.CharField(max_length=125, unique=True)
    subscribers = models.ManyToManyField(User,related_name='categories', through='CategorySubscribe')

    def __str__(self):
        return self.Title

class Post(models.Model):
    # Значения новость или статья
    article = "AR"
    news = 'NW'

    ARTICLES = [(article, 'Статья'),
                (news, 'Новость')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=ARTICLES, default=article)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return f'/news/{self.id}'

    # Метод просмотр, который возвращает первые 124 символа текста статьи
    def preview(self):
        return f"{self.text[0:124]}..."

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'


# Добавляем on-delete, чтобы при удалении объекта, удалялись все связанные с ними
# данные
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=600)
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class CategorySubscribe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)