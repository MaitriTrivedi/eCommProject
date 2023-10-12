from django.contrib import admin
from .models import Folders

# Register your models here.

@admin.register(Folders)
class FoldersModelAdmin(admin.ModelAdmin):
    list_display = ('name','parent_folder','hierarchy_number')

