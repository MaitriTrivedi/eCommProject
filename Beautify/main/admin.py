from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(Category)
# @admin.register(Category)
# class CategoryModelAdmin(admin.ModelAdmin):
#     list_display = ('name',)



@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ('couponcode','is_expired','discount','min_amount')

