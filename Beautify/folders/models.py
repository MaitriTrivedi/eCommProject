from django.db import models

# Create your models here.

class Folders(models.Model):
    name = models.CharField(max_length=10)
    parent_folder= models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    hierarchy_number = models.PositiveIntegerField(default=0)  # New field


    def __str__(self):
        return f"{self.name}"
    
    def get_hierarchy(self):
        hierarchy = [self.name]
        current_folder = self

        while current_folder.parent:
            hierarchy.insert(0, current_folder.parent.name)
            current_folder = current_folder.parent

        return ' > '.join(hierarchy)