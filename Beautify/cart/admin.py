from django.contrib import admin
from .models import Cart, CartItems

# Register your models here.
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('username','is_paid')

@admin.register(CartItems)
class CartItemsModelAdmin(admin.ModelAdmin):
    list_display = ('cart','products','quantity','total_price')