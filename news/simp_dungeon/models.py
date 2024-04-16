from django.db import models

# Create your models here.
class Order(models.Model):
    time_in = models.DateField(auto_now_add =True)
    time_out = models.DateField(auto_now = True)
    cost = models.FloatField()

class Products_Orders(models.Model):
    pass

class Staff(models.Model):
    full_name = models.CharField(max_length = 150)
    position = models.CharField(max_length = 150)
    labor_contract = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField(default = 0.0)