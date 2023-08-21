from django.contrib import admin
from .models import Order, OrderItems

# Register your models here.
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('order_id','username')

@admin.register(OrderItems)
class OrderItemsModelAdmin(admin.ModelAdmin):
    list_display = ('order','products','quantity','total_price')