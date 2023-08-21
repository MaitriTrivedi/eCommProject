from django.contrib import admin
from .models import Products

# Register your models here.
@admin.register(Products)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_name','seller','price','description','category','product_image')

