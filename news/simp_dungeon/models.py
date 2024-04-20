from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    pass

class Category(models.Model):
    Title = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    pass

class PostCategory(models.Model):
    pass
class Comment(models.Model):
    pass