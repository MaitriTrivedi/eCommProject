from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.
class Cart(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts',unique=True)
    is_paid=models.BooleanField(default=False)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    products = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True,related_name='cart_products')
    quantity = models.IntegerField(default=1)
    total_price=models.FloatField(default=0,null=True)

    def get_quantity(self,cart):
        return (i.quantity for i in  CartItems.objects.filter(cart=cart))
    
    def get_total_price(self):
        pass
    
    def __str__(self):
        uname = self.cart.username
        return f"{uname}"
    