from django.db import models
from django.contrib.auth.models import User
from account.models import Sellers

# Create your models here.

class Coupon(models.Model):
    couponcode = models.CharField(max_length=10)
    is_expired= models.BooleanField(default=False)
    discount = models.IntegerField(default=100)
    min_amount=models.IntegerField(default=500)


