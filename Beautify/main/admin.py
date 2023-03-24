from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Products)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_name','seller','price','description','category','product_image')

@admin.register(UserData)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username','email','address','contact')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('username','is_paid')

@admin.register(Sellers)
class SellersModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','company_name','address','phone')

@admin.register(CartItems)
class CartItemsModelAdmin(admin.ModelAdmin):
    list_display = ('cart','products','quantity','total_price')

@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ('couponcode','is_expired','discount','min_amount')

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('order_id','username')

@admin.register(OrderItems)
class OrderItemsModelAdmin(admin.ModelAdmin):
    list_display = ('order','products','quantity','total_price')