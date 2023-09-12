from django.contrib import admin
from .models import Products, Wishlist, WishlistItems

# Register your models here.
@admin.register(Products)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_name','seller','price','description','category','product_image')

@admin.register(Wishlist)
class SellersModelAdmin(admin.ModelAdmin):
    list_display = ('username',)

@admin.register(WishlistItems)
class SellersModelAdmin(admin.ModelAdmin):
    list_display = ('wishlist','products')
