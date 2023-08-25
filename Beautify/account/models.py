from django.db import models
from django.contrib.auth.models import User
# from products.models import Products
# from main.models import CartItems

# Create your models here.
class Sellers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name
    
class UserData(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=200)
    address=models.CharField(max_length=300)
    contact=models.CharField(max_length=15)
    profile_image=models.ImageField(upload_to='profile',null=True,default = None)
    # def get_cart_count(self):
    #     user = CartItems.objects.filter(cart__is_paid=False,cart__username=self.username)
    #     count=0
    #     for i in user:
    #         count=count+i.quantity
    #     return count


