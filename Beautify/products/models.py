from django.db import models
from account.models import Sellers
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
    
class Wishlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Wishlist')

    def __str__(self):
        return f"Wishlist for {self.username}"

class WishlistItems(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
    products = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True, related_name='wishlist_products')

    def __str__(self):
        return f"{self.products} - {self.wishlist.username}"

