from django.db import models
from account.models import Sellers
# Create your models here.


CATEGORY_CHOICES=(
    ('MAKEUP','MakeUp'),
    ('HAIR','HairCare'),
    ('LIPS','LipsCare'),
    ('EYE','EyeShadow'),
    ('NAIL','Nails'),
    ('FOOT','FootCare'),
    ('FACE','FaceProducts'),
)

class Products(models.Model):
    seller=models.ForeignKey(Sellers,default=1,on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=100,null=True)
    price = models.FloatField(null=False)
    description = models.TextField(null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=30,null=True)
    quantity  = models.IntegerField(default=0,null=True)
    product_image = models.ImageField(upload_to='product',null=True,default = None)
    
    def __int__(self):
        return self.product_id