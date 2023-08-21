from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    

class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    products = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    total_price=models.FloatField(null=True)