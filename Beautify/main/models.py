from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 
CATEGORY_CHOICES=(
    ('MAKEUP','MakeUp'),
    ('HAIR','HairCare'),
    ('LIPS','LipsCare'),
    ('EYE','EyeShadow'),
    ('NAIL','Nails'),
    ('FOOT','FootCare'),
    ('FACE','FaceProducts'),
)


class Sellers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name

class Products(models.Model):
    seller=models.ForeignKey(Sellers,default=1,on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=100,null=True)
    price = models.FloatField(null=False)
    description = models.TextField(null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=30,null=True)
    quantity  = models.IntegerField(default=0,null=True)
    product_image = models.ImageField(upload_to='product',null=True,default = None)
    
    def __int__(self):
        return self.product_id
    

class UserData(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=200)
    address=models.CharField(max_length=300)
    contact=models.CharField(max_length=15)

    def get_cart_count(self):
        user = CartItems.objects.filter(cart__is_paid=False,cart__username=self.username)
        count=0
        for i in user:
            count=count+i.quantity
        return count

class Coupon(models.Model):
    couponcode = models.CharField(max_length=10)
    is_expired= models.BooleanField(default=False)
    discount = models.IntegerField(default=100)
    min_amount=models.IntegerField(default=500)

class Cart(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    is_paid=models.BooleanField(default=False)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    products = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    total_price=models.FloatField(null=True)

    def get_quantity(self,cart,products):
        return CartItems.objects.filter(cart=cart,products=products)
    
    def get_total_price(self):
        pass
    
    def __str__(self):
        uname = self.cart.username
        return f"{uname}"
    
class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    

class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    products = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    total_price=models.FloatField(null=True)
