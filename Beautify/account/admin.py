from django.contrib import admin
from .models import UserData, Sellers

# Register your models here.
@admin.register(UserData)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username','email','address','contact')

@admin.register(Sellers)
class SellersModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','company_name','address','phone')
